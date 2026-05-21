import os
import json
from google import genai
from google.genai import types
from schemas.response import NextActionRecommendation
from typing import Dict, Any

# Get API key from environment variable or raise error if not set
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_next_question(zpd_info: Dict[str, Any], history_summary: str) -> NextActionRecommendation:
    """
    Gemini APIを呼び出して、ZPD情報に基づき次に解くべき問題を生成する
    """
    if not GEMINI_API_KEY:
        # 開発用のモック応答（APIキー未設定時）
        return NextActionRecommendation(
            target_genre=zpd_info.get("target_genre", "不明"),
            recommended_question="【APIキー未設定のためモック問題】 次の二次方程式を解きなさい: x^2 - 4x + 4 = 0",
            explanation="因数分解の公式 (a-b)^2 = a^2 - 2ab + b^2 を利用します。",
            learning_advice="APIキーを設定して、Geminiによる動的生成を有効にしましょう！",
            rationale=zpd_info.get("zpd_reasoning", "モック推論")
        )

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
あなたはプロの個別指導塾のAI講師です。生徒の学習履歴と、システムが判定した最適な学習領域(ZPD)に基づいて、
次に生徒が解くべきオリジナルの問題を1問作成し、解説と学習アドバイスを提供してください。

【システム判定によるZPD（発達の最近接領域）情報】
ターゲットジャンル: {zpd_info.get('target_genre')}
判定理由: {zpd_info.get('zpd_reasoning')}

【生徒の直近の学習状況サマリー】
{history_summary}

【指示】
・ターゲットジャンルに基づいた、少しだけひねりを加えたが自力で解けそうな問題を生成してください。
・JSONフォーマットで厳密に出力してください。
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=NextActionRecommendation,
            temperature=0.7,
        ),
    )
    
    # Parse JSON
    try:
        data = json.loads(response.text)
        return NextActionRecommendation(**data)
    except Exception as e:
        # JSONパースエラー時のフォールバック
        return NextActionRecommendation(
            target_genre=zpd_info.get("target_genre", "エラー"),
            recommended_question="問題の生成に失敗しました。",
            explanation="パースエラー",
            learning_advice="もう一度やり直してください。",
            rationale=f"Error: {str(e)}"
        )
