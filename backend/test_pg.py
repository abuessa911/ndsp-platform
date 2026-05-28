from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise SystemExit("DATABASE_URL is missing in .env")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_user, current_database(), NOW();")
        row = cur.fetchone()
        print({
            "current_user": row[0],
            "current_database": row[1],
            "now": str(row[2]),
        })
