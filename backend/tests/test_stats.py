"""統計エンドポイントのテスト"""

from datetime import datetime, timedelta, timezone


def test_get_stats_summary_success(client, auth_token):
    """GET /stats/summary - 正常系: 統計情報を取得できる"""
    # 失敗記録を3件作成
    for i in range(3):
        client.post(
            "/failures",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"content": f"失敗{i + 1}", "score": i + 1},
        )

    response = client.get("/stats/summary", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # 全期間の統計
    assert data["data"]["all_time"]["failure_count"] == 3
    assert data["data"]["all_time"]["total_score"] == 6  # 1 + 2 + 3
    assert data["data"]["all_time"]["average_score"] == 2.0  # 6 / 3

    # 今週の統計（今日作成したので同じ）
    assert data["data"]["this_week"]["failure_count"] == 3
    assert data["data"]["this_week"]["total_score"] == 6
    assert data["data"]["this_week"]["average_score"] == 2.0

    # 今月の統計（今日作成したので同じ）
    assert data["data"]["this_month"]["failure_count"] == 3
    assert data["data"]["this_month"]["total_score"] == 6
    assert data["data"]["this_month"]["average_score"] == 2.0

    assert "message" in data


def test_get_stats_summary_no_failures(client, auth_token):
    """GET /stats/summary - 正常系: 失敗記録がない場合"""
    response = client.get("/stats/summary", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # 全期間
    assert data["data"]["all_time"]["failure_count"] == 0
    assert data["data"]["all_time"]["total_score"] == 0
    assert data["data"]["all_time"]["average_score"] == 0.0

    # 今週
    assert data["data"]["this_week"]["failure_count"] == 0
    assert data["data"]["this_week"]["total_score"] == 0
    assert data["data"]["this_week"]["average_score"] == 0.0

    # 今月
    assert data["data"]["this_month"]["failure_count"] == 0
    assert data["data"]["this_month"]["total_score"] == 0
    assert data["data"]["this_month"]["average_score"] == 0.0


def test_get_stats_summary_no_token(client):
    """GET /stats/summary - 異常系: 認証トークンなし"""
    response = client.get("/stats/summary")

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_get_stats_summary_invalid_token(client):
    """GET /stats/summary - 異常系: 無効な認証トークン"""
    response = client.get("/stats/summary", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_get_stats_summary_user_isolation(client, auth_token):
    """GET /stats/summary - 正常系: ユーザー間のデータ分離"""
    # 現在のユーザーの失敗記録を作成
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "失敗1", "score": 5},
    )

    # 別のユーザーを作成してログイン
    client.post(
        "/auth/register",
        json={"email": "another@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "another@example.com", "password": "password123"},
    )
    another_token = login_response.json()["data"]["access_token"]

    # 別のユーザーの失敗記録を作成
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {another_token}"},
        json={"content": "失敗2", "score": 10},
    )

    # 最初のユーザーの統計を取得
    response = client.get("/stats/summary", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["all_time"]["failure_count"] == 1
    assert data["data"]["all_time"]["total_score"] == 5
    assert data["data"]["all_time"]["average_score"] == 5.0


def test_get_stats_summary_multiple_failures(client, auth_token):
    """GET /stats/summary - 正常系: 複数の失敗記録がある場合の合計計算"""
    # 様々なスコアの失敗記録を作成
    scores = [1, 2, 3, 4, 5]
    for score in scores:
        client.post(
            "/failures",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"content": f"失敗{score}", "score": score},
        )

    response = client.get("/stats/summary", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["all_time"]["failure_count"] == 5
    assert data["data"]["all_time"]["total_score"] == 15  # 1 + 2 + 3 + 4 + 5
    assert data["data"]["all_time"]["average_score"] == 3.0  # 15 / 5


# ====== Calendar Tests ======


def test_get_calendar_success(client, auth_token):
    """GET /stats/calendar - 正常系: カレンダーデータを取得できる"""
    # 失敗記録を作成（2024年1月）
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "失敗1", "score": 3},
    )
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "失敗2", "score": 5},
    )

    # 現在の年月を取得
    now = datetime.now(timezone(timedelta(hours=9)))
    year = now.year
    month = now.month

    response = client.get(
        f"/stats/calendar?year={year}&month={month}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["year"] == year
    assert data["data"]["month"] == month
    assert len(data["data"]["days"]) == 1  # 今日のデータのみ

    # 今日のデータ
    today_data = data["data"]["days"][0]
    assert today_data["failure_count"] == 2
    assert today_data["total_score"] == 8
    assert today_data["average_score"] == 4.0
    assert "date" in today_data


def test_get_calendar_no_data(client, auth_token):
    """GET /stats/calendar - 正常系: データがない月"""
    # 未来の月を指定
    response = client.get(
        "/stats/calendar?year=2099&month=12",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["year"] == 2099
    assert data["data"]["month"] == 12
    assert data["data"]["days"] == []


def test_get_calendar_no_token(client):
    """GET /stats/calendar - 異常系: 認証トークンなし"""
    response = client.get("/stats/calendar?year=2024&month=1")

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_get_calendar_invalid_token(client):
    """GET /stats/calendar - 異常系: 無効な認証トークン"""
    response = client.get(
        "/stats/calendar?year=2024&month=1",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_get_calendar_invalid_month(client, auth_token):
    """GET /stats/calendar - 異常系: 無効な月（範囲外）"""
    # 月が0
    response = client.get(
        "/stats/calendar?year=2024&month=0",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 422

    # 月が13
    response = client.get(
        "/stats/calendar?year=2024&month=13",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 422


def test_get_calendar_user_isolation(client, auth_token):
    """GET /stats/calendar - 正常系: ユーザー間のデータ分離"""
    # 現在のユーザーの失敗記録を作成
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "失敗1", "score": 5},
    )

    # 別のユーザーを作成してログイン
    client.post(
        "/auth/register",
        json={"email": "calendar_user@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "calendar_user@example.com", "password": "password123"},
    )
    another_token = login_response.json()["data"]["access_token"]

    # 別のユーザーの失敗記録を作成
    client.post(
        "/failures",
        headers={"Authorization": f"Bearer {another_token}"},
        json={"content": "失敗2", "score": 10},
    )

    # 現在の年月を取得
    now = datetime.now(timezone(timedelta(hours=9)))
    year = now.year
    month = now.month

    # 最初のユーザーのカレンダーを取得
    response = client.get(
        f"/stats/calendar?year={year}&month={month}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["days"]) == 1
    assert data["data"]["days"][0]["failure_count"] == 1
    assert data["data"]["days"][0]["total_score"] == 5
