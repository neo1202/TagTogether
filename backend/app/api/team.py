from fastapi import Security, APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.team_repository import TeamRepository
from app.schemas.team_schemas import CreateTeam, JoinTeam
from app.models.user_model import User
from app.models.team_model import Team, TeamMember, Score
from app.core.security import verify_access_token
from typing import List, Dict, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 定義 HTTPBearer 的依賴 給 leaderboard中jwt使用
auth_scheme = HTTPBearer(auto_error=False)
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
def get_leaderboard(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(auth_scheme)  # 可选 Token
):
    # 預設用戶未登入
    user_team_ids = []

    # 如果提供了 Token，验证并获取用户信息
    if credentials:
        try:
            payload = verify_access_token(credentials)
            user_name = payload["sub"]

            # 找到該用戶所屬的所有隊伍 ID
            user_team_ids = db.query(TeamMember.team_id).filter(
                TeamMember.user_name == user_name
            ).all()
            user_team_ids = [team_id[0] for team_id in user_team_ids]  # 提取 ID 列表
        except HTTPException:
            pass  # 忽略 Token 错误，继续匿名逻辑

    # 查询排行榜数据
    scores = (
        db.query(Team.id, Team.team_name, Score.score)
        .join(Score, Team.id == Score.team_id)
        .order_by(Score.score.desc())
        .limit(20)
        .all()
    )
    # 返回數據，對於未登入的用戶，所有隊伍的 is_user_team 為 False
    return [
        {
            "team_id": team_id,
            "team_name": team_name,
            "score": score,
            "is_user_team": team_id in user_team_ids  # 判斷是否為使用者的隊伍
        }
        for team_id, team_name, score in scores
    ]

@router.get("/score-info/{team_id}")
def get_team_score_info(team_id: int, db: Session = Depends(get_db)) -> Dict:
    # 获取团队数据
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    # 获取团队成员
    team_members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    member_ids = [member.user_id for member in team_members]
    
    if not member_ids:
        return {
            "team_name": team.team_name,
            "total_members": 0,
            "new_members": 0,
            "earliest_checkin": None,
            "latest_checkin": None,
        }

    # 查询用户数据
    users = db.query(User).filter(User.id.in_(member_ids)).all()

    # 计算总人数（基于 weight）和新会员人数（基于 weight 和 is_old_customer）
    total_members_weight = sum(user.weight for user in users)
    new_members_weight = sum(user.weight for user in users if not user.is_old_customer)

    # 查找最早和最晚打卡时间
    earliest_user = min(users, key=lambda x: x.last_update)
    latest_user = max(users, key=lambda x: x.last_update)

    return {
        "team_name": team.team_name,
        "total_members": total_members_weight,
        "new_members": new_members_weight,
        "earliest_checkin": {
            "name": earliest_user.user_name,
            "time": earliest_user.last_update,
        },
        "latest_checkin": {
            "name": latest_user.user_name,
            "time": latest_user.last_update,
        },
    }