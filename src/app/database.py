
import os
import struct

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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
