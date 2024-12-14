from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.team_repository import TeamRepository
from app.schemas.team_schemas import CreateTeam, JoinTeam
from app.models.user_model import User
from app.models.team_model import Team, TeamMember, Score
from app.core.security import verify_access_token

router = APIRouter()

# 顯示所有團隊
@router.get("/all-teams/")
def get_teams(db: Session = Depends(get_db)):
    teams = TeamRepository.get_all_teams(db)
    return [{"id": team.id, "name": team.team_name} for team in teams]

# 創建團隊
@router.post("/create-team/")
def create_team(team: CreateTeam, db: Session = Depends(get_db)):
    # 檢查團隊名稱是否已存在
    existing_team = TeamRepository.get_team_by_name(db, team.team_name)
    if existing_team:
        raise HTTPException(status_code=400, detail="Team name already exists.")
    new_team = TeamRepository.create_team(db, team.team_name)
    return {"message": "Team created successfully", "team_id": new_team.id, "team_name": new_team.team_name }

# 加入團隊傳入team_name, user name從jwt得到
@router.post("/join-team/")
def join_team(request: JoinTeam, db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    user_name = payload["sub"]
    # 检查团队是否存在
    team = TeamRepository.get_team_by_name(db, request.team_name)
    # 检查用户是否已经加入团队
    user = db.query(User).filter(User.user_name == user_name).first()
    existing_membership = (
        db.query(TeamMember)
        .filter(TeamMember.user_id == user.id, TeamMember.team_id == team.id)
        .first()
    )
    if existing_membership:
        raise HTTPException(status_code=400, detail="User already in this team.")
    # 添加成员并更新权重
    TeamRepository.add_team_member(db, team.team_name, user_name)
    # 加入成員時更新 所有有關的 team的權重
    TeamRepository.update_team_scores(db, user.id)
    return {"message": f"Successfully joined the team '{team.team_name}'."}

# 获取团队成员列表
@router.get("/team-members/{team_id}")
def get_team_members(team_id: int, db: Session = Depends(get_db)):
    try:
        members = TeamRepository.get_team_members(db, team_id)
        return members
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch team members: {str(e)}")

@router.get("/leaderboard/")
def get_leaderboard(db: Session = Depends(get_db)):
    scores = (
        db.query(Team.team_name, Score.score)
        .join(Score, Team.id == Score.team_id)
        .order_by(Score.score.desc())
        .limit(20)
        .all()
    )
    return [{"team_name": team_name, "score": score} for team_name, score in scores]


# [
#   {
#     "team_name": "Team Alpha",
#     "score": 95.2
#   },
#   {
#     "team_name": "Team Beta",
#     "score": 88.1
#   },
# ]