from app.models.user_model import User
# 模擬一個假數據庫查詢函數
def get_user(username: str) -> User:
    fake_db = {
        "testuser": User(username="testuser", password="testpassword")  # 明文密码
    }
    return fake_db.get(username)
