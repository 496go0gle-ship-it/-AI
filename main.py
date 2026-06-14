from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from api.routes import router as tutor_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)  # IPごとに数える
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="伴走型AIチューター ZPD推論エンジン",
    description="生徒の学習履歴からZPDを特定し、次に解くべき問題を提示するAPI",
    version="1.0.0"
)

# CORS設定（フロントエンドからの呼び出しを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-tutor-web-10ku.onrender.com"],  # ← ["*"] から自分のドメインに
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(tutor_router, prefix="/api/v1/tutor", tags=["Tutor"])

# フロントエンドの静的ファイル配信設定
# staticディレクトリが存在するか確認してからマウントする
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    """ルートURLにアクセスした際にフロントエンドのHTMLを返す"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Frontend not found. Please create static/index.html"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
