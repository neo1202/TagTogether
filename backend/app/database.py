from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.user_model import User
from app.models.team_model import Team, TeamMember

# 数据库连接字符串，替换为你的 PostgreSQL 配置
DATABASE_URL = "postgresql://myuser:mypassword@postgres:5432/mydb"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)
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
def get_user(db: Session, user_name: str) -> User:
    # 查询数据库中用户名对应的用户
    return db.query(User).filter(User.user_name == user_name).first()


from app.models.base import Base
Base.metadata.create_all(bind=engine)  # 创建所有表