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

# ポートを公開（Railwayが動的に割り当て）
EXPOSE 8000

# 本番サーバーを起動（PORT環境変数を使用、デフォルト8000）
CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
