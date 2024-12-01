# 存放與認證相關的路由，如登入和註冊
from fastapi import APIRouter, HTTPException
from app.schemas.user_schemas import UserLogin, Token
from app.core.security import create_access_token
from app.database import get_user

router = APIRouter()

@router.post("/login", response_model=Token)  # 定义返回给客户端的数据模型是 Token
def login(user: UserLogin):  # 接收一个 UserLogin 类型的参數
    db_user = get_user(user.username)
    print(f"received username:{user.username}, pwd: {user.password}")
    print(f"db_user: {db_user.username}, db_pwd: {db_user.password}")
    if not db_user or db_user.password != user.password:  # 直接比较明文密码
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}  # 生成的 JWT 令牌 , 类型为 bearer

