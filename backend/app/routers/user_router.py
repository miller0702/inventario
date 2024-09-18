from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user_schema import UserCreate, UserLogin, UserOut, UserBase, UserUpdate
from app.models.user import User
from app.services.user_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_user,
    get_users,
    count_users,
    eliminar_usuario
)
from app.database.database import get_db
from datetime import timedelta

router = APIRouter(prefix="/users")

# Listar Usuarios
@router.get("/getUsers/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

# Registrar Usuarios
@router.post("/registerUser/", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

# Login Usuarios
@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.contrasena)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Listar Usuario Por Id
@router.get("/getUser/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    return user

# Actualizar Usuarios
@router.put("/updateUser/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar Usuarios
@router.delete("/deleteUser/{user_id}", response_model=UserBase)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = eliminar_usuario(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    return user

# Contar Usuarios
@router.get("/count/", response_model=int)
def count_registered_users(db: Session = Depends(get_db)):
    total_users = count_users(db)
    return total_users
