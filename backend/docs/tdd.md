TDD開発の流れ

0. 事前準備（今すぐ実行）

# 依存関係をインストール
cd backend
uv sync

# テストが実行できることを確認（まだ全て失敗します）
pytest tests/test_auth.py -v

1. 認証ユーティリティの作成（backend/auth_utils.py）

まず、パスワードハッシュ化とJWT関連の関数を作成します。

実装するべき関数:
- get_password_hash(password: str) -> str - パスワードのハッシュ化
- verify_password(plain_password: str, hashed_password: str) -> bool - パスワード検証
- create_access_token(data: dict) -> str - JWTトークン生成
- decode_access_token(token: str) -> dict | None - JWTトークン検証

必要な設定:
SECRET_KEY = "your-secret-key-here"  # 本番では環境変数から読み込む
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

2. レスポンススキーマの追加（backend/schemas.py）

既存のschemas.pyに以下を追加:

class Token(BaseModel):
    """ログイン時のトークンレスポンス"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """トークンに含まれるデータ"""
    email: str | None = None

3. main.pyの準備

from fastapi import FastAPI

app = FastAPI(title="Failure Bank API")

# auth.pyからルーターをインポートして追加
from auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

4. 認証エンドポイントの実装（backend/auth.py）

開発する順番（TDDサイクル）:

ステップ1: POST /auth/register（ユーザー登録）

1. テストを実行 → 失敗を確認
pytest tests/test_auth.py::TestUserRegistration::test_register_success -v
2. 実装する内容:
- APIRouterを作成
- /register エンドポイントを作成
- パスワードをハッシュ化してDBに保存
- UserResponseを返す（status_code=201）
3. テストを実行 → 成功を確認
4. 他の異常系テストも実行
pytest tests/test_auth.py::TestUserRegistration -v

ステップ2: POST /auth/login（ログイン）

1. テストを実行 → 失敗を確認
pytest tests/test_auth.py::TestUserLogin::test_login_success -v
2. 実装する内容:
- /login エンドポイントを作成
- メールアドレスでユーザーを検索
- パスワードを検証
- JWTトークンを生成して返す
3. テストを実行 → 成功を確認
4. 他の異常系テストも実行
pytest tests/test_auth.py::TestUserLogin -v

ステップ3: GET /auth/me（ユーザー情報取得）

1. テストを実行 → 失敗を確認
pytest tests/test_auth.py::TestGetCurrentUser::test_get_me_success -v
2. 実装する内容:
- 認証依存関数を作成 get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))
- /me エンドポイントを作成
- トークンから現在のユーザーを取得して返す
3. テストを実行 → 成功を確認
4. 他の異常系テストも実行
pytest tests/test_auth.py::TestGetCurrentUser -v

5. 全テストの実行

pytest tests/test_auth.py -v

全て成功したら完成です！

---
TDDのポイント

1. Red → Green → Refactor のサイクルを守る
- Red: テストを書いて失敗させる
- Green: 最小限の実装でテストを通す
- Refactor: コードを整理する
2. 一度に1つのテストだけ実装する
- 焦らず、1つずつクリアしていく
3. テストが失敗する理由を確認する
- エラーメッセージを読んで、何が必要か理解する

実装時の参考情報

- PasslibでBcryptを使う: from passlib.context import CryptContext
- FastAPIのOAuth2: from fastapi.security import OAuth2PasswordBearer
- JWT生成: from jose import JWTError, jwt

質問があればいつでも聞いてください！

⏺ 準備完了です！以下のファイルを作成しました:

作成したファイル:
- backend/tests/conftest.py - テスト用の設定とフィクスチャ
- backend/tests/test_auth.py - 認証API用の包括的なテスト（正常系・異常系）
- backend/pyproject.toml - 認証とテストに必要な依存関係を追加

これから実装していただくファイル（順番通り）:
1. backend/auth_utils.py - パスワードハッシュ化とJWT関連の関数
2. backend/schemas.py - TokenとTokenDataスキーマを追加
3. backend/main.py - FastAPIアプリケーションの設定
4. backend/auth.py - 認証エンドポイント（register → login → me の順）

まずは uv sync で依存関係をインストールしてから、pytest tests/test_auth.py -v
でテストが失敗することを確認してスタートしてください！

質問があればいつでもどうぞ。頑張ってください！