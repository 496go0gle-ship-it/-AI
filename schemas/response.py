from pydantic import BaseModel, Field

class NextActionRecommendation(BaseModel):
    target_genre: str = Field(..., description="次に学習すべき最適なジャンル")
    recommended_question: str = Field(..., description="生成された最適な問題文")
    explanation: str = Field(..., description="問題の解説またはヒント")
    learning_advice: str = Field(..., description="生徒に対する学習アドバイス")
    rationale: str = Field(..., description="この問題を推奨した理由（ZPD判定理由）")
