import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, get_password_hash, verify_password

# 必要なモジュール
from database import get_db
from models import Failure, User
from schemas import (
    CalendarResponse,
    DayStats,
    FailureCreate,
    FailureResponse,
    FailureUpdate,
    PeriodStats,
    StatsSummaryResponse,
    SuccessResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
    UserWithToken,
)

app = FastAPI(title="Failure Bank")

# CORS設定（環境変数から許可オリジンを取得）
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"  # デフォルトは開発環境のみ
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
    return {"message": "Failure Bank API is running."}


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
    # notification_timeのみ更新可能（将来的にemailやpasswordも追加可能）
    if user_data.notification_time is not None:
        current_user.notification_time = user_data.notification_time

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


# ============ 失敗記録エンドポイント ============


# 失敗記録を作成
@app.post("/failures", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def create_failure(
    failure_data: FailureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """新しい失敗記録を作成するエンドポイント"""

    # 新しい失敗記録を作成
    new_failure = Failure(
        user_id=current_user.id,
        content=failure_data.content,
        score=failure_data.score,
    )

    db.add(new_failure)
    db.commit()
    db.refresh(new_failure)

    # レスポンスを返す
    failure_response = FailureResponse.model_validate(new_failure)

    return {
        "success": True,
        "data": failure_response.model_dump(),
        "message": "Failure record created successfully.",
    }


# 失敗記録一覧を取得
@app.get("/failures", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_failures(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
):
    """認証済みユーザーの失敗記録一覧を取得するエンドポイント"""

    # 自分の失敗記録のみを取得（他のユーザーの記録は見えない）
    # 新しい順（作成日時の降順）でソート
    failures = (
        db.query(Failure)
        .filter(Failure.user_id == current_user.id)
        .order_by(Failure.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # レスポンスを返す
    failures_response = [
        FailureResponse.model_validate(failure).model_dump() for failure in failures
    ]

    return {
        "success": True,
        "data": failures_response,
        "message": "Failure records retrieved successfully.",
    }


# 失敗記録の詳細を取得
@app.get("/failures/{failure_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_failure_by_id(
    failure_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の失敗記録を取得するエンドポイント"""

    # 自分の失敗記録のみ取得（他のユーザーの記録は404）
    failure = (
        db.query(Failure)
        .filter(Failure.id == failure_id, Failure.user_id == current_user.id)
        .first()
    )

    if not failure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure record not found.",
        )

    # レスポンスを返す
    failure_response = FailureResponse.model_validate(failure)

    return {
        "success": True,
        "data": failure_response.model_dump(),
        "message": "Failure record retrieved successfully.",
    }


# 失敗記録を更新
@app.put("/failures/{failure_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def update_failure(
    failure_id: UUID,
    failure_data: FailureUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の失敗記録を更新するエンドポイント"""

    # 自分の失敗記録のみ取得（他のユーザーの記録は404）
    failure = (
        db.query(Failure)
        .filter(Failure.id == failure_id, Failure.user_id == current_user.id)
        .first()
    )

    if not failure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure record not found.",
        )

    # 更新データを適用（Noneでないフィールドのみ更新）
    if failure_data.content is not None:
        failure.content = failure_data.content
    if failure_data.score is not None:
        failure.score = failure_data.score

    db.commit()
    db.refresh(failure)

    # レスポンスを返す
    failure_response = FailureResponse.model_validate(failure)

    return {
        "success": True,
        "data": failure_response.model_dump(),
        "message": "Failure record updated successfully.",
    }


# 失敗記録を削除
@app.delete(
    "/failures/{failure_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def delete_failure(
    failure_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの特定の失敗記録を削除するエンドポイント"""

    # 自分の失敗記録のみ取得（他のユーザーの記録は404）
    failure = (
        db.query(Failure)
        .filter(Failure.id == failure_id, Failure.user_id == current_user.id)
        .first()
    )

    if not failure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure record not found.",
        )

    # 削除実行
    db.delete(failure)
    db.commit()

    return {
        "success": True,
        "data": None,
        "message": "Failure record deleted successfully.",
    }


# ====== 統計エンドポイント ======


# 統計サマリーを取得
@app.get("/stats/summary", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def get_stats_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """認証済みユーザーの統計サマリーを取得するエンドポイント"""

    # 日本時間のタイムゾーン（JST = UTC+9）
    jst = timezone(timedelta(hours=9))

    # 現在の日本時間
    now_jst = datetime.now(jst)

    # 今週の開始日（日本時間の月曜日0時）
    week_start_jst = now_jst - timedelta(days=now_jst.weekday())
    week_start_jst = week_start_jst.replace(hour=0, minute=0, second=0, microsecond=0)

    # 今月の開始日（日本時間の1日0時）
    month_start_jst = now_jst.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # JSTをUTCに変換（DBと比較するため、tzinfo=Noneで取得）
    week_start_utc = week_start_jst.astimezone(timezone.utc).replace(tzinfo=None)
    month_start_utc = month_start_jst.astimezone(timezone.utc).replace(tzinfo=None)

    # 自分の失敗記録を取得
    all_failures = db.query(Failure).filter(Failure.user_id == current_user.id).all()

    # 今週の失敗記録（UTCで比較）
    this_week_failures = [f for f in all_failures if f.created_at >= week_start_utc]

    # 今月の失敗記録（UTCで比較）
    this_month_failures = [f for f in all_failures if f.created_at >= month_start_utc]

    # ヘルパー関数: 期間別の統計を計算
    def calculate_period_stats(failures_list):
        if not failures_list:
            return PeriodStats(failure_count=0, total_score=0, average_score=0.0)

        failure_count = len(failures_list)
        total_score = sum(f.score for f in failures_list)
        average_score = total_score / failure_count if failure_count > 0 else 0.0

        return PeriodStats(
            failure_count=failure_count, total_score=total_score, average_score=average_score
        )

    # 各期間の統計を計算
    all_time_stats = calculate_period_stats(all_failures)
    this_week_stats = calculate_period_stats(this_week_failures)
    this_month_stats = calculate_period_stats(this_month_failures)

    stats_response = StatsSummaryResponse(
        all_time=all_time_stats, this_week=this_week_stats, this_month=this_month_stats
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

    # 日本時間のタイムゾーン
    jst = timezone(timedelta(hours=9))

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

    # 指定月の失敗記録を取得
    failures = (
        db.query(Failure)
        .filter(
            Failure.user_id == current_user.id,
            Failure.created_at >= month_start_utc,
            Failure.created_at < month_end_utc,
        )
        .all()
    )

    # 日付ごとにグループ化
    from collections import defaultdict

    daily_stats = defaultdict(list)

    for failure in failures:
        # UTC時刻をJSTに変換して日付を取得
        created_at_jst = failure.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
        date_str = created_at_jst.strftime("%Y-%m-%d")
        daily_stats[date_str].append(failure)

    # 日別統計を計算
    days_list = []
    for date_str, failures_on_day in sorted(daily_stats.items()):
        failure_count = len(failures_on_day)
        total_score = sum(f.score for f in failures_on_day)
        average_score = total_score / failure_count if failure_count > 0 else 0.0

        days_list.append(
            DayStats(
                date=date_str,
                failure_count=failure_count,
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
