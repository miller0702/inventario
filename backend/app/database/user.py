from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user_service import pwd_context

def create_admin_user(db: Session):
    # Verifica si el usuario admin ya existe
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if admin_user:
        print("Admin user already exists.")
        return admin_user

    # Si no existe, crea el usuario admin
    hashed_password = pwd_context.hash("admin")  # Hashear la contraseña 'admin'
    new_admin = User(
        documento="0001",
        nombre="Admin",
        apellido="User",
        email="admin@example.com",  # Usar un email válido
        contrasena=hashed_password  # Guardar la contraseña hasheada
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    print("Admin user created successfully.")
    return new_admin
