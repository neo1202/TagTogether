from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.team_model import TeamMember
from datetime import datetime


class UserRepository:
    @staticmethod
    def update_user_weight(db: Session, user_id: int):
        # 获取该用户加入的总团队数
        total_teams = db.query(TeamMember).filter(TeamMember.user_id == user_id).count()
        # 更新用户权重
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.weight = 1 / total_teams if total_teams > 0 else 1
            db.commit()
        return user

    @staticmethod
    def get_user_id_by_username(db: Session, username: str) -> int:
        # 通过用户名获取用户 ID
        user = db.query(User).filter(User.user_name == username).first()
        if user:
            return user.id
        return None

    # 用戶上傳文章後 自動更新自己的 last_update
    @staticmethod
    def update_last_checkin_time(db: Session, user_id: int):
        # 更新用户的 last_update 字段
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_update = datetime.utcnow()
            db.commit()
        return user

