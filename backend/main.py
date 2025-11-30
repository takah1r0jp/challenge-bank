import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, get_password_hash, verify_password

# 必要なモジュール
from database import get_db
from email_service import send_notification_batch
from models import Challenge, User
from schemas import (
    CalendarResponse,
    ChallengeCreate,
    ChallengeResponse,
    ChallengeUpdate,
    DayStats,
    NotificationBatchResponse,
    NotificationTestResponse,
    PeriodStats,
    StatsSummaryResponse,
    SuccessResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
    UserWithToken,
)

# 日本標準時（JST: UTC+9）のタイムゾーン定義
jst = timezone(timedelta(hours=9))

app = FastAPI(title="Challenge Bank")

# CORS設定（環境変数から許可オリジンを取得）
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000",  # デフォルトは開発環境のみ
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)


# ヘルスチェック
@app.get("/")
def root():
    return {"message": "Challenge Bank API is running."}


# ====== API Key認証 ======
def verify_api_key(x_api_key: str = Header(None)):
    """Lambda内部API用のAPI Key認証"""
    expected_key = os.getenv("NOTIFICATION_API_KEY")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return True


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTPExceptionのカスタムハンドラー"""
    # エラーコードのマッピング
    error_code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        404: "NOT_FOUND",
        422: "VALIDATION_ERROR",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": error_code_map.get(exc.status_code, "ERROR"),
                "message": exc.detail,
                "details": None,
            },
        },
    )


# ユーザー登録
@app.post("/auth/register", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def register_user(
    user_data: UserCreate,  # リクエストボディから受け取るデータ
    db: Session = Depends(get_db),  # DBセッションを依存性注入で取得
):
    """新規ユーザーを登録するエンドポイント"""

    # 1. メールアドレスの重複チェック
    exisiting_user = db.query(User).filter(User.email == user_data.email).first()

    if exisiting_user:
        # 400 bad requestを返す
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists."
        )

    # 2. パスワードのハッシュ化
    hashed_password = get_password_hash(user_data.password)

    # 3. 新機ユーザーをDBに追加
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        notification_time=user_data.notification_time,
    )

    # セッションに追加(まだDBに保存されていない)
    db.add(new_user)

    try:
        db.commit()

        db.refresh(new_user)  # 新規ユーザーの情報を取得(id, created_atなど)
    except IntegrityError:
        # UNIQUE制約違反などのDB制約エラーが出た場合
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error occurred during user registration.",
        )

    # 4. レスポンスを返す
    user_response = UserResponse.model_validate(new_user)

    # トークン生成
    access_token = create_access_token(data={"sub": new_user.email})

    user_response = UserWithToken(**user_response.model_dump(), access_token=access_token)

    return {
        "success": True,
        "data": user_response.model_dump(),
        "message": "User registered successfully.",
    }


# ログイン機能
@app.post("/auth/login", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def login_user(request_data: UserCreate, db: Session = Depends(get_db)):
    # 1. ユーザーの存在確認
    user = db.query(User).filter(User.email == request_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password."
        )

    # 2. パスワードの検証
    if not verify_password(request_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password."
        )

    # 3. トークン生成
    access_token = create_access_token(data={"sub": user.email})

    user_response = UserWithToken(
        **UserResponse.model_validate(user).model_dump(), access_token=access_token
    )

    return {"success": True, "data": user_response.model_dump(), "message": "Login successful."}


# 現在のユーザー情報を取得
@app.get("/auth/me", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    """認証済みユーザーの情報を取得するエンドポイント"""
    user_response = UserResponse.model_validate(current_user)

    return {
        "success": True,
        "data": user_response.model_dump(),
        "message": "User information retrieved successfully.",
    }


# ユーザー情報を更新
@app.put("/auth/me", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの情報を更新するエンドポイント"""
    # notification_time, is_notification_setup_completedを更新可能
    if user_data.notification_time is not None:
        current_user.notification_time = user_data.notification_time

    if user_data.is_notification_setup_completed is not None:
        current_user.is_notification_setup_completed = user_data.is_notification_setup_completed

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error occurred during user update.",
        )

    user_response = UserResponse.model_validate(current_user)

    return {
        "success": True,
        "data": user_response.model_dump(),
        "message": "User information updated successfully.",
    }


# ログアウト
@app.post("/auth/logout", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def logout_user(current_user: User = Depends(get_current_user)):
    """ログアウトエンドポイント（クライアント側でトークンを削除する方式）"""
    # JWTはステートレスなので、サーバー側では何もしない
    # クライアント側でトークンを削除することでログアウトを実現
    return {
        "success": True,
        "data": None,
        "message": "Logout successful. Please remove the token from the client.",
    }


# ============ 挑戦記録エンドポイント ============


# 挑戦記録を作成
@app.post("/challenges", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def create_challenge(
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """新しい挑戦記録を作成するエンドポイント"""

    # 新しい挑戦記録を作成
    new_challenge = Challenge(
        user_id=current_user.id,
        content=challenge_data.content,
        score=challenge_data.score,
    )

    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

    # レスポンスを返す（UTC→JST変換）
    challenge_dict = ChallengeResponse.model_validate(new_challenge).model_dump()
    # UTC naive datetime → UTC aware → JST aware に変換
    created_at_jst = new_challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
    challenge_dict["created_at"] = created_at_jst.isoformat()

    return {
        "success": True,
        "data": challenge_dict,
        "message": "Challenge record created successfully.",
    }


# 挑戦記録一覧を取得
@app.get("/challenges", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
):
    """認証済みユーザーの挑戦記録一覧を取得するエンドポイント"""

    # 自分の挑戦記録のみを取得（他のユーザーの記録は見えない）
    # 新しい順（作成日時の降順）でソート
    challenges = (
        db.query(Challenge)
        .filter(Challenge.user_id == current_user.id)
        .order_by(Challenge.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # レスポンスを返す（UTC→JST変換）
    challenges_response = []
    for challenge in challenges:
        challenge_dict = ChallengeResponse.model_validate(challenge).model_dump()
        # UTC naive datetime → UTC aware → JST aware に変換
        created_at_jst = challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
        challenge_dict["created_at"] = created_at_jst.isoformat()
        challenges_response.append(challenge_dict)

    return {
        "success": True,
        "data": challenges_response,
        "message": "Challenge records retrieved successfully.",
    }


# 挑戦記録の詳細を取得
@app.get(
    "/challenges/{challenge_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def get_challenge_by_id(
    challenge_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の挑戦記録を取得するエンドポイント"""

    # 自分の挑戦記録のみ取得（他のユーザーの記録は404）
    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == challenge_id, Challenge.user_id == current_user.id)
        .first()
    )

    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge record not found.",
        )

    # レスポンスを返す（UTC→JST変換）
    challenge_dict = ChallengeResponse.model_validate(challenge).model_dump()
    # UTC naive datetime → UTC aware → JST aware に変換
    created_at_jst = challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
    challenge_dict["created_at"] = created_at_jst.isoformat()

    return {
        "success": True,
        "data": challenge_dict,
        "message": "Challenge record retrieved successfully.",
    }


# 挑戦記録を更新
@app.put(
    "/challenges/{challenge_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def update_challenge(
    challenge_id: UUID,
    challenge_data: ChallengeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の挑戦記録を更新するエンドポイント"""

    # 自分の挑戦記録のみ取得（他のユーザーの記録は404）
    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == challenge_id, Challenge.user_id == current_user.id)
        .first()
    )

    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge record not found.",
        )

    # 更新データを適用（Noneでないフィールドのみ更新）
    if challenge_data.content is not None:
        challenge.content = challenge_data.content
    if challenge_data.score is not None:
        challenge.score = challenge_data.score

    db.commit()
    db.refresh(challenge)

    # レスポンスを返す（UTC→JST変換）
    challenge_dict = ChallengeResponse.model_validate(challenge).model_dump()
    # UTC naive datetime → UTC aware → JST aware に変換
    created_at_jst = challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
    challenge_dict["created_at"] = created_at_jst.isoformat()

    return {
        "success": True,
        "data": challenge_dict,
        "message": "Challenge record updated successfully.",
    }


# 挑戦記録を削除
@app.delete(
    "/challenges/{challenge_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def delete_challenge(
    challenge_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の挑戦記録を削除するエンドポイント"""

    # 自分の挑戦記録のみ取得（他のユーザーの記録は404）
    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == challenge_id, Challenge.user_id == current_user.id)
        .first()
    )

    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge record not found.",
        )

    # 削除実行
    db.delete(challenge)
    db.commit()

    return {
        "success": True,
        "data": None,
        "message": "Challenge record deleted successfully.",
    }


# ====== 統計エンドポイント ======


# 統計サマリーを取得
@app.get("/stats/summary", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_stats_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの統計サマリーを取得するエンドポイント"""

    # 現在の日本時間
    now_jst = datetime.now(jst)

    # 今日の開始日（日本時間の0時）
    today_start_jst = now_jst.replace(hour=0, minute=0, second=0, microsecond=0)

    # 今週の開始日（日本時間の月曜日0時）
    week_start_jst = now_jst - timedelta(days=now_jst.weekday())
    week_start_jst = week_start_jst.replace(hour=0, minute=0, second=0, microsecond=0)

    # JSTをUTCに変換（DBと比較するため、tzinfo=Noneで取得）
    today_start_utc = today_start_jst.astimezone(timezone.utc).replace(tzinfo=None)
    week_start_utc = week_start_jst.astimezone(timezone.utc).replace(tzinfo=None)

    # 自分の挑戦記録を取得
    all_challenges = db.query(Challenge).filter(Challenge.user_id == current_user.id).all()

    # 今日の挑戦記録（UTCで比較）
    today_challenges = [f for f in all_challenges if f.created_at >= today_start_utc]

    # 今週の挑戦記録（UTCで比較）
    this_week_challenges = [f for f in all_challenges if f.created_at >= week_start_utc]

    # ヘルパー関数: 期間別の統計を計算
    def calculate_period_stats(challenges_list):
        if not challenges_list:
            return PeriodStats(challenge_count=0, total_score=0, average_score=0.0)

        challenge_count = len(challenges_list)
        total_score = sum(f.score for f in challenges_list)
        average_score = total_score / challenge_count if challenge_count > 0 else 0.0

        return PeriodStats(
            challenge_count=challenge_count, total_score=total_score, average_score=average_score
        )

    # 各期間の統計を計算
    today_stats = calculate_period_stats(today_challenges)
    this_week_stats = calculate_period_stats(this_week_challenges)
    all_time_stats = calculate_period_stats(all_challenges)

    stats_response = StatsSummaryResponse(
        today=today_stats, this_week=this_week_stats, all_time=all_time_stats
    )

    return {
        "success": True,
        "data": stats_response.model_dump(),
        "message": "Statistics summary retrieved successfully.",
    }


# カレンダーデータを取得
@app.get("/stats/calendar", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_calendar(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの指定月のカレンダーデータを取得するエンドポイント"""

    # 月のバリデーション
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Month must be between 1 and 12.",
        )

    # 指定月の開始日（日本時間）
    month_start_jst = datetime(year, month, 1, 0, 0, 0, tzinfo=jst)

    # 指定月の終了日（翌月の1日0時 - 1秒）
    if month == 12:
        month_end_jst = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=jst)
    else:
        month_end_jst = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=jst)

    # JSTをUTCに変換（DBと比較するため）
    month_start_utc = month_start_jst.astimezone(timezone.utc).replace(tzinfo=None)
    month_end_utc = month_end_jst.astimezone(timezone.utc).replace(tzinfo=None)

    # 指定月の挑戦記録を取得
    challenges = (
        db.query(Challenge)
        .filter(
            Challenge.user_id == current_user.id,
            Challenge.created_at >= month_start_utc,
            Challenge.created_at < month_end_utc,
        )
        .all()
    )

    # 日付ごとにグループ化
    from collections import defaultdict

    daily_stats = defaultdict(list)

    for challenge in challenges:
        # UTC時刻をJSTに変換して日付を取得
        created_at_jst = challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
        date_str = created_at_jst.strftime("%Y-%m-%d")
        daily_stats[date_str].append(challenge)
    
    # 日別統計を計算
    days_list = []
    for date_str, challenges_on_day in sorted(daily_stats.items()):
        challenge_count = len(challenges_on_day)
        total_score = sum(f.score for f in challenges_on_day)
        average_score = total_score / challenge_count if challenge_count > 0 else 0.0

        days_list.append(
            DayStats(
                date=date_str,
                challenge_count=challenge_count,
                total_score=total_score,
                average_score=average_score,
            )
        )

    calendar_response = CalendarResponse(year=year, month=month, days=days_list)

    return {
        "success": True,
        "data": calendar_response.model_dump(),
        "message": "Calendar data retrieved successfully.",
    }


# ====== 通知エンドポイント ======


@app.post(
    "/notifications/send", status_code=status.HTTP_200_OK, response_model=NotificationBatchResponse
)
def send_notifications(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key),
):
    """Lambda内部API: 現在のJST時刻に対応するユーザーにメール通知を送信"""
    result = send_notification_batch(db)
    return {
        "success": True,
        "data": result,
        "message": "Notification batch completed.",
    }


@app.post(
    "/notifications/test", status_code=status.HTTP_200_OK, response_model=NotificationTestResponse
)
def send_test_notification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """テスト用: 認証済みユーザーにテストメールを送信"""
    from email_service import get_weekly_stats, send_notification_email

    stats = get_weekly_stats(db, current_user.id)
    success = send_notification_email(current_user, stats)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send email"
        )

    return {
        "success": True,
        "data": {
            "email": current_user.email,
            "sent_at": datetime.now(timezone.utc).isoformat(),
        },
        "message": "Test notification email sent successfully.",
    }
