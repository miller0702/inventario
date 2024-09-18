from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    contrasena: str
    
class UserOut(UserBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    contrasena: str
    
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None
