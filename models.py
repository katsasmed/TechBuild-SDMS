from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: str
    password: str
    otp: str

class LoginResponse(BaseModel):
    message: str
    session_status: str