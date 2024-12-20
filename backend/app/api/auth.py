from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schemas import UserLogin, Token, UserRegister
from app.core.security import create_access_token
from app.database import get_db_reader, get_db_writer, get_user
from sqlalchemy.orm import Session
from app.models.user_model import User

router = APIRouter()

@router.post("/login", response_model=Token)  # 定义返回给客户端的数据模型是 Token
def login(user: UserLogin, db: Session = Depends(get_db_reader)):  # 注入数据库会话
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

@router.post("/register")
def signup(request: UserRegister, db: Session = Depends(get_db_writer)):
    # 檢查用戶是否已存在
    existing_user = db.query(User).filter(User.user_name == request.user_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    # 創建新用戶
    new_user = User(
        user_name=request.user_name,
        password=request.password,  # 需加密存儲
        is_old_customer=request.is_old_customer,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully."}