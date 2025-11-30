import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class User(Base):
    __tablename__ = "users"

    # uuidをprimary keyとして使用
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    notification_time: Mapped[str] = mapped_column(
        String(5), default="20:00", nullable=True
    )  # "HH:MM"形式で保存
    is_notification_setup_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )  # 通知設定完了フラグ
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow(), nullable=False
    )

    # リレーション
    challenges: Mapped[list["Challenge"]] = relationship(
        "Challenge", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # Userテーブルの外部キー
    content: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 挑戦の質を数値化したもの
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow(), nullable=False
    )

    # リレーション（型ヒント付き）
    user: Mapped["User"] = relationship(
        back_populates="challenges",
        lazy="joined",  # Challengeを取得時にUserも一緒に取得
    )

    def __repr__(self) -> str:
        return f"<Challenge(id={self.id}, user_id={self.user_id}, score={self.score})>"
