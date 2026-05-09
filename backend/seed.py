"""Seed script to create creator users. Run from the PhotoShare root directory:
   python -m backend.seed
"""
from backend.database.db import SessionLocal, engine, Base
from backend.database.models import User
from backend.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

creators = [
    {"username": "creator1", "email": "creator1@photoshare.com", "password": "Creator123!"},
    {"username": "creator2", "email": "creator2@photoshare.com", "password": "Creator456!"},
]

for creator_data in creators:
    existing = db.query(User).filter(User.username == creator_data["username"]).first()
    if existing:
        print(f"Creator '{creator_data['username']}' already exists, skipping.")
        continue
    user = User(
        username=creator_data["username"],
        email=creator_data["email"],
        hashed_password=get_password_hash(creator_data["password"][:72]),
        is_creator=True,
    )
    db.add(user)
    db.commit()
    print(f"Created creator user: {creator_data['username']}")

db.close()
print("Seeding complete!")
