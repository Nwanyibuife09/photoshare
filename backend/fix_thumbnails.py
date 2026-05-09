import sys
import os

# Add the backend directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db import SessionLocal
from database.models import Photo
from services import process_uploaded_image

db = SessionLocal()
try:
    photos = db.query(Photo).all()
    for photo in photos:
        filename = photo.s3_path.split("/")[-1]
        print(f"Processing photo {photo.id}: {filename}")
        
        # Only process if the file exists
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", filename)
        if os.path.exists(filepath):
            process_uploaded_image(photo.id, filename)
        else:
            print(f"File not found: {filepath}")
finally:
    db.close()
