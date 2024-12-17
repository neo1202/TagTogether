from typing import Union
from fastapi import FastAPI
from app.api import auth, user, team, post  # 確保從 app 根開始，已經從docker compose設定絕對路徑起點
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的前端地址，可設為 ["http://127.0.0.1:5500"] 等具體地址
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 頭部
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 加載路由
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(post.router, prefix="/post", tags=["Post"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(team.router, prefix="/team", tags=["Team"])
