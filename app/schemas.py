from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.user
    company_id: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    company_id: int

    class Config:
        orm_mode = True

class EmployeeCreate(BaseModel):
    name: str
    password: str 
    email: EmailStr
    role: UserRole = UserRole.user
    company_id: int
    position: str
    salary: int

class EmployeeResponse(BaseModel):
    id: int
    position: str
    salary: int
    user: UserResponse

    class Config:
        orm_mode = True


# Company

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        orm_mode = True
