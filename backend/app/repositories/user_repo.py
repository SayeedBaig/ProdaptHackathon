import uuid
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepo:
    @staticmethod
    def get_by_id(db: Session, user_id: uuid.UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower().strip()).first()

    @staticmethod
    def create(db: Session, email: str, password_hash: str) -> User:
        user = User(
            email=email.lower().strip(),
            password_hash=password_hash,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
