# Challenge Bank - 挑戦を貯金するアプリ

挑戦を習慣化し、成長を可視化するフルスタックWebアプリケーション

## プロジェクト概要

このプロジェクトは、ユーザーが日々の挑戦を記録・可視化し、挑戦を習慣化するためのWebアプリケーションのバックエンドです。挑戦を「貯金」として捉えることで、挑戦することへの心理的ハードルを下げ、継続的な成長をサポートします。

## フルスタック構成

### フロントエンド
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Design System**: Material Design 3 (Material You)
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI, Lucide React
- **Charts**: Recharts
- **Form Management**: React Hook Form + Zod
- **Deploy**: Vercel

### バックエンド（backend/）
- **Framework**: FastAPI 0.121.1+
- **ORM**: SQLAlchemy 2.0.44+
- **Database**: PostgreSQL
- **認証**: JWT + Argon2パスワードハッシュ（トークン有効期限: 10日）
- **Email Service**: Resend
- **Testing**: pytest + httpx (カバレッジ90%+)
- **Code Quality**: Ruff
- **Package Manager**: uv
- **Deploy**: Railway

### インフラ・通知
- **メール通知**: Resend（実装済み✅）
- **定期実行**: AWS Lambda + EventBridge（毎日、ユーザー設定時刻に実行）
- **Database Hosting**: Railway PostgreSQL
- **CI/CD**: GitHub Actions

## MVP機能

### 1. 認証機能（実装済み✅）
- メールアドレス + パスワード認証
- JWT トークンベース
- 通知時間設定（notification_time）

### 2. 挑戦の記録（実装済み✅）
ユーザーが挑戦を記録する際に以下の情報を入力：

- **挑戦内容**（テキスト）: content
- **スコア**（整数）: score
- **記録日時**（自動）: created_at
- **更新日時**（自動）: updated_at

**将来的な拡張候補:**
- challenge_content（挑戦内容）
- challenge_content（挑戦内容の詳細）
- next_action（ネクストアクション）
- challenge_level（チャレンジ度合い: 1-3）
- novelty_level（新しい度合い: 1-3）

### 3. 可視化機能（実装済み✅）
- **統計サマリー**: 全期間/今週/今月の挑戦数・スコア・平均スコア
- **カレンダービュー**: 指定月の日別統計（挑戦数、合計スコア、平均スコア）
- **週次トレンド**: 今週の挑戦をグラフで表示（Recharts使用）

### 4. 通知機能（実装済み✅）
- メール通知機能（Resend統合）
- AWS Lambda + EventBridge定期実行（毎日、ユーザー設定時刻に実行）
- 週次統計メール（HTMLテンプレート）
- バッチ送信API（`POST /notifications/send`）- APIキー認証
- テスト送信API（`POST /notifications/test`）- ユーザー認証

## 技術スタック

- **Framework**: FastAPI 0.121.1+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0.44+
- **認証**: JWT + Argon2パスワードハッシュ（トークン有効期限: 10日）
- **テスト**: pytest + httpx
- **コード品質**: Ruff
- **パッケージ管理**: uv

## プロジェクト構造

```
challenge-bank/
├── frontend/               # Next.js フロントエンド
│   ├── app/                # App Router (ルーティング)
│   ├── components/         # UIコンポーネント
│   └── lib/                # ユーティリティ (API, 認証)
├── backend/                # FastAPI バックエンド
│   ├── main.py             # APIエンドポイント
│   ├── models.py           # SQLAlchemyモデル
│   ├── schemas.py          # Pydanticスキーマ
│   ├── auth.py             # 認証ロジック
│   ├── database.py         # DB接続
│   └── tests/              # pytestテストコード
├── .github/workflows/      # GitHub Actions CI/CD
├── CLAUDE.md               # このファイル（開発ドキュメント）
├── README.md               # プロジェクト概要
└── DEVELOPMENT.md          # ローカル開発ガイド
```

## 実装状況

### ✅ 実装済み（MVP完了）
**認証機能:**
- [x] ユーザー登録（`POST /auth/register`）
- [x] ログイン（`POST /auth/login`）
- [x] 認証済みユーザー情報取得（`GET /auth/me`）
- [x] ユーザー情報更新（`PUT /auth/me`）- notification_time更新対応
- [x] ログアウト（`POST /auth/logout`）- クライアント側トークン削除方式
- [x] Userモデル（notification_time対応）
- [x] 環境変数化（JWT_SECRET_KEY, DATABASE_URL）

**挑戦記録CRUD:**
- [x] 挑戦記録作成（`POST /challenges`）
- [x] 挑戦記録一覧取得（`GET /challenges`）- ページネーション対応
- [x] 挑戦記録詳細取得（`GET /challenges/{id}`）
- [x] 挑戦記録更新（`PUT /challenges/{id}`）
- [x] 挑戦記録削除（`DELETE /challenges/{id}`）
- [x] Challengeモデル（content, score, created_at, updated_at）

**統計・可視化API:**
- [x] 統計サマリー取得（`GET /stats/summary`）- 全期間/今週/今月
- [x] カレンダーデータ取得（`GET /stats/calendar`）- 日別統計、JST対応

**通知機能:**
- [x] メール送信機能（Resend統合）
- [x] バッチ送信API（`POST /notifications/send`）- APIキー認証
- [x] テスト送信API（`POST /notifications/test`）- ユーザー認証
- [x] AWS Lambda関数（EventBridge定期実行）- 毎日、ユーザー設定時刻に実行
- [x] 週次統計メール（HTMLテンプレート対応）

**フロントエンド:**
- [x] 認証画面（ログイン・登録）
- [x] ダッシュボード（統計サマリー、週次トレンドグラフ）
- [x] 挑戦記録フォーム（作成・編集）
- [x] 挑戦一覧表示
- [x] カレンダービュー（月別表示）
- [x] ユーザー設定（通知時刻変更）
- [x] Material Design 3によるUI統一
- [x] レスポンシブデザイン

### 🚧 今後の実装予定（優先度順）
1. **フィルタリング・検索機能**
   - [ ] 日付範囲フィルタ（start_date, end_date）
   - [ ] スコア範囲フィルタ
   - [ ] ソート機能（日付順、スコア順など）

2. **タグ・カテゴリ機能**
   - [ ] 挑戦のタグ付け
   - [ ] カテゴリ別統計

3. **Challengeモデルの拡張（将来的な機能）**
   - [ ] challenge_content（挑戦内容の詳細）
   - [ ] next_action（ネクストアクション）
   - [ ] challenge_level（チャレンジ度合い: 1-3）
   - [ ] novelty_level（新しい度合い: 1-3）

## データベースモデル

### User（実装済み✅）
```python
- id: UUID (PK)
- email: String (unique)
- hashed_password: String
- notification_time: Time (nullable)  # 通知時刻（例: "20:00:00"）
- created_at: DateTime
```

### Challenge（実装済み✅）
```python
- id: UUID (PK)
- user_id: UUID (FK -> User)
- content: Text              # 挑戦内容
- score: Integer             # スコア
- created_at: DateTime       # 記録日時
- updated_at: DateTime       # 更新日時
```

**将来的な拡張候補:**
```python
- challenge_content: Text      # 挑戦内容
- challenge_content: Text        # 挑戦内容の詳細
- next_action: Text           # ネクストアクション
- challenge_level: Integer    # 1-3 (チャレンジ度合い)
- novelty_level: Integer      # 1-3 (新しい度合い)
```

## 開発ガイドライン

### 開発サイクル：TDD（Test-Driven Development）

このプロジェクトでは**テスト駆動開発（TDD）**を推奨します。

#### TDDの基本サイクル
1. **Red**: 挑戦するテストを書く
2. **Green**: テストが通る最小限のコードを書く
3. **Refactor**: コードを改善する

#### 実践例
```python
# 1. まずテストを書く（tests/test_challenges.py）
def test_create_challenge(client, auth_token):
    response = client.post(
        "/challenges",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "content": "新しい言語の環境構築で詰まった",
            "score": 5
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["content"] == "新しい言語の環境構築で詰まった"
    assert data["score"] == 5

# 2. テストが通るようにエンドポイントを実装（main.py）
@app.post("/challenges", response_model=SuccessResponse, status_code=201)
def create_challenge(
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 実装...
    pass

# 3. リファクタリング（必要に応じて）
```

#### TDDのメリット
- バグの早期発見
- リファクタリングの安全性
- 仕様の明確化（テストがドキュメントになる）
- 実装の最小化（必要な機能だけを実装）

### コーディング規約
- Python 3.10以上
- 1行の最大文字数: 100文字
- フォーマッター: Ruff（ダブルクォート、スペースインデント）
- 型ヒントを積極的に使用
- **テストファーストで開発**（TDD推奨）
- 各エンドポイントには対応するテストを作成

### 認証フロー
1. ユーザーはメールアドレスとパスワードで登録
2. ログイン時にJWTアクセストークンを発行（デフォルト有効期限: 30日）
3. 保護されたエンドポイントは`Authorization: Bearer <token>`ヘッダーで認証
4. トークンからユーザー情報を取得し、リクエストを処理

### エラーハンドリング
- 適切なHTTPステータスコードを返す
- エラーレスポンスは統一されたフォーマット（`{"detail": "error message"}`）
- カスタム例外ハンドラーで一貫性を保つ

## セットアップ

詳細なセットアップ手順は [DEVELOPMENT.md](./DEVELOPMENT.md) を参照してください。

### クイックスタート（バックエンド）

```bash
cd backend

# 依存関係のインストール
uv sync

# 環境変数を設定
export DATABASE_URL="postgresql://user:password@localhost:5432/challenge_bank"
export JWT_SECRET_KEY="your-secret-key"

# データベース初期化
python init_db.py

# 開発サーバー起動
uvicorn main:app --reload

# テスト実行
pytest

# コードフォーマット & リンター
ruff format .
ruff check .
```

### クイックスタート（フロントエンド）

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数を設定（.env.local）
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 開発サーバー起動
npm run dev
```

## API仕様

### 認証エンドポイント

#### POST /auth/register
ユーザー登録
```json
Request:
{
  "email": "user@example.com",
  "password": "password123",
  "notification_time": "20:00:00"  // optional
}

Response (201):
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00:00",
    "created_at": "2024-01-01T00:00:00",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully."
}
```

#### POST /auth/login
ログイン
```json
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (200):
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00:00",
    "created_at": "2024-01-01T00:00:00",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful."
}
```

#### GET /auth/me
認証済みユーザー情報取得（要認証）
```json
Headers:
  Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00:00",
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "User information retrieved successfully."
}
```

#### PUT /auth/me
ユーザー情報更新（要認証）
```json
Headers:
  Authorization: Bearer <token>

Request:
{
  "notification_time": "09:30"  // HH:MM形式（必須）
}

Response (200):
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "09:30",
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "User information updated successfully."
}
```

#### POST /auth/logout
ログアウト（要認証）
```json
Headers:
  Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "data": null,
  "message": "Logout successful. Please remove the token from the client."
}

Note: JWTはステートレスなため、サーバー側では何も処理しません。
クライアント側でトークンを削除することでログアウトを実現してください。
```

### 挑戦記録エンドポイント

#### POST /challenges
挑戦記録作成（要認証）
```json
Request:
{
  "content": "新しい言語の環境構築で詰まった",
  "score": 5
}

Response (201):
{
  "success": true,
  "data": {
    "id": "...",
    "user_id": "...",
    "content": "新しい言語の環境構築で詰まった",
    "score": 5,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  },
  "message": "Challenge record created successfully."
}
```

#### GET /challenges
挑戦記録一覧取得（要認証）
```json
Query Parameters:
  - limit: int (default: 20)
  - offset: int (default: 0)

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "...",
      "user_id": "...",
      "content": "...",
      "score": 5,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "message": "Challenge records retrieved successfully."
}
```

#### GET /challenges/{challenge_id}
挑戦記録詳細取得（要認証）
```json
Response (200):
{
  "success": true,
  "data": {
    "id": "...",
    "user_id": "...",
    "content": "...",
    "score": 5,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  },
  "message": "Challenge record retrieved successfully."
}
```

#### PUT /challenges/{challenge_id}
挑戦記録更新（要認証）
```json
Request:
{
  "content": "更新された内容",  // optional
  "score": 7  // optional
}

Response (200):
{
  "success": true,
  "data": {
    "id": "...",
    "user_id": "...",
    "content": "更新された内容",
    "score": 7,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-02T10:00:00"
  },
  "message": "Challenge record updated successfully."
}
```

#### DELETE /challenges/{challenge_id}
挑戦記録削除（要認証）
```json
Response (200):
{
  "success": true,
  "data": null,
  "message": "Challenge record deleted successfully."
}
```

### 統計エンドポイント

#### GET /stats/summary
統計サマリー取得（要認証）
```json
Response (200):
{
  "success": true,
  "data": {
    "all_time": {
      "challenge_count": 100,
      "total_score": 500,
      "average_score": 5.0
    },
    "this_week": {
      "challenge_count": 5,
      "total_score": 25,
      "average_score": 5.0
    },
    "this_month": {
      "challenge_count": 20,
      "total_score": 100,
      "average_score": 5.0
    }
  },
  "message": "Statistics summary retrieved successfully."
}
```

#### GET /stats/calendar
カレンダーデータ取得（要認証）
```json
Query Parameters:
  - year: int (required)
  - month: int (required, 1-12)

Response (200):
{
  "success": true,
  "data": {
    "year": 2024,
    "month": 1,
    "days": [
      {
        "date": "2024-01-15",
        "challenge_count": 3,
        "total_score": 15,
        "average_score": 5.0
      }
    ]
  },
  "message": "Calendar data retrieved successfully."
}
```

## セキュリティ

### 実装済み
- パスワードはArgon2でハッシュ化
- JWT認証による保護されたエンドポイント（トークン有効期限: 10日）
- メールアドレスのバリデーション
- notification_timeのバリデーション（HH:MM形式）
- JWTシークレットキーの環境変数化（`JWT_SECRET_KEY`）
- データベース接続URLの環境変数化（`DATABASE_URL`）

### 改善予定
- [ ] JWTリフレッシュトークン実装
- [ ] レート制限（Rate Limiting）
- [ ] CORS設定の厳密化
- [ ] 本番環境でのHTTPS必須化

## CI/CD

### GitHub Actions（設定済み✅）

`.github/workflows/ci.yml`でバックエンドの自動テストを実行しています。

#### トリガー
- `main`ブランチへのpush
- `develop`ブランチへのpush
- Pull Request作成時

#### 実行内容
1. **Ruff Linter**: コード品質チェック
2. **Ruff Formatter**: フォーマットチェック
3. **pytest**: テスト実行
4. **Coverage**: カバレッジレポート生成

#### バッジ（追加推奨）
README.mdに以下のバッジを追加すると、CI状態が一目でわかります：

```markdown
![CI](https://github.com/<username>/challenge-bank/workflows/CI/badge.svg)
```

#### ローカルでCIと同じチェックを実行
```bash
cd backend

# リンターチェック
uv run ruff check .

# フォーマットチェック
uv run ruff format --check .

# テスト実行
uv run pytest -v

# カバレッジ付きテスト
uv run pytest --cov=. --cov-report=term
```

## デプロイ

### 本番環境構成（実装済み✅）

#### バックエンド: Railway
- **PostgreSQLデータベース**: Railway PostgreSQL
- **FastAPI**: Railway Webサービス
- **環境変数**:
  - `DATABASE_URL`: PostgreSQL接続文字列
  - `JWT_SECRET_KEY`: JWT署名用シークレットキー
  - `RESEND_API_KEY`: メール送信用APIキー
  - `NOTIFICATION_API_KEY`: Lambda用APIキー
- **ビルドコマンド**: `uv sync`
- **起動コマンド**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **自動デプロイ**: GitHubの`main`ブランチへのpush時

#### フロントエンド: Vercel
- **Next.js**: Vercelにデプロイ
- **環境変数**:
  - `NEXT_PUBLIC_API_URL`: バックエンドAPIのURL
- **自動デプロイ**: GitHubの`main`ブランチへのpush時

#### 通知: AWS Lambda + EventBridge
- **Lambda関数**: Python 3.10ランタイム
- **トリガー**: EventBridge（毎日、ユーザー設定時刻に実行）
- **環境変数**:
  - `BACKEND_API_URL`: バックエンドAPIのURL
  - `NOTIFICATION_API_KEY`: バッチ送信用APIキー

## テスト

### テスト方針（TDD）
このプロジェクトでは**テスト駆動開発**を採用しています。

1. **テストファースト**: 実装前にテストを書く
2. **独立性**: 各テストは独立して実行可能
3. **テストDB**: テストは独立したSQLiteデータベースを使用
4. **認証テスト**: 保護されたエンドポイントはテストユーザーで認証
5. **カバレッジ**: コードカバレッジを定期的に確認

### テスト実行
```bash
# 全テスト実行
pytest

# カバレッジ付き実行
pytest --cov=. --cov-report=html

# 特定のテストファイルのみ
pytest tests/test_auth.py

# ウォッチモード（ファイル変更を監視）
pytest-watch
```

### テスト構成
```
backend/tests/
├── conftest.py           # テストフィクスチャ
├── test_auth.py          # 認証エンドポイントのテスト（実装済み）
├── test_challenges.py      # 挑戦記録エンドポイントのテスト（実装済み）
└── test_stats.py         # 統計エンドポイントのテスト（実装済み）
```

## 今後の改善・拡張アイデア

### Phase 2（次の優先機能）
- [ ] **フィルタリング・検索機能**: 日付範囲、スコア範囲での絞り込み
- [ ] **タグ機能**: 挑戦をカテゴリ分けして整理、カテゴリ別統計
- [ ] **目標設定機能**: 週間・月間目標を設定し、達成度を可視化
- [ ] **エクスポート機能**: CSV/JSON形式でデータをエクスポート
- [ ] **パスワード変更機能**: 現在のパスワード確認後に変更
- [ ] **パスワードリセット機能**: メール送信による再設定

### Phase 3（長期的な拡張）
- [ ] **ソーシャル機能**: 挑戦をコミュニティで共有
- [ ] **AI分析**: 挑戦パターンの分析、アドバイス生成
- [ ] **バッジ・報酬システム**: ゲーミフィケーション要素の追加
- [ ] **モバイルアプリ**: React Native / Flutterでのネイティブアプリ開発
- [ ] **他サービス連携**: Notion、Slack、Discord等との統合

## 参考リンク

### バックエンド
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [JWT公式サイト](https://jwt.io/)
- [pytest公式ドキュメント](https://docs.pytest.org/)

### フロントエンド
- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [Material Design 3](https://m3.material.io/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/)

### インフラ
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**最終更新**: 2024年
**Note**: このドキュメントはプロジェクトの進行に合わせて随時更新してください。
