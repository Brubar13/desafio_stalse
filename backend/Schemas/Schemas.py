from typing import Optional

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class CreateCustomer(BaseModel):
    name: str 
    email: str
    phone: Optional[str] = None