from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schemas import UserLogin, Token
from app.core.security import create_access_token
from app.database import get_db, get_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login", response_model=Token)  # 定义返回给客户端的数据模型是 Token
def login(user: UserLogin, db: Session = Depends(get_db)):  # 注入数据库会话
    db_user = get_user(db, user.user_name)  # 使用 get_user 函数从数据库中获取用户
    print(f"/login, received username: {user.user_name}, pwd: {user.password}")
    
    # 验证用户是否存在以及密码是否匹配
    if not db_user or db_user.password != user.password:  # 直接比较明文密码
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 创建访问令牌
    access_token = create_access_token({"sub": db_user.user_name})
    # 返回生成的 JWT 令牌
    return {"access_token": access_token, "token_type": "bearer"}
# API 调用: 客户端发起 POST 请求到 /login，携带用户名和密码。
# get_db 生成会话: FastAPI 调用 get_db，生成一个数据库会话，并传递给 db 参数。
# get_user 查询用户: get_user(db, user.username) 使用会话查询用户表，返回匹配的用户或 None。
# 验证逻辑: 检查用户是否存在以及密码是否匹配，验证失败则返回 401 错误。
# 令牌生成: 如果验证通过，调用 create_access_token 生成 JWT 令牌，并返回给客户端。