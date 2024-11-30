from app.models.user_model import User

# 模擬一個假數據庫查詢函數
def get_user(username: str) -> User:
    fake_db = {
        "testuser": User(username="testuser", password_hash="$2b$12$wBdnbBp8eWdTZR68KAEV.O/Z8yuv9y3QQI/bCMKvoDnOgiOw.OFOa") # 輸入用戶名 testuser 和密碼 testpassword
    }
    return fake_db.get(username)
