from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        nombre=product.nombre,
        precio=product.precio,
        cantidad=product.cantidad,
        descripcion=product.descripcion
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product: ProductUpdate):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        return None
    for field, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, field, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product


def count_products(db: Session) -> int:
    return db.query(Product).count()