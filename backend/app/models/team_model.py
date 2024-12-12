from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base  # 导入全局 Base
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    scores = relationship("Score", back_populates="team", cascade="all, delete-orphan")

class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    team_name = Column(String)
    user_name = Column(String)
    joined_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="team_members")  # team_member.user 可以方便地访问与该记录关联的用户

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)  # 外键关联到 Team 表
    team_name = Column(String, nullable=False)
    score = Column(Float, nullable=False, default=0.0)  # 分数，默认为 0
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # 自动更新时间

    team = relationship("Team", back_populates="scores")  # 方便访问关联的 Team
