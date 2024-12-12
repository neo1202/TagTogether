from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.team_model import Team, TeamMember
from app.repositories.user_repository import UserRepository


class TeamRepository:
    @staticmethod
    def get_all_teams(db: Session):
        return db.query(Team).all()

    @staticmethod
    def get_team_by_name(db: Session, name: str):
        return db.query(Team).filter(Team.team_name == name).first()

    @staticmethod
    def create_team(db: Session, name: str):
        new_team = Team(team_name=name)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
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
