# 存放與用戶相關的路由，如獲取當前用戶資訊，上傳貼文
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import Checkin
from app.core.security import verify_access_token
from app.schemas.user_schemas import UploadPost
from app.repositories.user_repository import UserRepository

router = APIRouter()

@router.get("/me")
def get_my_user_name(payload: dict = Depends(verify_access_token)):
    """
    获取当前用户的用户名。
    :param payload: 解码后的 JWT 令牌数据
    :return: 用户名
    """
    return {"user_name": payload["sub"]}
# 假設 Token 有效，payload 的值為：
# {
#     "sub": "testuser",  # 用戶名
#     "exp": 1700000000   # 過期時間戳
# }

@router.post("/upload-post")
def upload_post(content: UploadPost, db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    try:
        user_name = payload["sub"]
        user_id = UserRepository.get_user_id_by_username(db, user_name)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found.")

        # 創建新的 Check-in 寫入資料庫
        new_checkin = Checkin(
            content=content.content,
            user_id=user_id,
            user_name=user_name,
        )
        db.add(new_checkin)
        db.commit()
        db.refresh(new_checkin)
        # 更新這使用者的最後一次上傳時間
        UserRepository.update_last_checkin_time(db, user_id)
        # 更新該用戶所在團隊的分數
        TeamRepository.update_team_scores(db, user_id)
        return {"message": "Post uploaded successfully", "checkin_id": new_checkin.id}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload post.")
