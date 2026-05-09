import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.database.db import SessionLocal
from backend.database.models import Photo
from backend.services import process_uploaded_image

db = SessionLocal()
try:
    photos = db.query(Photo).all()
    for photo in photos:
        filename = photo.s3_path.split("/")[-1]
        print(f"Processing photo {photo.id}: {filename}")
        
        filepath = os.path.join("uploads", filename)
        if os.path.exists(filepath):
            process_uploaded_image(photo.id, filename)
        else:
            print(f"File not found: {filepath}")
finally:
    db.close()
