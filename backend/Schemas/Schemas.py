from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    email: str
    password: str

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    assigned_user_id: int | None
    channel: str
    subject: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

class UsersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    password_hash: str
    role: str
    is_active: bool

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: Literal["user", "admin"]

class CreateTicketRequest(BaseModel):
    subject: str
    channel: str
    status: Literal["open"]
    priority: Literal["low", "medium", "high"]
    assigned_user_id: Optional[int] = None
    customer_id: int

class CreateCustomerRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class PatchTicketRequest(BaseModel):
    status: Optional[Literal['closed']] = None
    priority: Optional[Literal["low", "medium", "high"]] = None