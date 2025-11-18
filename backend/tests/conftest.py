import os
import sys
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# backendディレクトリをPYTHONPATHに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402

# テスト用のSQLiteデータベースURL（メモリ上に作成）
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# テスト用エンジンとセッション
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """各テスト関数ごとにデータベースをセットアップ・クリーンアップ"""
    # テーブルを作成
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # テスト後にテーブルを削除
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """FastAPIのテストクライアントを提供"""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
