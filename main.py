from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes import router as tutor_router

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
    allow_origins=["*"],  # 本番環境では特定のドメインに絞る
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(tutor_router, prefix="/api/v1/tutor", tags=["Tutor"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
