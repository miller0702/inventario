from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routers import user_router, product_router
from app.database.database import SessionLocal
from app.models.user import User
from app.services.user_service import pwd_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(product_router.router)

# Código para crear un usuario por defecto

# def create_admin_user(db: Session):
#     admin_user = db.query(User).filter(User.email == "admin@example.com").first()
#     if admin_user:
#         print("Admin user already exists.")
#         return
#     hashed_password = pwd_context.hash("admin")
#     new_admin = User(
#         documento="0001",
#         nombre="Admin",
#         apellido="User",
#         email="admin@example.com",
#         contrasena=hashed_password 
#     )
#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)
#     print("Admin user created successfully.")

# @app.on_event("startup")
# def on_startup():
#     db = SessionLocal()
#     try:
#         create_admin_user(db)
#     finally:
#         db.close()

@app.get("/")
def read_root():
    return {"message": "API de Inventario de Productos"}
