"""
失敗記録詳細取得（GET /failures/{id}）エンドポイントのテストコード

TDDアプローチ:
1. Red: テストを書く（失敗する）
2. Green: 実装してテストを通す
3. Refactor: コードを改善する
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestGetFailureById:
    """GET /failures/{id} のテスト"""

    def test_get_failure_by_id_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーが自分の失敗記録の詳細を取得できる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 失敗記録を作成
        create_response = client.post(
            "/failures",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "プレゼンで緊張して早口になってしまった",
                "score": 3,
            },
        )
        failure_id = create_response.json()["data"]["id"]

        # 失敗記録の詳細を取得
        response = client.get(
            f"/failures/{failure_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == failure_id
        assert data["data"]["content"] == "プレゼンで緊張して早口になってしまった"
        assert data["data"]["score"] == 3
        assert "user_id" in data["data"]
        assert "created_at" in data["data"]
        assert data["message"] == "Failure record retrieved successfully."

    def test_get_failure_by_id_not_found(self, client: TestClient, db: Session):
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
            f"/failures/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_failure_by_id_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで401エラー"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/failures/{fake_id}")
        assert response.status_code == 401

    def test_get_failure_by_id_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで401エラー"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/failures/{fake_id}",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401

    def test_get_failure_by_id_other_user(self, client: TestClient, db: Session):
        """異常系: 他のユーザーの失敗記録は取得できない（404エラー）"""
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

        # ユーザー1が失敗記録を作成
        create_response = client.post(
            "/failures",
            headers={"Authorization": f"Bearer {token1}"},
            json={"content": "ユーザー1の失敗", "score": 3},
        )
        failure_id = create_response.json()["data"]["id"]

        # ユーザー2がユーザー1の記録を取得しようとする
        response = client.get(
            f"/failures/{failure_id}",
            headers={"Authorization": f"Bearer {token2}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_failure_by_id_invalid_uuid(self, client: TestClient, db: Session):
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
            "/failures/invalid-uuid",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 422
