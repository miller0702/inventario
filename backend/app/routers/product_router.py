from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product_schema import ProductCreate, ProductOut, ProductUpdate
from app.models.product import Product
from app.services.product_service import (
    create_product,
    get_product,
    get_products,
    update_product,
    delete_product,
    count_products
)
from app.database.database import get_db

router = APIRouter(prefix="/products")

# Listar Productos
@router.get("/getProducts/", response_model=List[ProductOut])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

# Registrar Productos
@router.post("/registerProduct/", response_model=ProductOut)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db, product)
    return db_product

# Listar Producto Por Id
@router.get("/getProduct/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# Actualizar Productos
@router.put("/updateProduct/{product_id}", response_model=ProductOut)
def update_existing_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id, product_update)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

# Eliminar Productos
@router.delete("/deleteProduct/{product_id}", response_model=ProductOut)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# Contar Productos
@router.get("/count/", response_model=int)
def count_registered_products(db: Session = Depends(get_db)):
    total_products = count_products(db)
    return total_products
