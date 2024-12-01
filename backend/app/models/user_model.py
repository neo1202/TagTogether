from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 创建基础类
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # 存储明文密码
    email = Column(String, unique=True, index=True)

    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email
