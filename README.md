# 伴走型AIチューター ZPD推論エンジン (FastAPI)

生徒の学習履歴を分析し、「発達の最近接領域（ZPD）」を特定して、次に解くべき最適な問題や学習アクションを提示する「伴走型AIチューターモデル」のバックエンドAPIです。
LLM（Gemini API）の推論能力を活用し、学習者の現在地に最適な問題を動的に生成します。

## 機能

*   生徒の直近の学習履歴（正誤、難易度、ジャンル等）に基づくZPDの定量的計算。
*   計算されたZPD情報に基づく、Gemini APIによるパーソナライズされた問題の自動生成。
*   厳密なJSON Schemaに基づく安定したレスポンス出力（Structured Outputs）。

## セットアップと起動方法

### 前提条件
*   Python 3.9以上
*   Google Gemini API キー (Google AI Studioにて取得可能)

### 1. リポジトリのクローンと環境構築

```bash
git clone <your-repository-url>
cd <your-repository-name>

# 仮想環境の作成とアクティベート
python3 -m venv .venv
source .venv/bin/activate  # Windowsの場合は `.venv\Scripts\activate`

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を記述してください。

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
TUTOR_API_KEY=my-secret-key-123
```

> **Note:** `.env` ファイルはGitの管理対象外(`.gitignore`)になっているため、コミットされません。

### 3. ローカルサーバーの起動

```bash
uvicorn main:app --reload
```
サーバーが起動したら、ブラウザで [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) にアクセスすると、Swagger UI（API仕様書とテスト画面）を確認できます。

## API仕様

### エンドポイント
`POST /api/v1/tutor/recommend`

### 認証
ヘッダーに `X-API-Key` を付与してリクエストを送信してください。
例: `X-API-Key: my-secret-key-123`

### リクエストボディ (JSON)
生徒の直近の解答履歴を配列で渡します。

```json
{
  "student_id": "student_001",
  "history": [
    {
      "genre": "数学/二次方程式",
      "difficulty": 0.8,
      "is_correct": false,
      "time_spent_seconds": 120
    },
    {
      "genre": "数学/平方完成",
      "difficulty": 0.6,
      "is_correct": true,
      "time_spent_seconds": 60
    }
  ]
}
```

### レスポンス (JSON)
ZPDに基づき生成された最適な問題とアドバイスが返されます。

```json
{
  "target_genre": "数学/二次方程式",
  "recommended_question": "次の二次方程式を解きなさい: x^2 - 4x + 4 = 0",
  "explanation": "因数分解の公式 (a-b)^2 = a^2 - 2ab + b^2 を利用します。",
  "learning_advice": "平方完成の基礎はできているので、二次方程式の因数分解に挑戦しましょう！",
  "rationale": "ジャンル '数学/二次方程式' の本人の正答率は 0.0% であり、最適な挑戦領域(ZPD)と判定しました。"
}
```
