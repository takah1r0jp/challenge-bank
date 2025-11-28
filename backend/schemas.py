from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

# ======User関連=======


class UserCreate(BaseModel):
    """ユーザー登録時の入力"""

    email: EmailStr
    password: str = Field(min_length=8)
    notification_time: str | None = "20:00"

    @field_validator("notification_time")
    @classmethod
    def validate_notification_time(cls, v: str | None) -> str | None:
        """notification_timeのバリデーション（HH:MM形式をチェック）"""
        if v is None:
            return v
        try:
            # HH:MMフォーマットを検証
            time.fromisoformat(v)
            return v
        except ValueError as e:
            raise ValueError("notification_time must be in HH:MM format (e.g., '20:00')") from e


class UserUpdate(BaseModel):
    """ユーザー情報更新時の入力"""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    notification_time: str | None = None

    @field_validator("notification_time")
    @classmethod
    def validate_notification_time(cls, v: str | None) -> str | None:
        """notification_timeのバリデーション（HH:MM形式をチェック）"""
        if v is None:
            return v
        try:
            # HH:MMフォーマットを検証
            time.fromisoformat(v)
            return v
        except ValueError as e:
            raise ValueError("notification_time must be in HH:MM format (e.g., '20:00')") from e


class UserResponse(BaseModel):
    """ユーザー情報のレスポンス"""

    id: UUID
    email: EmailStr
    notification_time: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}  # SQLAlchemyモデルから変換可能に


# ======Challenge関連=======


class ChallengeCreate(BaseModel):
    """挑戦記録作成時の入力"""

    content: str = Field(min_length=1, max_length=1000)
    score: int = Field(ge=1, le=5)  # スコアは1から5の範囲


class ChallengeUpdate(BaseModel):
    """挑戦記録更新時の入力"""

    content: str | None = Field(None, min_length=1, max_length=1000)
    score: int | None = Field(None, ge=1, le=5)


class ChallengeResponse(BaseModel):
    """挑戦記録のレスポンス"""

    id: UUID
    user_id: UUID
    content: str
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ========== 継承を使ったネストモデル ==========


class UserWithChallenges(UserResponse):
    """
    UserResponseを継承して、challengesフィールドを追加
    id, email, notification_time, created_atは自動的に継承される
    """

    challenges: list[ChallengeResponse]


class ChallengeWithUser(ChallengeResponse):
    """
    ChallengeResponseを継承して、userフィールドを追加
    id, user_id, content, score, created_atは自動的に継承される
    """

    user: UserResponse


# ====== 統一レスポンス形式 ======


class SuccessResponse(BaseModel):
    """成功時のレスポンス（汎用）"""

    success: bool = True
    data: dict | list | None = None
    message: str | None = None


class ErrorDetail(BaseModel):
    """エラー詳細"""

    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    """エラー時のレスポンス"""

    success: bool = False
    error: ErrorDetail


# ====== 統計 ======


class PeriodStats(BaseModel):
    """期間別の統計情報"""

    challenge_count: int
    total_score: int
    average_score: float


class StatsSummaryResponse(BaseModel):
    """統計サマリーのレスポンス"""

    all_time: PeriodStats
    this_week: PeriodStats
    this_month: PeriodStats


class DayStats(BaseModel):
    """日別の統計情報"""

    date: str  # YYYY-MM-DD形式
    challenge_count: int
    total_score: int
    average_score: float


class CalendarResponse(BaseModel):
    """カレンダーレスポンス"""

    year: int
    month: int
    days: list[DayStats]


# ====== トークン ======
class TokenData(BaseModel):
    """トークンデータ"""

    access_token: str
    token_type: str = "bearer"


class UserWithToken(UserResponse):
    """ユーザー情報とトークンを含むレスポンス"""

    access_token: str
    token_type: str = "bearer"
