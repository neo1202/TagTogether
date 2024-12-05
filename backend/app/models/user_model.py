from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from app.models.base import Base  # 导入全局 Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)  # 存储明文密码（建议后续加密）
    weight = Column(Float, default=1)
    is_old_customer = Column(Boolean, default=False)
    last_update = Column(TIMESTAMP, default="2024-12-02")  # 默认为指定日期
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    team_members = relationship("TeamMember", back_populates="user")  # 通过 user.team_members，可以获取用户加入的所有团队

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_name = Column(String)
    content = Column(String)
    timestamp = Column(TIMESTAMP, server_default=func.now())