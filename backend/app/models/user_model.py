from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 創建基礎類
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)

    def __init__(self, username: str, password_hash: str, email: str = None):
        self.username = username
        self.password_hash = password_hash
        self.email = email
