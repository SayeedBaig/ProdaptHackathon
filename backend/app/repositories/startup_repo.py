import uuid
from sqlalchemy.orm import Session
from app.models.startup import Startup

class StartupRepo:
    @staticmethod
    def create(db: Session, user_id: uuid.UUID, name: str, raw_idea: str) -> Startup:
        startup = Startup(
            user_id=user_id,
            name=name.strip(),
            raw_idea=raw_idea.strip(),
            status="active",
        )
        db.add(startup)
        db.commit()
        db.refresh(startup)
        return startup

    @staticmethod
    def get_by_id(db: Session, startup_id: uuid.UUID) -> Startup | None:
        return db.query(Startup).filter(Startup.id == startup_id).first()

    @staticmethod
    def get_owned_startup(db: Session, startup_id: uuid.UUID, user_id: uuid.UUID) -> Startup | None:
        return db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == user_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[Startup]:
        return (
            db.query(Startup)
            .filter(Startup.user_id == user_id)
            .order_by(Startup.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count_by_user(db: Session, user_id: uuid.UUID) -> int:
        return db.query(Startup).filter(Startup.user_id == user_id).count()

    @staticmethod
    def update_current_version(db: Session, startup: Startup, version_id: uuid.UUID) -> Startup:
        startup.current_version_id = version_id
        db.add(startup)
        db.commit()
        db.refresh(startup)
        return startup

    @staticmethod
    def update(db: Session, startup: Startup, **kwargs) -> Startup:
        for key, value in kwargs.items():
            if hasattr(startup, key) and value is not None:
                setattr(startup, key, value)
        db.add(startup)
        db.commit()
        db.refresh(startup)
        return startup

    @staticmethod
    def delete(db: Session, startup: Startup) -> None:
        db.delete(startup)
        db.commit()
