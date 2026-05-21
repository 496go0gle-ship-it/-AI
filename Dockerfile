FROM python:3.11-slim

WORKDIR /app

# 依存関係のコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY . .

# Render.comの環境変数対策
ENV PORT=8000
EXPOSE 8000

# サーバーの起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
