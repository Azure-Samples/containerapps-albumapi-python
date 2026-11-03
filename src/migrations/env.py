from logging.config import fileConfig

from alembic import context

from app.database import Base, engine, connect_with_retry
from app import models  # Registers Album with Base.metadata


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Give Alembic access to our SQLAlchemy models.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    url = engine.url.render_as_string(hide_password=False)

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using an actual database connection."""

    with connect_with_retry() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()