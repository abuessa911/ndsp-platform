from app.services.api_keys import generate_key, init_db

init_db()

key = generate_key("nawaf", plan="pro", days=999)
print("API KEY:", key)
