import os
from typing import Dict


def load_ndsp_db_env(force: bool = True) -> Dict[str, str]:
    """
    NDSP runtime DB environment loader.

    Important:
    - Do NOT read /etc/ndsp/ndsp-db.env from Python workers.
    - systemd loads secrets using EnvironmentFile.
    - This function only normalizes already-loaded environment variables.
    """

    database_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or os.environ.get("AUTH_DATABASE_URL")

    pg_host = os.environ.get("PGHOST") or os.environ.get("DB_HOST") or os.environ.get("POSTGRES_HOST") or "127.0.0.1"
    pg_port = os.environ.get("PGPORT") or os.environ.get("DB_PORT") or os.environ.get("POSTGRES_PORT") or "5432"
    pg_database = os.environ.get("PGDATABASE") or os.environ.get("DB_NAME") or os.environ.get("DB_DATABASE") or os.environ.get("POSTGRES_DB") or os.environ.get("POSTGRES_DATABASE") or "ndsp_auth"
    pg_user = os.environ.get("PGUSER") or os.environ.get("DB_USER") or os.environ.get("DB_USERNAME") or os.environ.get("POSTGRES_USER") or "ndsp_auth"
    pg_password = os.environ.get("PGPASSWORD") or os.environ.get("DB_PASSWORD") or os.environ.get("POSTGRES_PASSWORD")

    aliases = {
        "DATABASE_URL": database_url,
        "POSTGRES_URL": database_url,
        "AUTH_DATABASE_URL": database_url,
        "PGHOST": pg_host,
        "PGPORT": pg_port,
        "PGDATABASE": pg_database,
        "PGUSER": pg_user,
        "PGPASSWORD": pg_password,
        "DB_HOST": pg_host,
        "DB_PORT": pg_port,
        "DB_NAME": pg_database,
        "DB_DATABASE": pg_database,
        "DB_USER": pg_user,
        "DB_USERNAME": pg_user,
        "DB_PASSWORD": pg_password,
        "POSTGRES_HOST": pg_host,
        "POSTGRES_PORT": pg_port,
        "POSTGRES_DB": pg_database,
        "POSTGRES_DATABASE": pg_database,
        "POSTGRES_USER": pg_user,
        "POSTGRES_PASSWORD": pg_password,
    }

    for key, value in aliases.items():
        if value is None:
            continue
        if force or not os.environ.get(key):
            os.environ[key] = str(value)

    return {k: v for k, v in aliases.items() if v is not None}


load_ndsp_db_env(force=True)
