from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"
    wallet_balance: int = 500

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    wallet_balance: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    accessToken: str
    refreshToken: str

class RefreshTokenRequest(BaseModel):
    refreshToken: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user: UserOut
    accessToken: str
    refreshToken: str