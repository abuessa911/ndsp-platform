import time
from fastapi import HTTPException

RATE_LIMIT = 20  # requests
WINDOW = 60  # seconds

clients = {}

def rate_limiter(client_id: str):
    now = time.time()
    if client_id not in clients:
        clients[client_id] = []

    clients[client_id] = [t for t in clients[client_id] if now - t < WINDOW]

    if len(clients[client_id]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    clients[client_id].append(now)
