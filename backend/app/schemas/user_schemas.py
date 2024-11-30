# 這個文件的主要用途是 定義 Pydantic 模式（schemas），用於：

## 請求數據的驗證：
# 確保從前端發送到後端的數據格式正確，類似於表單驗證。
## 響應數據的序列化：
# 定義後端返回給前端的數據結構，統一數據格式。
from pydantic import BaseModel, EmailStr

# 用於用戶登入請求
class UserLogin(BaseModel):
    username: str
    password: str

# 用於生成 JWT 的響應模式
class Token(BaseModel):
    access_token: str
    token_type: str

# 用於用戶註冊請求
class UserRegister(BaseModel):
    username: str
    email: EmailStr  # 驗證是否為合法郵箱
    password: str

# 用於返回給前端的用戶信息
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str


