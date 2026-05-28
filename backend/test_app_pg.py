from app.pg_db import fetch_one

row = fetch_one("SELECT current_user, current_database(), NOW() AS now")
print(row)
