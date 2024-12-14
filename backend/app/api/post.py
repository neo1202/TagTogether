from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User, Checkin
from app.core.security import verify_access_token

router = APIRouter()

@router.get("/posts/", response_model=list)
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取按时间倒序排列的帖子流
    """
    posts = db.query(Checkin).order_by(Checkin.timestamp.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": post.id,
            "user_id": post.user_id,
            "user_name": post.user_name,
            "content": post.content,
            "timestamp": post.timestamp,
        }
        for post in posts
    ]
