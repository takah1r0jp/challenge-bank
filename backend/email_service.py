import os
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from models import Challenge, User


def _jst_timezone() -> timezone:
    return timezone(timedelta(hours=9))


def get_users_for_notification(db: Session, hour_jst: int) -> list[User]:
    """指定されたJST時刻(0-23)に通知を希望しているユーザーを取得する

    notification_timeはHH:MM形式で保存されているため、LIKEでhour部分を絞り込む
    """
    hour_pattern = f"{hour_jst:02d}:"
    users = db.query(User).filter(User.notification_time.like(f"{hour_pattern}%")).all()
    return users


def get_weekly_stats(db: Session, user_id) -> dict[str, Any]:
    """指定ユーザーのこの週の統計を返す

    返却値は辞書で、challenge_count, total_score, average_score, week_start, week_end を含む
    week_start/week_end は JST の YYYY/MM/DD 形式を返す
    """
    jst = _jst_timezone()

    now_jst = datetime.now(jst)
    week_start_jst = now_jst - timedelta(days=now_jst.weekday())
    week_start_jst = week_start_jst.replace(hour=0, minute=0, second=0, microsecond=0)

    # 週末は週の開始から7日目の00:00 (exclusive)
    week_end_jst = week_start_jst + timedelta(days=7)

    # DB保存はUTC naiveなので、JST->UTCに変換して比較する
    week_start_utc = week_start_jst.astimezone(timezone.utc).replace(tzinfo=None)

    challenges = (
        db.query(Challenge)
        .filter(Challenge.user_id == user_id, Challenge.created_at >= week_start_utc)
        .all()
    )

    if not challenges:
        return {
            "challenge_count": 0,
            "total_score": 0,
            "average_score": 0.0,
            "week_start": week_start_jst.strftime("%Y/%m/%d"),
            "week_end": (week_end_jst - timedelta(seconds=1)).strftime("%Y/%m/%d"),
        }

    challenge_count = len(challenges)
    total_score = sum(c.score for c in challenges)
    average_score = total_score / challenge_count if challenge_count > 0 else 0.0

    return {
        "challenge_count": challenge_count,
        "total_score": total_score,
        "average_score": average_score,
        "week_start": week_start_jst.strftime("%Y/%m/%d"),
        "week_end": (week_end_jst - timedelta(seconds=1)).strftime("%Y/%m/%d"),
    }


def _load_template(template_name: str) -> str:
    """テンプレートファイルを読み込む"""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_path = os.path.join(template_dir, template_name)

    if not os.path.exists(template_path):
        return ""

    with open(template_path, encoding="utf-8") as f:
        return f.read()


def _render_template(template_content: str, context: dict[str, Any]) -> str:
    """テンプレートに変数を埋め込む（簡易テンプレートエンジン）"""
    result = template_content
    for key, value in context.items():
        placeholder = "{{ " + key + " }}"
        result = result.replace(placeholder, str(value))
    return result


def send_notification_email(user: User, stats: dict[str, Any]) -> bool:
    """ユーザーに通知メールを送信する。

    実際の送信はResend等のクライアントに委ねる。成功すればTrue、失敗または例外でFalseを返す。
    この関数はテストのために簡易なモック可能な形で実装している。
    """
    print(f"🔔 Starting email notification for {user.email}")
    try:
        # インポートを実行時に行うことでテスト時にsys.modules経由で差し替え可能にする
        import importlib

        print("📦 Importing resend module...")
        resend = importlib.import_module("resend")
        print("✅ Resend module imported successfully")

        app_url = os.getenv("APP_URL", "https://example.com")
        from_email = os.getenv("FROM_EMAIL", "noreply@example.com")

        subject = "今日も挑戦を記録しましょう！"

        # テンプレート変数の準備
        template_context = {
            "email": user.email,
            "challenge_count": stats.get("challenge_count", 0),
            "total_score": stats.get("total_score", 0),
            "average_score": f"{stats.get('average_score', 0.0):.1f}",
            "week_start": stats.get("week_start", ""),
            "week_end": stats.get("week_end", ""),
            "app_url": app_url,
        }

        # HTMLテンプレートを読み込んでレンダリング
        html_template = _load_template("notification_email.html")
        html_body = _render_template(html_template, template_context) if html_template else ""

        # テキストテンプレートを読み込んでレンダリング
        text_template = _load_template("notification_email.txt")
        text_body = _render_template(text_template, template_context) if text_template else ""

        # テンプレートが読み込めない場合はフォールバック
        if not html_body and not text_body:
            text_body = (
                f"Hi {user.email}\n\n"
                f"今週の挑戦回数: {stats.get('challenge_count', 0)}\n"
                f"合計スコア: {stats.get('total_score', 0)}\n"
                f"平均スコア: {stats.get('average_score', 0.0):.1f}\n\n"
                f"アプリへ: {app_url}\n"
            )

        # Resend APIキーを設定
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            print("❌ RESEND_API_KEY not found in environment variables")
            return False
        print(f"✅ RESEND_API_KEY found: {api_key[:8]}...")

        # APIキーをresendモジュールに設定
        resend.api_key = api_key

        # メール送信パラメータを準備（正しいResend Python SDK形式）
        print(f"📧 Attempting to send email to {user.email}")
        params = {
            "from": from_email,  # "from"が正しいパラメータ名
            "to": [user.email],
            "subject": subject,
        }
        if html_body:
            params["html"] = html_body
        if text_body:
            params["text"] = text_body

        # Resend APIでメール送信（静的メソッドとして呼び出す）
        email = resend.Emails.send(params)
        print(f"✅ Email sent successfully to {user.email}, ID: {email.get('id', 'N/A')}")

        return True

    except Exception as e:
        # エラー内容をログに記録して、デバッグを容易にする
        print(f"❌ Email send failed for {user.email}: {type(e).__name__}: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def send_notification_batch(db: Session) -> dict[str, Any]:
    """バッチ処理 - 現在JST時刻で対象ユーザーを選んでメールを送る

    成果を集計した辞書を返す（テストでは未使用）
    """
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc.astimezone(_jst_timezone())
    current_hour = now_jst.hour

    users = get_users_for_notification(db, current_hour)

    total = len(users)
    sent = 0
    failed = 0
    failed_emails = []

    for u in users:
        stats = get_weekly_stats(db, u.id)
        ok = send_notification_email(u, stats)
        if ok:
            sent += 1
        else:
            failed += 1
            failed_emails.append({"user_id": str(u.id), "email": u.email, "error": "send_failed"})

    return {
        "total_users": total,
        "emails_sent": sent,
        "emails_failed": failed,
        "current_hour_jst": current_hour,
        "failed_emails": failed_emails,
    }
