from pydantic import BaseModel, EmailStr

class TrialRegister(BaseModel):
    client_ip: str | None = None
    device_fingerprint: str | None = None
    email: EmailStr
    name: str

class TokenLogin(BaseModel):
    email: EmailStr
    token: str
