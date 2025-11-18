from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# PostgreSQLのデータベースURL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ttaka:postgres@localhost/failure_bank"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # SQLログを出力（開発時に便利、本番はFalse推奨）
    pool_pre_ping=True,  # 接続の有効性を確認
    pool_size=5,  # コネクションプールのサイズ
    max_overflow=10,  # プールを超えた追加接続数
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# DB接続用の依存性
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
