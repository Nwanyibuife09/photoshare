import os
import uuid
import shutil
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ...database.db import get_db
from ...database.models import Photo, User, Comment, Rating
from ...schemas.schemas import PhotoResponse
from ...auth import get_current_user, require_creator
from ...services import process_uploaded_image

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
def upload_photo(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    caption: str = Form(...),
    location: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    """Upload a new photo (creator only). Triggers background thumbnail."""
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed. Use JPEG, PNG, GIF, or WebP.")

    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_photo = Photo(
        title=title,
        caption=caption,
        location=location,
        tags=tags,
        s3_path=f"/uploads/{filename}",
        owner_id=current_user.id,
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    # Trigger background processing: thumbnail generation
    background_tasks.add_task(process_uploaded_image, db_photo.id, filename)

    return db_photo


import json
import redis
from ...config import settings

# Initialize Redis client
redis_client = redis.from_url(settings.REDIS_URL)

@router.get("/", response_model=List[PhotoResponse])
def list_photos(
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all photos, optionally search by title/tags/location. Cached in Redis."""
    cache_key = f"photos:search:{search}:skip:{skip}:limit:{limit}"
    
    # Try fetching from cache
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except redis.ConnectionError:
        pass # Fallback to DB if Redis is down

    query = db.query(Photo)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Photo.title.ilike(search_term))
            | (Photo.tags.ilike(search_term))
            | (Photo.location.ilike(search_term))
            | (Photo.caption.ilike(search_term))
        )
    
    results = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()
    
    # Serialize and cache results for 60 seconds
    try:
        serialized_results = [
            {
                "id": p.id,
                "title": p.title,
                "caption": p.caption,
                "location": p.location,
                "tags": p.tags,
                "s3_path": p.s3_path,
                "thumbnail_path": p.thumbnail_path,
                "created_at": p.created_at.isoformat(),
                "owner_id": p.owner_id
            } for p in results
        ]
        redis_client.setex(cache_key, 60, json.dumps(serialized_results))
    except redis.ConnectionError:
        pass

    return results


@router.get("/{photo_id}")
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    """Get a single photo with its comments and average rating."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    comments = db.query(Comment).filter(Comment.photo_id == photo_id).all()
    ratings = db.query(Rating).filter(Rating.photo_id == photo_id).all()
    avg_rating = sum(r.score for r in ratings) / len(ratings) if ratings else 0

    return {
        "id": photo.id,
        "title": photo.title,
        "caption": photo.caption,
        "location": photo.location,
        "tags": photo.tags,
        "s3_path": photo.s3_path,
        "thumbnail_path": photo.thumbnail_path,
        "created_at": photo.created_at,
        "owner_id": photo.owner_id,
        "comments": [
            {"id": c.id, "text": c.text, "author_id": c.author_id, "created_at": c.created_at}
            for c in comments
        ],
        "average_rating": round(avg_rating, 1),
        "rating_count": len(ratings),
    }


@router.post("/{photo_id}/comment")
def add_comment(
    photo_id: int,
    text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a comment to a photo (any authenticated user)."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    comment = Comment(text=text, author_id=current_user.id, photo_id=photo_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"id": comment.id, "text": comment.text, "author_id": comment.author_id, "created_at": comment.created_at}


@router.post("/{photo_id}/rate")
def rate_photo(
    photo_id: int,
    score: int = Form(..., ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Rate a photo 1-5 (any authenticated user). Updates existing rating if already rated."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    existing = db.query(Rating).filter(
        Rating.rater_id == current_user.id, Rating.photo_id == photo_id
    ).first()

    if existing:
        existing.score = score
    else:
        rating = Rating(score=score, rater_id=current_user.id, photo_id=photo_id)
        db.add(rating)

    db.commit()
    return {"message": "Rating submitted", "score": score}


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a photo (only the owner/creator can delete their photo)."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
        
    if photo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to delete this photo"
        )

    # 1. Delete files from OS
    if photo.s3_path:
        filename = photo.s3_path.split("/")[-1]
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Failed to delete original image {filepath}: {e}")

    if photo.thumbnail_path:
        thumb_filename = photo.thumbnail_path.split("/")[-1]
        thumb_filepath = os.path.join(UPLOAD_DIR, "thumbnails", thumb_filename)
        if os.path.exists(thumb_filepath):
            try:
                os.remove(thumb_filepath)
            except Exception as e:
                print(f"Failed to delete thumbnail {thumb_filepath}: {e}")

    # 2. Delete database record
    db.delete(photo)
    db.commit()
    
    # Attempt to invalidate Redis cache (broad invalidation for simplicity)
    try:
        from ...config import settings
        import redis
        redis_client = redis.from_url(settings.REDIS_URL)
        # Find all keys matching the photos cache pattern
        for key in redis_client.scan_iter("photos:search:*"):
            redis_client.delete(key)
    except Exception as e:
        print(f"Failed to invalidate cache: {e}")

    return None
