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
    FailureCreate,
    FailureResponse,
    FailureUpdate,
    SuccessResponse,
    UserCreate,
    UserResponse,
    UserWithToken,
)

app = FastAPI(title="Failure Bank")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.jsのデフォルトポート
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
    failures = (
        db.query(Failure)
        .filter(Failure.user_id == current_user.id)
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
