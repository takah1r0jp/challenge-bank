from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# ======User関連=======


class UserCreate(BaseModel):
    """ユーザー登録時の入力"""

    email: EmailStr
    password: str = Field(min_length=8)
    notification_time: str | None = "20:00"


class UserUpdate(BaseModel):
    """ユーザー情報更新時の入力"""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    notification_time: str | None = None


class UserResponse(BaseModel):
    """ユーザー情報のレスポンス"""

    id: UUID
    email: EmailStr
    notification_time: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}  # SQLAlchemyモデルから変換可能に


# ======Failure関連=======


class FailureCreate(BaseModel):
    """失敗記録作成時の入力"""

    content: str = Field(min_length=1, max_length=1000)
    score: int = Field(ge=1, le=5)  # スコアは1から5の範囲


class FailureUpdate(BaseModel):
    """失敗記録更新時の入力"""

    content: str | None = Field(None, min_length=1, max_length=1000)
    score: int | None = Field(None, ge=1, le=5)


class FailureResponse(BaseModel):
    """失敗記録のレスポンス"""

    id: UUID
    user_id: UUID
    content: str
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ========== 継承を使ったネストモデル ==========


class UserWithFailures(UserResponse):
    """
    UserResponseを継承して、failuresフィールドを追加
    id, email, notification_time, created_atは自動的に継承される
    """

    failures: list[FailureResponse]


class FailureWithUser(FailureResponse):
    """
    FailureResponseを継承して、userフィールドを追加
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

    failure_count: int
    total_score: int
    average_score: float


class StatsSummaryResponse(BaseModel):
    """統計サマリーのレスポンス"""

    all_time: PeriodStats
    this_week: PeriodStats
    this_month: PeriodStats


# ====== トークン ======
class TokenData(BaseModel):
    """トークンデータ"""

    access_token: str
    token_type: str = "bearer"


class UserWithToken(UserResponse):
    """ユーザー情報とトークンを含むレスポンス"""

    access_token: str
    token_type: str = "bearer"
