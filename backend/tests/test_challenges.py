"""
挑戦記録（Challenge）エンドポイントのテストコード

TDDアプローチ:
1. Red: テストを書く（挑戦する）
2. Green: 実装してテストを通す
3. Refactor: コードを改善する
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestCreateChallenge:
    """POST /challenges のテスト"""

    def test_create_challenge_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーが挑戦記録を作成できる"""
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
        response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "プレゼンで緊張して早口になってしまった",
                "score": 3,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["content"] == "プレゼンで緊張して早口になってしまった"
        assert data["data"]["score"] == 3
        assert "id" in data["data"]
        assert "user_id" in data["data"]
        assert "created_at" in data["data"]
        assert data["message"] == "Challenge record created successfully."

    def test_create_challenge_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで挑戦記録を作成できない"""
        response = client.post(
            "/challenges",
            json={
                "content": "テスト挑戦",
                "score": 1,
            },
        )
        assert response.status_code == 401

    def test_create_challenge_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで挑戦記録を作成できない"""
        response = client.post(
            "/challenges",
            headers={"Authorization": "Bearer invalid_token"},
            json={
                "content": "テスト挑戦",
                "score": 1,
            },
        )
        assert response.status_code == 401

    def test_create_challenge_missing_content(self, client: TestClient, db: Session):
        """異常系: contentが空の場合エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # contentが空
        response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "",
                "score": 3,
            },
        )
        assert response.status_code == 422

    def test_create_challenge_invalid_score_too_low(self, client: TestClient, db: Session):
        """異常系: scoreが1未満の場合エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # scoreが0
        response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "テスト挑戦",
                "score": 0,
            },
        )
        assert response.status_code == 422

    def test_create_challenge_invalid_score_too_high(self, client: TestClient, db: Session):
        """異常系: scoreが5を超える場合エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # scoreが6
        response = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "テスト挑戦",
                "score": 6,
            },
        )
        assert response.status_code == 422

    def test_create_challenge_multiple_records(self, client: TestClient, db: Session):
        """正常系: 同じユーザーが複数の挑戦記録を作成できる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 1つ目の挑戦記録
        response1 = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "挑戦1",
                "score": 2,
            },
        )
        assert response1.status_code == 201

        # 2つ目の挑戦記録
        response2 = client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "挑戦2",
                "score": 4,
            },
        )
        assert response2.status_code == 201

        # それぞれ異なるIDを持つことを確認
        data1 = response1.json()["data"]
        data2 = response2.json()["data"]
        assert data1["id"] != data2["id"]
        assert data1["user_id"] == data2["user_id"]


class TestGetChallenges:
    """GET /challenges のテスト"""

    def test_get_challenges_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーの挑戦記録一覧を取得できる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 3つの挑戦記録を作成
        for i in range(3):
            client.post(
                "/challenges",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "content": f"挑戦記録{i + 1}",
                    "score": (i % 5) + 1,
                },
            )

        # 挑戦記録一覧を取得
        response = client.get(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 3
        # 新しい順（降順）で返される
        assert data["data"][0]["content"] == "挑戦記録3"
        assert data["data"][1]["content"] == "挑戦記録2"
        assert data["data"][2]["content"] == "挑戦記録1"

    def test_get_challenges_empty(self, client: TestClient, db: Session):
        """正常系: 挑戦記録がない場合は空配列を返す"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 挑戦記録一覧を取得（何も作成していない）
        response = client.get(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == []

    def test_get_challenges_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで挑戦記録一覧を取得できない"""
        response = client.get("/challenges")
        assert response.status_code == 401

    def test_get_challenges_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで挑戦記録一覧を取得できない"""
        response = client.get(
            "/challenges",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401

    def test_get_challenges_only_own_records(self, client: TestClient, db: Session):
        """正常系: 自分の挑戦記録のみ取得できる（他ユーザーの記録は見えない）"""
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

        # ユーザー1が2つの挑戦記録を作成
        client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token1}"},
            json={"content": "ユーザー1の挑戦1", "score": 3},
        )
        client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token1}"},
            json={"content": "ユーザー1の挑戦2", "score": 4},
        )

        # ユーザー2が1つの挑戦記録を作成
        client.post(
            "/challenges",
            headers={"Authorization": f"Bearer {token2}"},
            json={"content": "ユーザー2の挑戦1", "score": 2},
        )

        # ユーザー1で取得
        response1 = client.get("/challenges", headers={"Authorization": f"Bearer {token1}"})
        data1 = response1.json()
        assert len(data1["data"]) == 2
        assert all("ユーザー1" in record["content"] for record in data1["data"])

        # ユーザー2で取得
        response2 = client.get("/challenges", headers={"Authorization": f"Bearer {token2}"})
        data2 = response2.json()
        assert len(data2["data"]) == 1
        assert data2["data"][0]["content"] == "ユーザー2の挑戦1"

    def test_get_challenges_with_limit(self, client: TestClient, db: Session):
        """正常系: limitパラメータで取得件数を制限できる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 5つの挑戦記録を作成
        for i in range(5):
            client.post(
                "/challenges",
                headers={"Authorization": f"Bearer {token}"},
                json={"content": f"挑戦{i + 1}", "score": 3},
            )

        # limitを指定して取得
        response = client.get(
            "/challenges?limit=2",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2

    def test_get_challenges_with_offset(self, client: TestClient, db: Session):
        """正常系: offsetパラメータでページネーションできる"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 5つの挑戦記録を作成
        for i in range(5):
            client.post(
                "/challenges",
                headers={"Authorization": f"Bearer {token}"},
                json={"content": f"挑戦{i + 1}", "score": 3},
            )

        # offset=2で取得
        response = client.get(
            "/challenges?offset=2",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3  # 5つ中、最初の2つをスキップして3つ取得


class TestUpdateChallenge:
    """PUT /challenges/{challenge_id} のテスト"""

    def test_update_challenge_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーが自分の挑戦記録を更新できる"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # 挑戦記録を更新
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "更新されたコンテンツ",
                "score": 5,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == challenge_id
        assert data["data"]["content"] == "更新されたコンテンツ"
        assert data["data"]["score"] == 5
        assert data["message"] == "Challenge record updated successfully."

    def test_update_challenge_partial_content_only(self, client: TestClient, db: Session):
        """正常系: contentのみ更新できる"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # contentのみ更新
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "新しいコンテンツ",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["content"] == "新しいコンテンツ"
        assert data["data"]["score"] == 3  # scoreは変更されていない

    def test_update_challenge_partial_score_only(self, client: TestClient, db: Session):
        """正常系: scoreのみ更新できる"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # scoreのみ更新
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "score": 5,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["content"] == "初期コンテンツ"  # contentは変更されていない
        assert data["data"]["score"] == 5

    def test_update_challenge_not_found(self, client: TestClient, db: Session):
        """異常系: 存在しない挑戦記録を更新しようとするとエラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 存在しないIDで更新を試みる
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.put(
            f"/challenges/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "更新コンテンツ",
                "score": 4,
            },
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert data["error"]["message"] == "Challenge record not found."

    def test_update_challenge_other_user(self, client: TestClient, db: Session):
        """異常系: 他のユーザーの挑戦記録は更新できない"""
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
            json={
                "content": "ユーザー1の挑戦",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # ユーザー2が更新を試みる
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token2}"},
            json={
                "content": "悪意のある更新",
                "score": 1,
            },
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert data["error"]["message"] == "Challenge record not found."

    def test_update_challenge_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで更新できない"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.put(
            f"/challenges/{fake_id}",
            json={
                "content": "更新コンテンツ",
                "score": 4,
            },
        )
        assert response.status_code == 401

    def test_update_challenge_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで更新できない"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.put(
            f"/challenges/{fake_id}",
            headers={"Authorization": "Bearer invalid_token"},
            json={
                "content": "更新コンテンツ",
                "score": 4,
            },
        )
        assert response.status_code == 401

    def test_update_challenge_invalid_score_too_low(self, client: TestClient, db: Session):
        """異常系: scoreが1未満の場合エラー"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # scoreを0に更新しようとする
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "score": 0,
            },
        )
        assert response.status_code == 422

    def test_update_challenge_invalid_score_too_high(self, client: TestClient, db: Session):
        """異常系: scoreが5を超える場合エラー"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # scoreを6に更新しようとする
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "score": 6,
            },
        )
        assert response.status_code == 422

    def test_update_challenge_empty_content(self, client: TestClient, db: Session):
        """異常系: contentを空文字列に更新しようとするとエラー"""
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
                "content": "初期コンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # contentを空文字列に更新しようとする
        response = client.put(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": "",
            },
        )
        assert response.status_code == 422


class TestDeleteChallenge:
    """DELETE /challenges/{challenge_id} のテスト"""

    def test_delete_challenge_success(self, client: TestClient, db: Session):
        """正常系: 認証済みユーザーが自分の挑戦記録を削除できる"""
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
                "content": "削除予定のコンテンツ",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # 挑戦記録を削除
        response = client.delete(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Challenge record deleted successfully."

        # 削除後、同じIDで取得しようとすると404が返る
        get_response = client.get(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert get_response.status_code == 404

    def test_delete_challenge_not_found(self, client: TestClient, db: Session):
        """異常系: 存在しない挑戦記録を削除しようとするとエラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 存在しないIDで削除を試みる
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(
            f"/challenges/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert data["error"]["message"] == "Challenge record not found."

    def test_delete_challenge_other_user(self, client: TestClient, db: Session):
        """異常系: 他のユーザーの挑戦記録は削除できない"""
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
            json={
                "content": "ユーザー1の挑戦",
                "score": 3,
            },
        )
        challenge_id = create_response.json()["data"]["id"]

        # ユーザー2が削除を試みる
        response = client.delete(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token2}"},
        )

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert data["error"]["message"] == "Challenge record not found."

        # ユーザー1の記録は削除されていないことを確認
        get_response = client.get(
            f"/challenges/{challenge_id}",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert get_response.status_code == 200

    def test_delete_challenge_no_token(self, client: TestClient, db: Session):
        """異常系: トークンなしで削除できない"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/challenges/{fake_id}")
        assert response.status_code == 401

    def test_delete_challenge_invalid_token(self, client: TestClient, db: Session):
        """異常系: 無効なトークンで削除できない"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(
            f"/challenges/{fake_id}",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401

    def test_delete_challenge_invalid_uuid(self, client: TestClient, db: Session):
        """異常系: 無効なUUID形式の場合エラー"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 無効なUUID形式で削除を試みる
        response = client.delete(
            "/challenges/invalid-uuid",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    def test_delete_challenge_multiple_records_remain(self, client: TestClient, db: Session):
        """正常系: 複数の記録のうち1つだけ削除される"""
        # ユーザーを登録してトークンを取得
        register_response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = register_response.json()["data"]["access_token"]

        # 3つの挑戦記録を作成
        challenge_ids = []
        for i in range(3):
            create_response = client.post(
                "/challenges",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "content": f"挑戦{i + 1}",
                    "score": 3,
                },
            )
            challenge_ids.append(create_response.json()["data"]["id"])

        # 2番目の記録を削除
        delete_response = client.delete(
            f"/challenges/{challenge_ids[1]}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert delete_response.status_code == 200

        # 一覧を取得して2件残っていることを確認
        list_response = client.get(
            "/challenges",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_response.status_code == 200
        data = list_response.json()
        assert len(data["data"]) == 2
        # 削除した記録は含まれていないことを確認
        remaining_ids = [record["id"] for record in data["data"]]
        assert challenge_ids[1] not in remaining_ids
        assert challenge_ids[0] in remaining_ids
        assert challenge_ids[2] in remaining_ids
