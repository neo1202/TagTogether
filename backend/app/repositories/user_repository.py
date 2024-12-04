from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.team_model import TeamMember

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
