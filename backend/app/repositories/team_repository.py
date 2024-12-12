from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.team_model import Team, TeamMember
from app.repositories.user_repository import UserRepository

# add： 添加对象到db Session。
# flush： 获取主键或生成的字段值。
# commit： 提交所有事务操作。
# refresh： 确保对象与数据库同步。

class TeamRepository:
    @staticmethod
    def get_all_teams(db: Session):
        return db.query(Team).all()

    @staticmethod
    def get_team_by_name(db: Session, name: str):
        return db.query(Team).filter(Team.team_name == name).first()

    @staticmethod
    def create_team(db: Session, team_name: str):
        new_team = Team(team_name=team_name)
        db.add(new_team)
        db.flush()
        # 初始化團隊分數為0
        TeamRepository.init_team_score(db, new_team.id, new_team.team_name) 
        db.commit()  # 一次性提交所有更改，包含init_team_score的
        db.refresh(new_team)  # 确保 new_team 是最新的对象
        return new_team

    @staticmethod
    def add_team_member(db: Session, team_name: str, user_name: str):
        # 查找团队和用户
        team = db.query(Team).filter(Team.team_name == team_name).first()
        user = db.query(User).filter(User.user_name == user_name).first()
        if not team:
            raise ValueError("Team not found.")
        if not user:
            raise ValueError("User not found.")
        # 添加团队成员
        team_member = TeamMember(team_id=team.id, user_id=user.id, team_name=team_name, user_name=user_name)
        db.add(team_member)
        db.commit()
        # 更新用户权重
        UserRepository.update_user_weight(db, user.id)
        return team_member
    @staticmethod
    def get_team_members(db: Session, team_id: int):
        # 获取团队成员
        team_members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        return [{"user_id": member.user_id, "user_name": member.user_name} for member in team_members]

    @staticmethod
    def init_team_score(db: Session, team_id: int, team_name: str):
        default_score = Score(
            team_id=team_id,
            team_name=team_name,
            score=0.0,  # 默认分数为 0
        )
        db.add(default_score)

    # 1. 團隊人數 T
    # 2. 團隊默契 S(團隊所有人完成打卡所需的時間，即最後一個的打卡時間與第一位打卡時 間的差距)
    # 3. 團隊內新會員的人數 N
    @staticmethod
    def update_team_scores(db: Session, user_id: int):
        # 找到用戶所在的所有團隊
        team_memberships = db.query(TeamMember).filter(TeamMember.user_id == user_id).all()  # TeamMember表內 entry

        for membership in team_memberships:
            team_id = membership.team_id
            team_name = membership.team_name
            # 計算團隊總人數 T
            T = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()
            # 計算團隊默契 S
            checkins = db.query(Checkin).filter(Checkin.user_id == user_id).order_by(Checkin.timestamp).all()
            if len(checkins) > 1:
                first_checkin = checkins[0].timestamp
                last_checkin = checkins[-1].timestamp
                S = (last_checkin - first_checkin).total_seconds()
            else:
                S = 0  # 單一 Check-in 時默契為 0

            # 計算新會員數量 N
            N = db.query(TeamMember).join(User, TeamMember.user_id == User.id).filter(
                TeamMember.team_id == team_id,
                User.is_old_customer == False  # 新会员的条件
            ).count()

            # 設定 α 和 β 的參數
            alpha = 0.5
            beta = 2
            # 計算團隊分數
            score = T / (alpha * (S + 1)) + beta * N
            # 更新團隊分數表
            existing_score = db.query(Score).filter(Score.team_id == team_id).first()
            if existing_score:
                existing_score.score = score
                existing_score.updated_at = func.now()
            else:
                new_score = Score(
                    team_id=team_id,
                    team_name=team_name,
                    score=score,
                    updated_at=func.now()
                )
                db.add(new_score)

        db.commit()