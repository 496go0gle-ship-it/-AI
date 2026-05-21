from schemas.request import ZPDRequest
from typing import Dict, Any

def calculate_zpd(request: ZPDRequest) -> Dict[str, Any]:
    """
    直近の学習履歴からZPD（発達の最近接領域）を定量的に計算する
    """
    if not request.history:
        return {
            "target_genre": "基礎総合",
            "zpd_reasoning": "履歴がないため、まずは基礎問題からスタートします。"
        }

    # ジャンルごとに正答率と平均難易度を集計
    genre_stats = {}
    for item in request.history:
        if item.genre not in genre_stats:
            genre_stats[item.genre] = {"correct": 0, "total": 0, "difficulty_sum": 0.0}
        
        genre_stats[item.genre]["total"] += 1
        genre_stats[item.genre]["difficulty_sum"] += item.difficulty
        if item.is_correct:
            genre_stats[item.genre]["correct"] += 1

    # 各ジャンルの平均正答率と平均難易度を計算
    zpd_candidates = []
    for genre, stats in genre_stats.items():
        accuracy = stats["correct"] / stats["total"]
        avg_difficulty = stats["difficulty_sum"] / stats["total"]
        
        # ZPDの仮説: 正答率が 0% より大きく、100% 未満のジャンル、あるいは一般正答率が高いのに本人が間違えているジャンル
        # 今回の簡易ロジック:
        # 正答率が 30% 〜 70% の領域を最もZPDとして有望視する。
        # または、本人の正答率が低くても、問題の一般正答率(difficulty)が高い場合は「基礎の抜け漏れ」として優先度を上げる。
        
        # スコアリング (値が高いほどZPDとして適している)
        # 1. 50%に近いほど高いスコア (0.5 - abs(0.5 - accuracy)) * 2 -> 0〜1
        zpd_score = 1.0 - (abs(0.5 - accuracy) * 2)
        
        # 2. 全く解けなかった(0%)が、一般正答率が高い(易しい)場合はスコアを底上げ
        if accuracy == 0.0 and avg_difficulty > 0.6:
            zpd_score = 0.8
            
        zpd_candidates.append({
            "genre": genre,
            "accuracy": accuracy,
            "avg_difficulty": avg_difficulty,
            "zpd_score": zpd_score
        })
        
    # スコアで降順ソート
    zpd_candidates.sort(key=lambda x: x["zpd_score"], reverse=True)
    
    best_candidate = zpd_candidates[0]
    
    return {
        "target_genre": best_candidate["genre"],
        "zpd_reasoning": f"ジャンル '{best_candidate['genre']}' の本人の正答率は {best_candidate['accuracy']*100:.1f}% であり、最適な挑戦領域(ZPD)と判定しました。",
        "accuracy": best_candidate["accuracy"],
        "avg_difficulty": best_candidate["avg_difficulty"]
    }
