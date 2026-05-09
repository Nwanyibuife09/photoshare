"""
Background services for PhotoShare:
1. Thumbnail generation (Pillow)
2. Cognitive image analysis (local Pillow-based analysis + architecture ready for cloud AI)
"""
import os
import json
from PIL import Image
from collections import Counter

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
THUMB_DIR = os.path.join(UPLOAD_DIR, "thumbnails")
os.makedirs(THUMB_DIR, exist_ok=True)

THUMBNAIL_SIZE = (400, 400)


def generate_thumbnail(filename: str) -> str:
    """Generate a thumbnail for an uploaded image. Returns the thumbnail path."""
    source_path = os.path.join(UPLOAD_DIR, filename)
    thumb_filename = f"thumb_{filename}"
    thumb_path = os.path.join(THUMB_DIR, thumb_filename)

    try:
        with Image.open(source_path) as img:
            img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
            # Convert RGBA to RGB if needed for JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_path, "JPEG", quality=85, optimize=True)
        return f"/uploads/thumbnails/{thumb_filename}"
    except Exception as e:
        print(f"Thumbnail generation failed for {filename}: {e}")
        return ""


def process_uploaded_image(photo_id: int, filename: str):
    """
    Background task: generates thumbnail + runs cognitive analysis.
    Updates the database record with the results.
    """
    from .database.db import SessionLocal
    from .database.models import Photo

    # 1. Generate thumbnail
    thumb_path = generate_thumbnail(filename)

    # 3. Update DB
    db = SessionLocal()
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            if thumb_path:
                photo.thumbnail_path = thumb_path

            db.commit()
            print(f"Processed photo {photo_id}: thumbnail={thumb_path}")
    except Exception as e:
        print(f"DB update failed for photo {photo_id}: {e}")
        db.rollback()
    finally:
        db.close()
