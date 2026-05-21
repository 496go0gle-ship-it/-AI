from pydantic import BaseModel, Field
from typing import List, Optional

class ExerciseHistory(BaseModel):
    genre: str = Field(..., description="問題のジャンル（例：数学/二次関数）")
    difficulty: float = Field(..., description="問題の難易度または一般正答率（0.0〜1.0）")
    is_correct: bool = Field(..., description="生徒が正解したかどうか")
    time_spent_seconds: Optional[int] = Field(None, description="解答にかかった時間（秒）")

class ZPDRequest(BaseModel):
    student_id: str = Field(..., description="生徒のID")
    history: List[ExerciseHistory] = Field(..., description="直近N回の解答履歴")
