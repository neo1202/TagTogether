# 存放與用戶相關的路由，如獲取當前用戶資訊
from fastapi import APIRouter, Depends
from app.core.security import verify_access_token

router = APIRouter()

@router.get("/me")
def get_my_username(payload: dict = Depends(verify_access_token)):
    """
    获取当前用户的用户名。
    :param payload: 解码后的 JWT 令牌数据
    :return: 用户名
    """
    return {"username": payload["sub"]}
# 假設 Token 有效，payload 的值為：
# {
#     "sub": "testuser",  # 用戶名
#     "exp": 1700000000   # 過期時間戳
# }