from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.deps import get_current_user
from app.core.errors import AppException, UnauthenticatedError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepo
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.schemas.common import DataEnvelope

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=DataEnvelope[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = UserRepo.get_by_email(db, req.email)
    if existing:
        raise AppException(
            code="CONFLICT",
            message=f"Email {req.email} is already registered",
            status_code=status.HTTP_409_CONFLICT,
        )

    hashed_pw = get_password_hash(req.password)
    user = UserRepo.create(db, email=req.email, password_hash=hashed_pw)
    token = create_access_token(subject=str(user.id))

    return DataEnvelope(
        data=TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES * 60,
        )
    )

@router.post("/login", response_model=DataEnvelope[TokenResponse])
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = UserRepo.get_by_email(db, req.email)
    if not user or not verify_password(req.password, user.password_hash):
        raise UnauthenticatedError("Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return DataEnvelope(
        data=TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES * 60,
        )
    )

@router.get("/me", response_model=DataEnvelope[UserResponse])
def get_me(current_user: User = Depends(get_current_user)):
    return DataEnvelope(data=UserResponse.model_validate(current_user))
