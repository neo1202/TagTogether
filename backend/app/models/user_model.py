from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# 创建基础类
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # 存储明文密码（建议后续加密）
    is_old_customer = Column(Boolean, default=False)

    def __init__(self, username: str, password: str, is_old_customer: bool = False):
        self.username = username
        self.password = password
        self.is_old_customer = is_old_customer
