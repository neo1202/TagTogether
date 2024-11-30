# 存放與認證相關的路由，如登入和註冊
from fastapi import APIRouter, HTTPException
from app.schemas.user_schemas import UserLogin, Token
from app.core.security import create_access_token, verify_password
from app.database import get_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
