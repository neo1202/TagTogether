from datetime import datetime, timedelta
import jwt
from jose import JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

load_dotenv()

# 配置
SECRET_KEY = os.getenv("SECRET_KEY")  # 之後、替换为强大的密钥并通过环境变量存储
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建访问令牌
def create_access_token(data: dict) -> str:
    """
    创建一个带有过期时间的 JWT 令牌
    :param data: 包含用户信息的字典，例如 {"sub": "username"}
    :return: 加密后的 JWT 字符串
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # 添加到期时间
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 定義 HTTPBearer 的依賴，能夠自動解析Authorization中的header有沒有token
auth_scheme = HTTPBearer()
def verify_access_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)) -> dict:
    """
    验证 JWT 令牌的有效性并解码
    :param credentials: 自动从 Authorization header 提取的 JWT 令牌
    :return: 解码后的 payload
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise HTTPException(status_code=401, detail="Invalid token: no subject")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

