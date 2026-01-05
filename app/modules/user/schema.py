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
    access_token: str
    token_type: str = "bearer"
