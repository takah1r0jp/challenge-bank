# 開発ガイド - Challenge Bank

このドキュメントでは、Challenge Bankをローカル環境で動かすための手順を説明します。

## 前提条件

- Node.js 20+
- Python 3.10+
- PostgreSQL
- uv (Pythonパッケージマネージャー)

## リポジトリのクローン

```bash
git clone https://github.com/takah1r0jp/challenge-bank.git
cd challenge-bank
```

## バックエンドのセットアップ

```bash
cd backend

# 依存関係のインストール
uv sync

# 環境変数を設定
export DATABASE_URL="postgresql://user:password@localhost:5432/challenge_bank"
export JWT_SECRET_KEY="your-secret-key"
export RESEND_API_KEY="your-resend-api-key"

# データベース初期化
python init_db.py

# 開発サーバー起動
uvicorn main:app --reload
```

バックエンドは `http://localhost:8000` で起動します。

### テスト実行

```bash
# 全テスト実行
pytest

# カバレッジ付き実行
pytest --cov=. --cov-report=html

# 特定のテストのみ
pytest tests/test_auth.py -v
```

### コード品質チェック

```bash
# リンター実行
ruff check .

# フォーマッター実行
ruff format .
```

## フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数を設定（.env.local）
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 開発サーバー起動
npm run dev
```

ブラウザで `http://localhost:3000` にアクセスしてください。

## 環境変数

### バックエンド

| 変数名 | 説明 |
|--------|------|
| `DATABASE_URL` | PostgreSQL接続文字列 |
| `JWT_SECRET_KEY` | JWT署名用シークレットキー |
| `RESEND_API_KEY` | メール送信用APIキー |
| `NOTIFICATION_API_KEY` | Lambda用APIキー |

### フロントエンド

| 変数名 | 説明 |
|--------|------|
| `NEXT_PUBLIC_API_URL` | バックエンドAPIのURL |

## トラブルシューティング

### データベース接続エラー

PostgreSQLが起動しているか確認してください：

```bash
# macOS (Homebrew)
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### ポートが既に使用されている

別のアプリケーションがポート8000または3000を使用している場合は、ポートを変更してください：

```bash
# バックエンド
uvicorn main:app --reload --port 8001

# フロントエンド
npm run dev -- -p 3001
```

## CI/CD

GitHub Actionsで自動テストが実行されます。詳細は `.github/workflows/ci.yml` を参照してください。

## その他のドキュメント

- [CLAUDE.md](./CLAUDE.md): 詳細な開発ドキュメント
- [README.md](./README.md): プロジェクト概要
