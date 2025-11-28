"""
挑戦記録詳細取得（GET /challenges/{id}）エンドポイントのテストコード

TDDアプローチ:
1. Red: テストを書く（挑戦する）
2. Green: 実装してテストを通す
3. Refactor: コードを改善する
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestGetChallengeById:
    """GET /challenges/{id} のテスト"""

    def test_get_challenge_by_id_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーが自分の挑戦記録の詳細を取得できる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 挑戦記録を作成
        create_response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "プレゼンで緊張して早口になってしまった",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # 挑戦記録の詳細を取得
        response = client.get(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == challenge_id
        assert data["data"]["content"] == "プレゼンで緊張して早口になってしまった"
        assert data["data"]["score"] == 3
        assert "user_id" in data["data"]
        assert "created_at" in data["data"]
        assert data["message"] == "Challenge record retrieved successfully."

    def test_get_challenge_by_id_not_found(self, client: TestClient, db: Session):
        """異常系: 存在しないIDで404エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 存在しないIDで取得
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/challenges/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_challenge_by_id_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで401エラー"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/challenges/{fake_id}")
        assert response.status_code == 401

    def test_get_challenge_by_id_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで401エラー"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/challenges/{fake_id}",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401

    def test_get_challenge_by_id_other_user(self, client: TestClient, db: Session):
        """異常系: 他のユーザーの挑戦記録は取得できない（404エラー）"""
        # ユーザー1を登録
        register_response1 = client.post(
            "/auth/register",
            json={
                "email": "user1@example.com",
                "password": "password123",
            },
        )
        token1 = register_response1.json()["data"]["access_token"]

        # ユーザー2を登録
        register_response2 = client.post(
            "/auth/register",
            json={
                "email": "user2@example.com",
                "password": "password123",
            },
        )
        token2 = register_response2.json()["data"]["access_token"]

        # ユーザー1が挑戦記録を作成
        create_response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token1}"},
            json={"content": "ユーザー1の挑戦", "score": 3},
        )
        challenge_id = create_response.json()["data"]["id"]

        # ユーザー2がユーザー1の記録を取得しようとする
        response = client.get(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token2}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_challenge_by_id_invalid_uuid(self, client: TestClient, db: Session):
        """異常系: 無効なUUID形式で422エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 無効なUUID形式で取得
        response = client.get(
            "/challenges/invalid-uuid",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 422
