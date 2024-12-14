# 這個文件的主要用途是 定義 Pydantic 模式（schemas），用於：

## 請求數據的驗證：
# 確保從前端發送到後端的數據格式正確，類似於表單驗證。
## 響應數據的序列化：
# 定義後端返回給前端的數據結構，統一數據格式。
from pydantic import BaseModel
from typing import Optional
# 用於用戶註冊請求
class UserRegister(BaseModel):
    user_name: str
    password: str
    is_old_customer: Optional[bool] = False  # Default to False

# 用於用戶登入請求
class UserLogin(BaseModel):
    user_name: str
    password: str

# 用於生成 JWT 的響應模式
class Token(BaseModel):
    access_token: str
    token_type: str

# 用於返回給前端的用戶信息
class UserResponse(BaseModel):
    id: int
    user_name: str
    created_at: str

class UploadPost(BaseModel):
    content: str


