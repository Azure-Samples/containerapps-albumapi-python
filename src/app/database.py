
import os
import struct
import time
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./albums.db"
)

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)


# Configure Microsoft Entra access-token authentication for Azure SQL.
if DATABASE_URL.startswith("mssql+pyodbc"):
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()

    @event.listens_for(engine, "do_connect")
    def provide_access_token(dialect, conn_rec, cargs, cparams):
        # SQLAlchemy adds Trusted_Connection when no username/password
        # is supplied. Remove it because we authenticate using a token.
        connection_parts = cargs[0].split(";")
        connection_parts = [
            part for part in connection_parts
            if not part.lower().startswith("trusted_connection=")
        ]
        cargs[0] = ";".join(connection_parts)

        # Obtain an access token for Azure SQL.
        token = credential.get_token(
            "https://database.windows.net/.default"
        ).token.encode("utf-16-le")

        # Package the token in the format expected by ODBC Driver 18.
        token_struct = struct.pack(
            f"<I{len(token)}s",
            len(token),
            token
        )

        # SQL_COPT_SS_ACCESS_TOKEN = 1256
        cparams["attrs_before"] = {
            **cparams.get("attrs_before", {}),
            1256: token_struct
        }


# Azure SQL reports an unavailable or still-resuming database as either of
# these, depending on whether the failure lands in the TCP connect or the
# login that follows.
TRANSIENT_CONNECTION_ERRORS = (OperationalError, InterfaceError)


@contextmanager
def connect_with_retry(max_attempts=6, initial_delay=2, max_delay=15):
    """
    Yield a live database connection, retrying transient failures.

    The connection yielded is the one the caller goes on to use, rather than
    a throwaway opened only to test availability. A database resuming from
    auto-pause can refuse connections for a minute or more, so the caller
    would otherwise fail before doing any work.

    Only the connect is retried. A failure raised by the caller's own work
    propagates untouched, because replaying a partially applied migration
    is far more dangerous than failing loudly.
    """
    delay = initial_delay

    for attempt in range(1, max_attempts + 1):
        connection = None

        try:
            connection = engine.connect()
            # Connecting can succeed against a database that cannot yet
            # serve queries, so confirm it really is reachable.
            connection.exec_driver_sql("SELECT 1")

        except TRANSIENT_CONNECTION_ERRORS as exc:
            if connection is not None:
                connection.close()

            if attempt == max_attempts:
                logger.exception(
                    "Database connection failed after %s attempts",
                    max_attempts
                )
                raise

            logger.warning(
                "Database unavailable. Attempt %s/%s failed. "
                "Retrying in %s seconds. Error: %s",
                attempt,
                max_attempts,
                delay,
                exc
            )

            time.sleep(delay)
            delay = min(delay * 2, max_delay)

        else:
            logger.info(
                "Database connection established on attempt %s/%s",
                attempt,
                max_attempts
            )

            try:
                yield connection
            finally:
                connection.close()

            return


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
