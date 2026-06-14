from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi import Request
import os

from schemas.request import ZPDRequest
from schemas.response import NextActionRecommendation
from services.zpd_service import calculate_zpd
from services.llm_service import generate_next_question

from limiter import limiter


router = APIRouter()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    expected_api_key = os.environ.get("TUTOR_API_KEY", "default-dev-key")
    if api_key_header == expected_api_key:
        return api_key_header
    raise HTTPException(
        status_code=403, detail="Could not validate API Key"
    )

@router.post("/recommend", response_model=NextActionRecommendation)
@limiter.limit("10/minute")
async def recommend_next_action(
    request: Request,        # ← slowapiが名前で探す本物のRequest（この名前必須）
    payload: ZPDRequest,     # ← リクエストボディ（生徒の解答履歴）
):
    # 1. ZPDの計算
    zpd_info = calculate_zpd(payload)

    # 2. 学習履歴のサマリーテキスト作成（LLMのプロンプト用）
    history_summary = "直近の解答履歴:\n"
    for item in payload.history:
        status = "正解" if item.is_correct else "不正解"
        history_summary += f"- ジャンル: {item.genre}, 難易度: {item.difficulty}, 結果: {status}\n"

    # 3. LLMによる問題生成
    recommendation = generate_next_question(zpd_info, history_summary)

    return recommendation