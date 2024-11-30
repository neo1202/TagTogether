# 存放與用戶相關的路由，如獲取當前用戶資訊
from fastapi import APIRouter, Depends
from app.core.security import decode_token

router = APIRouter()

@router.get("/me")
def get_my_username(token: str = Depends(decode_token)):
    return {"username": token["sub"]}
