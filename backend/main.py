from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# 必要なモジュール
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, SuccessResponse, ErrorResponse, ErrorDetail
from auth import get_password_hash

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
            }
        }
    )

# ユーザー登録
@app.post(
    "/auth/register", 
    status_code=status.HTTP_201_CREATED, 
    response_model=SuccessResponse
)
def register_user(
    user_data: UserCreate, # リクエストボディから受け取るデータ
    db: Session = Depends(get_db) # DBセッションを依存性注入で取得
):
    """新規ユーザーを登録するエンドポイント"""
    
    # 1. メールアドレスの重複チェック
    exisiting_user = db.query(User).filter(User.email == user_data.email).first()
    
    if exisiting_user:
        # 400 bad requestを返す
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    # 2. パスワードのハッシュ化
    hashed_password = get_password_hash(user_data.password)
    
    # 3. 新機ユーザーをDBに追加
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        notification_time=user_data.notification_time
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
            detail="Database integrity error occurred during user registration."
        )
    
    # 4. レスポンスを返す
    user_response = UserResponse.model_validate(new_user)        

    return {
        "success": True,
        "data": user_response.model_dump(),
        "message": "User registered successfully."
    }
