# Failure Bank - 失敗を貯金するアプリ

挑戦を習慣化し、成長を可視化するフルスタックWebアプリケーション

## プロジェクト概要

このプロジェクトは、ユーザーが日々の失敗を記録・可視化し、挑戦を習慣化するためのWebアプリケーションのバックエンドです。失敗を「貯金」として捉えることで、挑戦することへの心理的ハードルを下げ、継続的な成長をサポートします。

## フルスタック構成

### フロントエンド
- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deploy**: Vercel

### バックエンド（backend/）
- **Framework**: FastAPI 0.121.1+
- **ORM**: SQLAlchemy 2.0.44+
- **Database**: PostgreSQL（開発環境ではSQLite）
- **認証**: JWT + Argon2パスワードハッシュ
- **Deploy**: Render / Railway

### 通知
- **メール通知**: SendGrid / Resend
- **プッシュ通知**: Web Push API（検討中）

## MVP機能（実装予定）

### 1. 失敗の記録（Core機能）
ユーザーが失敗を記録する際に以下の情報を入力：

- **挑戦内容**（テキスト）: "どんな挑戦をしたの？"
- **失敗内容**（テキスト）: "どんな失敗をしたの？"
- **ネクストアクション**（テキスト）: "次に何をする？"
- **チャレンジ度合い**（3段階）: 挑戦の難易度は高かったか？
- **新しい度合い**（3段階）: 自分にとって新しいことだったか？
- **記録日時**（自動）

### 2. 通知機能
- 毎日決まった時間にプッシュ通知/メール送信
- ユーザーが通知時間を設定可能

### 3. 可視化機能
- **累積失敗数カウンター**: "貯金"としての総数表示
- **カレンダービュー**: 記録した日に失敗数とその質を表示
- **統計グラフ**: 週/月の記録数（折れ線または棒グラフ）

### 4. 認証機能（実装済み✅）
- メールアドレス + パスワード認証
- JWT トークンベース

## 技術スタック

- **Framework**: FastAPI 0.121.1+
- **Database**: PostgreSQL（開発環境ではSQLite）
- **ORM**: SQLAlchemy 2.0.44+
- **認証**: JWT + Argon2パスワードハッシュ
- **テスト**: pytest + httpx
- **コード品質**: Ruff
- **パッケージ管理**: uv

## プロジェクト構造

```
backend/
├── main.py          # FastAPIアプリケーションとエンドポイント定義
├── models.py        # SQLAlchemyモデル（User, Failure）
├── schemas.py       # Pydanticスキーマ
├── database.py      # データベース接続設定
├── auth.py          # 認証関連のユーティリティ
├── init_db.py       # データベース初期化スクリプト
├── tests/           # テストコード
├── pyproject.toml   # プロジェクト設定
└── CLAUDE.md        # このファイル
```

## 実装状況

### ✅ 実装済み
- [x] ユーザー登録（`POST /register`）
- [x] ログイン（`POST /login`）
- [x] 認証済みユーザー情報取得（`GET /me`）
- [x] Userモデル
- [x] Failureモデル（基本構造）

### 🚧 実装予定（優先度順）
1. **失敗記録のCRUD**
   - [ ] 失敗記録作成（`POST /failures`）
   - [ ] 失敗記録一覧取得（`GET /failures`）
   - [ ] 失敗記録詳細取得（`GET /failures/{id}`）
   - [ ] 失敗記録更新（`PUT /failures/{id}`）
   - [ ] 失敗記録削除（`DELETE /failures/{id}`）

2. **Failureモデルの拡張**
   - [ ] challenge_content（挑戦内容）
   - [ ] failure_content（失敗内容）
   - [ ] next_action（ネクストアクション）
   - [ ] challenge_level（チャレンジ度合い: 1-3）
   - [ ] novelty_level（新しい度合い: 1-3）

3. **統計・可視化API**
   - [ ] 累積失敗数取得（`GET /statistics/total`）
   - [ ] カレンダーデータ取得（`GET /statistics/calendar?year=2024&month=1`）
   - [ ] 週次/月次統計（`GET /statistics/weekly`, `GET /statistics/monthly`）

4. **通知機能**
   - [ ] 通知設定モデル（NotificationSettings）
   - [ ] メール送信機能（SendGrid/Resend統合）
   - [ ] スケジューラー設定（定期実行）

5. **その他**
   - [ ] ページネーション実装
   - [ ] フィルタリング機能（日付範囲、チャレンジレベルなど）
   - [ ] ソート機能

## データベースモデル

### User
```python
- id: UUID (PK)
- email: String (unique)
- hashed_password: String
- created_at: DateTime
```

### Failure（拡張予定）
```python
- id: UUID (PK)
- user_id: UUID (FK -> User)
- challenge_content: Text      # 挑戦内容
- failure_content: Text        # 失敗内容
- next_action: Text           # ネクストアクション
- challenge_level: Integer    # 1-3 (チャレンジ度合い)
- novelty_level: Integer      # 1-3 (新しい度合い)
- created_at: DateTime        # 記録日時
- updated_at: DateTime
```

### NotificationSettings（今後追加）
```python
- id: UUID (PK)
- user_id: UUID (FK -> User)
- notification_time: Time     # 通知時刻
- notification_enabled: Boolean
- notification_method: Enum   # email, push, both
- timezone: String
```

## 開発ガイドライン

### 開発サイクル：TDD（Test-Driven Development）

このプロジェクトでは**テスト駆動開発（TDD）**を推奨します。

#### TDDの基本サイクル
1. **Red**: 失敗するテストを書く
2. **Green**: テストが通る最小限のコードを書く
3. **Refactor**: コードを改善する

#### 実践例
```python
# 1. まずテストを書く（tests/test_failures.py）
def test_create_failure(client, auth_token):
    response = client.post(
        "/failures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "challenge_content": "新しい言語を学ぶ",
            "failure_content": "環境構築で詰まった",
            "next_action": "公式ドキュメントを読む",
            "challenge_level": 2,
            "novelty_level": 3
        }
    )
    assert response.status_code == 201
    assert response.json()["challenge_content"] == "新しい言語を学ぶ"

# 2. テストが通るようにエンドポイントを実装（main.py）
@app.post("/failures", response_model=FailureResponse, status_code=201)
async def create_failure(failure: FailureCreate, current_user: User = Depends(get_current_user)):
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

```bash
# 依存関係のインストール
uv sync

# データベース初期化
python init_db.py

# 開発サーバー起動
uvicorn main:app --reload

# テスト実行
pytest

# コードフォーマット
ruff format .

# リンター実行
ruff check .
```

## API仕様

### 認証エンドポイント

#### POST /register
ユーザー登録
```json
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (201):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### POST /login
ログイン
```json
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### GET /me
認証済みユーザー情報取得（要認証）
```
Headers:
  Authorization: Bearer <token>

Response (200):
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

### 失敗記録エンドポイント（実装予定）

#### POST /failures
失敗記録作成（要認証）
```json
Request:
{
  "challenge_content": "新しいプログラミング言語でWebアプリを作る",
  "failure_content": "環境構築でつまずいて1日溶かした",
  "next_action": "公式ドキュメントを最初から読み直す",
  "challenge_level": 3,
  "novelty_level": 3
}

Response (201):
{
  "id": "...",
  "user_id": "...",
  "challenge_content": "...",
  "failure_content": "...",
  "next_action": "...",
  "challenge_level": 3,
  "novelty_level": 3,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

#### GET /failures
失敗記録一覧取得（要認証）
```
Query Parameters:
  - limit: int (default: 20)
  - offset: int (default: 0)
  - start_date: date (optional)
  - end_date: date (optional)
  - challenge_level: int (optional, 1-3)

Response (200):
{
  "total": 100,
  "items": [...]
}
```

## セキュリティ

### 実装済み
- パスワードはArgon2でハッシュ化
- JWT認証による保護されたエンドポイント
- メールアドレスのバリデーション

### 改善予定
- [ ] JWTシークレットキーを環境変数で管理（現在はハードコード）
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
![CI](https://github.com/<username>/failure-bank/workflows/CI/badge.svg)
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

### 本番環境要件
- PostgreSQLデータベース
- 環境変数設定
  - `DATABASE_URL`: PostgreSQL接続文字列
  - `JWT_SECRET_KEY`: JWT署名用シークレットキー
  - `SENDGRID_API_KEY` / `RESEND_API_KEY`: メール送信用APIキー

### Render / Railway デプロイ手順
1. GitHubリポジトリをプラットフォームに接続
2. 環境変数を設定
3. ビルドコマンド: `uv sync`
4. 起動コマンド: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### CD（継続的デプロイ）
将来的にGitHub Actionsで自動デプロイを設定可能：
- `main`ブランチへのマージ時に本番環境へ自動デプロイ
- `develop`ブランチへのマージ時にステージング環境へ自動デプロイ

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
├── test_auth.py          # 認証エンドポイントのテスト
├── test_failures.py      # 失敗記録エンドポイントのテスト（実装予定）
└── test_statistics.py    # 統計エンドポイントのテスト（実装予定）
```

## 今後の改善・拡張アイデア

### Phase 2（MVPの次）
- [ ] タグ・カテゴリ機能（失敗をカテゴリ分け）
- [ ] 検索機能（全文検索）
- [ ] エクスポート機能（CSV、JSON）
- [ ] プロフィール編集機能
- [ ] パスワードリセット機能

### Phase 3（長期的な拡張）
- [ ] ソーシャル機能（失敗の共有、コミュニティ）
- [ ] AI分析（失敗パターンの分析、アドバイス生成）
- [ ] 目標設定機能（挑戦の目標を設定）
- [ ] バッジ・報酬システム（ゲーミフィケーション）
- [ ] モバイルアプリ（React Native / Flutter）

## 参考リンク

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [JWT公式サイト](https://jwt.io/)

## ライセンス

（プロジェクトのライセンスを記載）

---

**Note**: このドキュメントはプロジェクトの進行に合わせて随時更新してください。
