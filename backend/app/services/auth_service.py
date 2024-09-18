from passlib.context import CryptContext

from backend.app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return False
    if not pwd_context.verify(password, user.contrasena):
        return False
    return user
