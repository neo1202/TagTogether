from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import Base  # 导入全局 Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)  # 存储明文密码（建议后续加密）
    weight = Column(Float, default=1)
    is_old_customer = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
