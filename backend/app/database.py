# from app.models.user_model import User
# # 模擬一個假數據庫查詢函數
# def get_user(username: str) -> User:
#     fake_db = {
#         "testuser": User(username="testuser", password="testpassword")  # 明文密码
#     }
#     return fake_db.get(username)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.user_model import User

# 数据库连接字符串，替换为你的 PostgreSQL 配置
DATABASE_URL = "postgresql://myuser:mypassword@postgres_container:5432/mydb"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
# 创建数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Dependency: 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据库操作函数
def get_user(db: Session, username: str) -> User:
    # 查询数据库中用户名对应的用户
    return db.query(User).filter(User.username == username).first()


