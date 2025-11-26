# Python 3.10以上の軽量イメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システム依存パッケージをインストール（PostgreSQL接続用）
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# uvをインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 依存関係ファイルをコピー
COPY pyproject.toml uv.lock ./

# 依存関係をインストール
RUN uv sync --frozen

# アプリケーションコードをコピー（ボリュームマウントするが、初期ビルド用）
COPY . .

# ポート8000を公開
EXPOSE 8000

# 開発サーバーを起動（ホットリロード有効）
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
