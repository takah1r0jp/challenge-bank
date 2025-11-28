import sys
from datetime import datetime, timedelta, timezone

from models import Challenge, User


def test_get_users_for_notification_jst_20(db):
    """指定JST時刻(20時台)のユーザーを取得できる"""
    # テスト用ユーザー作成
    u1 = User(email="u1@example.com", hashed_password="x", notification_time="20:00")
    u2 = User(email="u2@example.com", hashed_password="x", notification_time="20:30")
    u3 = User(email="u3@example.com", hashed_password="x", notification_time="19:00")

    db.add_all([u1, u2, u3])
    db.commit()

    from email_service import get_users_for_notification

    users = get_users_for_notification(db, 20)

    emails = {u.email for u in users}

    assert "u1@example.com" in emails
    assert "u2@example.com" in emails
    assert "u3@example.com" not in emails


def test_get_weekly_stats(db):
    """週次統計を正しく計算できる"""
    # ユーザーと挑戦記録をセットアップ
    user = User(email="weekly@example.com", hashed_password="x")
    db.add(user)
    db.commit()

    # JSTの週開始を計算し、UTCに変換した値を基準に作成日時を用意する
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst)
    week_start_jst = now_jst - timedelta(days=now_jst.weekday())
    week_start_jst = week_start_jst.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start_utc = week_start_jst.astimezone(timezone.utc).replace(tzinfo=None)

    # 週の範囲に入る挑戦
    c1 = Challenge(
        user_id=user.id, content="in_week", score=3, created_at=week_start_utc + timedelta(days=1)
    )

    # 週の範囲に入らない挑戦
    c2 = Challenge(
        user_id=user.id,
        content="before_week",
        score=5,
        created_at=week_start_utc - timedelta(days=1),
    )

    db.add_all([c1, c2])
    db.commit()

    from email_service import get_weekly_stats

    stats = get_weekly_stats(db, user.id)

    assert stats["challenge_count"] == 1
    assert stats["total_score"] == 3
    # average_score should be float
    assert isinstance(stats["average_score"], float)


def test_send_notification_email_success(monkeypatch, db, tmp_path):
    """Resendの送信が成功した場合Trueを返す"""
    # 簡易ユーザー
    user = User(email="send@example.com", hashed_password="x")
    db.add(user)
    db.commit()

    # モック統計
    stats = {
        "challenge_count": 2,
        "total_score": 7,
        "average_score": 3.5,
        "week_start": "2025/01/01",
        "week_end": "2025/01/07",
    }

    # 環境変数はテスト用にセット
    monkeypatch.setenv("RESEND_API_KEY", "test_api_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@example.com")
    monkeypatch.setenv("APP_URL", "https://example.com")

    # sys.modulesに簡易resendモックを差し込む
    class DummyEmails:
        def send(self, **kwargs):
            return {"id": "msg_123"}

    class DummyResend:
        Emails = DummyEmails

    monkeypatch.setitem(sys.modules, "resend", DummyResend())

    from email_service import send_notification_email

    result = send_notification_email(user, stats)

    assert result is True


# ====== API Key 認証テスト ======


def test_send_endpoint_unauthorized_no_key(client):
    """API KeyなしでリクエストするとUnauthorized"""
    response = client.post("/notifications/send")
    assert response.status_code == 403


def test_send_endpoint_unauthorized_invalid_key(client, monkeypatch):
    """無効なAPI KeyでリクエストするとUnauthorized"""
    monkeypatch.setenv("NOTIFICATION_API_KEY", "valid_key_123")
    response = client.post(
        "/notifications/send",
        headers={"X-API-Key": "invalid_key"},
    )
    assert response.status_code == 403


def test_send_endpoint_with_valid_api_key(client, monkeypatch, db):
    """有効なAPI Keyでリクエストするとバッチ処理が実行される"""
    monkeypatch.setenv("NOTIFICATION_API_KEY", "valid_key_123")

    response = client.post(
        "/notifications/send",
        headers={"X-API-Key": "valid_key_123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["total_users"] == 0  # テストDBにはユーザーなし
    assert data["data"]["emails_sent"] == 0
    assert data["message"] == "Notification batch completed."


def test_send_endpoint_success(client, monkeypatch, db):
    """複数のユーザーがいる場合、バッチ処理が正常に実行される"""
    monkeypatch.setenv("NOTIFICATION_API_KEY", "test_key_123")
    monkeypatch.setenv("RESEND_API_KEY", "resend_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@test.com")
    monkeypatch.setenv("APP_URL", "https://test.com")

    # Resendモック
    class DummyEmails:
        def send(self, **kwargs):
            return {"id": "msg_test"}

    class DummyResend:
        Emails = DummyEmails

    monkeypatch.setitem(sys.modules, "resend", DummyResend())

    # 現在のJST時刻を取得（時間部分）
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst)
    current_hour = now_jst.hour

    # 現在の時刻に対応するユーザーを2人作成
    hour_str = f"{current_hour:02d}:00"
    u1 = User(email="send_test1@example.com", hashed_password="x", notification_time=hour_str)
    u2 = User(email="send_test2@example.com", hashed_password="x", notification_time=hour_str)

    db.add_all([u1, u2])
    db.commit()

    response = client.post(
        "/notifications/send",
        headers={"X-API-Key": "test_key_123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_users"] == 2
    assert data["data"]["emails_sent"] == 2
    assert data["data"]["emails_failed"] == 0
    assert data["data"]["current_hour_jst"] == current_hour
    assert data["message"] == "Notification batch completed."


def test_send_endpoint_no_users(client, monkeypatch):
    """対象ユーザーがいない場合、バッチ処理は正常に完了する"""
    monkeypatch.setenv("NOTIFICATION_API_KEY", "test_key_123")

    response = client.post(
        "/notifications/send",
        headers={"X-API-Key": "test_key_123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_users"] == 0
    assert data["data"]["emails_sent"] == 0
    assert data["data"]["emails_failed"] == 0
    assert "current_hour_jst" in data["data"]
    assert data["message"] == "Notification batch completed."


def test_test_endpoint_success(client, monkeypatch, db, auth_token):
    """認証済みユーザーがテストメールを送信できる"""
    monkeypatch.setenv("RESEND_API_KEY", "resend_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@test.com")
    monkeypatch.setenv("APP_URL", "https://test.com")

    # Resendモック
    class DummyEmails:
        def send(self, **kwargs):
            return {"id": "msg_test"}

    class DummyResend:
        Emails = DummyEmails

    monkeypatch.setitem(sys.modules, "resend", DummyResend())

    response = client.post(
        "/notifications/test",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["email"] == "test@example.com"
    assert "sent_at" in data["data"]
    assert data["message"] == "Test notification email sent successfully."


# ====== 統合テスト ======


def test_send_notification_batch_integration(client, monkeypatch, db):
    """バッチ送信の統合テスト - ユーザーと挑戦記録を含めた全体フロー"""
    monkeypatch.setenv("NOTIFICATION_API_KEY", "integration_test_key")
    monkeypatch.setenv("RESEND_API_KEY", "resend_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@test.com")
    monkeypatch.setenv("APP_URL", "https://test.com")

    # Resendモック
    sent_emails = []

    class DummyEmails:
        def send(self, **kwargs):
            sent_emails.append(kwargs)
            return {"id": "msg_integration"}

    class DummyResend:
        Emails = DummyEmails

    monkeypatch.setitem(sys.modules, "resend", DummyResend())

    # テストデータ準備
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst)
    current_hour = now_jst.hour
    hour_str = f"{current_hour:02d}:00"

    # 複数ユーザーを作成
    u1 = User(email="integration1@example.com", hashed_password="x", notification_time=hour_str)
    u2 = User(email="integration2@example.com", hashed_password="x", notification_time=hour_str)
    u3 = User(
        email="integration3@example.com", hashed_password="x", notification_time="19:00"
    )  # 別時刻

    db.add_all([u1, u2, u3])
    db.commit()

    # u1, u2に挑戦記録を作成（現在の週の範囲内）
    week_start_jst = now_jst - timedelta(days=now_jst.weekday())
    week_start_jst = week_start_jst.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start_utc = week_start_jst.astimezone(timezone.utc).replace(tzinfo=None)

    c1 = Challenge(
        user_id=u1.id,
        content="integration_challenge_1",
        score=4,
        created_at=week_start_utc + timedelta(days=2),
    )
    c2 = Challenge(
        user_id=u1.id,
        content="integration_challenge_2",
        score=3,
        created_at=week_start_utc + timedelta(days=3),
    )
    c3 = Challenge(
        user_id=u2.id,
        content="integration_challenge_3",
        score=5,
        created_at=week_start_utc + timedelta(days=1),
    )

    db.add_all([c1, c2, c3])
    db.commit()

    # バッチ送信エンドポイントを呼び出し
    response = client.post(
        "/notifications/send",
        headers={"X-API-Key": "integration_test_key"},
    )

    assert response.status_code == 200
    data = response.json()

    # レスポンス検証
    assert data["success"] is True
    assert data["message"] == "Notification batch completed."

    # バッチ結果を検証
    assert data["data"]["total_users"] == 2  # 現在の時刻に対応するユーザー（u1, u2）
    assert data["data"]["emails_sent"] == 2  # 両方とも送信成功
    assert data["data"]["emails_failed"] == 0
    assert data["data"]["current_hour_jst"] == current_hour
    assert len(data["data"]["failed_emails"]) == 0

    # Resendに実際に送信されたメールをチェック
    assert len(sent_emails) == 2

    # メール内容を確認
    email_1 = sent_emails[0]
    assert email_1["to"] == ["integration1@example.com"]
    assert email_1["subject"] == "今日も挑戦を記録しましょう！"
    # HTMLメール形式
    assert "html" in email_1 or "text" in email_1

    email_2 = sent_emails[1]
    assert email_2["to"] == ["integration2@example.com"]
    assert email_2["subject"] == "今日も挑戦を記録しましょう！"
