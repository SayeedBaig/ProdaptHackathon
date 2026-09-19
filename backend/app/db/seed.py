from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.repositories.startup_repo import StartupRepo
from app.repositories.user_repo import UserRepo
from app.services.startup_service import StartupService

def seed_demo_data():
    db = SessionLocal()
    try:
        demo_email = "demo@pitchpilot.ai"
        user = UserRepo.get_by_email(db, demo_email)
        if not user:
            print(f"Creating demo user: {demo_email}")
            user = UserRepo.create(
                db=db,
                email=demo_email,
                password_hash=get_password_hash("password123"),
            )
        else:
            print(f"Demo user already exists: {demo_email}")

        # Check if NutriNest demo startup exists
        startups = StartupRepo.list_by_user(db, user.id)
        nutrinest = next((s for s in startups if s.name == "NutriNest"), None)
        if not nutrinest:
            print("Seeding NutriNest demo startup...")
            startup, profile_data, version = StartupService.create_startup(
                db=db,
                user_id=user.id,
                name="NutriNest",
                raw_idea="An app that helps college students living in hostels find affordable, healthy food subscriptions without expensive delivery charges.",
            )
            print(f"Created NutriNest startup ID: {startup.id} with Profile v{version}")
        else:
            print(f"NutriNest demo startup already exists: {nutrinest.id}")

        print("\nDemo Seed Completed Successfully!")
        print("Credentials: demo@pitchpilot.ai / password123")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
