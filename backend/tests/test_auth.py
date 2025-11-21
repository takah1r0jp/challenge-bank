from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestUserRegistration:
    """POST /auth/register のテスト"""

    def test_register_success(self, client: TestClient, db: Session):
        """正常系: ユーザー登録が成功する"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "notification_time": "20:00",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"
        assert data["data"]["notification_time"] == "20:00"
        assert "id" in data["data"]
        assert "created_at" in data["data"]
        assert "password" not in data["data"]  # パスワードは返さない
        assert "hashed_password" not in data["data"]  # ハッシュ化されたパスワードも返さない

        # トークン検証
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert len(data["data"]["access_token"]) > 0
        
        
    def test_register_duplicate_email(self, client: TestClient, db: Session):
        """異常系: 同じメールアドレスで登録できない"""
        # 1回目の登録
        client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        # 2回目の登録（同じメールアドレス）
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password456",
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already exists" in data["error"]["message"].lower()

    def test_register_invalid_email(self, client: TestClient, db: Session):
        """異常系: 無効なメールアドレスで登録できない"""
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422  # Validation error

    def test_register_short_password(self, client: TestClient, db: Session):
        """異常系: 短いパスワードで登録できない"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",  # 8文字未満
            },
        )
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """POST /auth/login のテスト"""

    def test_login_success(self, client: TestClient, db: Session):
        """正常系: ログインが成功してトークンが返される"""
        # まずユーザーを登録
        client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        # ログイン
        response = client.post(
            "/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, db: Session):
        """異常系: 間違ったパスワードでログインできない"""
        # ユーザーを登録
        client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        # 間違ったパスワードでログイン
        response = client.post(
            "/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "incorrect" in data["error"]["message"].lower()

    def test_login_nonexistent_user(self, client: TestClient, db: Session):
        """異常系: 存在しないユーザーでログインできない"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 401


class TestGetCurrentUser:
    """GET /auth/me のテスト"""

    def test_get_me_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーの情報を取得できる"""
        # ユーザーを登録
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        
        token = register_response.json()["data"]["access_token"]

        # トークンを使って自分の情報を取得
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"
        assert "id" in data["data"]
        assert "created_at" in data["data"]
        assert "password" not in data["data"]
        assert "hashed_password" not in data["data"]

    def test_get_me_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしでアクセスできない"""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンでアクセスできない"""
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
