import uuid
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.core.errors import NotFoundError, UnauthenticatedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.startup import Startup
from app.models.user import User
from app.repositories.startup_repo import StartupRepo
from app.repositories.user_repo import UserRepo

def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthenticatedError("Missing or invalid authorization header")
    
    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise UnauthenticatedError("Invalid or expired access token")
    
    try:
        user_id = uuid.UUID(payload["sub"])
    except ValueError:
        raise UnauthenticatedError("Invalid user ID in token")
        
    user = UserRepo.get_by_id(db, user_id)
    if not user:
        raise UnauthenticatedError("User not found")
        
    return user

def get_owned_startup(
    startup_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Startup:
    startup = StartupRepo.get_owned_startup(db, startup_id, current_user.id)
    if not startup:
        # Return 404 instead of 403 to avoid leaking existence of startup
        raise NotFoundError(f"Startup {startup_id} not found")
    return startup
