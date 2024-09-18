from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.contrasena)
    db_user = User(
        email=user.email,
        contrasena=hashed_password,
        nombre=user.nombre,
        apellido=user.apellido,
        documento=user.documento
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, contrasena: str):
    user = db.query(User).filter(User.email == email).first()
    if user is None or not pwd_context.verify(contrasena, user.contrasena):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: UserCreate):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        return None
    existing_user.email = user.email
    existing_user.nombre = user.nombre
    existing_user.apellido = user.apellido
    existing_user.documento = user.documento

    if user.contrasena:
        existing_user.contrasena = pwd_context.hash(user.contrasena)

    db.commit()
    db.refresh(existing_user)
    return existing_user


def eliminar_usuario(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def count_users(db: Session) -> int:
    return db.query(User).count()

