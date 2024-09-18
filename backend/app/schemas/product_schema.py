from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    descripcion: Optional[str] = None
