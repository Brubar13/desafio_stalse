from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    email: str
    password: str


class TicketCustomerResponse(BaseModel):
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class TicketAssignedUserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: str
    subject: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    customer: TicketCustomerResponse | None
    assigned_user: TicketAssignedUserResponse | None

class UsersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
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
    status: Optional[Literal['closed', 'open']] = None
    priority: Optional[Literal["low", "medium", "high"]] = None

class PatchUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal['user', 'admin']] = None
    is_active: Optional[bool] = None


class PatchCustomerRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

