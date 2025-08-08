from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str