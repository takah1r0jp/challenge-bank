# Failure Bank API 仕様書

## 概要

Failure Bank APIは、日々の失敗を記録・管理し、統計情報を提供するためのRESTful APIです。

**ベースURL**: `http://localhost:8000`

---

## 認証

JWTトークンを使用したBearer認証を採用しています。

```
Authorization: Bearer {access_token}
```

---

## レスポンス形式

### 成功レスポンス

```json
{
  "success": true,
  "data": {},
  "message": "Success message"
}
```

### エラーレスポンス

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": null
  }
}
```

---

## エンドポイント一覧

## 🔐 認証エンドポイント

### POST /auth/register
新規ユーザーを登録します。

**認証**: 不要

**リクエストボディ**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "notification_time": "20:00"
}
```

**レスポンス** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00",
    "created_at": "2024-01-01T00:00:00",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "message": "User registered successfully."
}
```

**エラー**:
- `400 BAD_REQUEST`: メールアドレスが既に登録されている
- `422 VALIDATION_ERROR`: バリデーションエラー（パスワード8文字未満など）

---

### POST /auth/login
ログインしてアクセストークンを取得します。

**認証**: 不要

**リクエストボディ**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00",
    "created_at": "2024-01-01T00:00:00",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "message": "Login successful."
}
```

**エラー**:
- `401 UNAUTHORIZED`: メールアドレスまたはパスワードが正しくない

---

### POST /auth/logout
ログアウトします（トークンの無効化）。

**認証**: 必要

**リクエストボディ**: なし

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": null,
  "message": "Logout successful."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー

---

### GET /auth/me
認証済みユーザーの情報を取得します。

**認証**: 必要

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "notification_time": "20:00",
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "User information retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: トークンが無効または期限切れ

---

### PATCH /auth/me
認証済みユーザーの情報を更新します。

**認証**: 必要

**リクエストボディ** (すべてオプション):
```json
{
  "email": "newemail@example.com",
  "password": "newpassword123",
  "notification_time": "21:00"
}
```

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "newemail@example.com",
    "notification_time": "21:00",
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "User information updated successfully."
}
```

**エラー**:
- `400 BAD_REQUEST`: メールアドレスが既に使用されている
- `401 UNAUTHORIZED`: 認証エラー
- `422 VALIDATION_ERROR`: バリデーションエラー

---

## 📝 失敗記録エンドポイント

### POST /failures
新しい失敗記録を作成します。

**認証**: 必要

**リクエストボディ**:
```json
{
  "content": "プレゼンで緊張して早口になってしまった",
  "score": 3
}
```

**レスポンス** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "content": "プレゼンで緊張して早口になってしまった",
    "score": 3,
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "Failure record created successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `422 VALIDATION_ERROR`: バリデーションエラー（スコアが1-5の範囲外など）

---

### GET /failures
ユーザーの失敗記録一覧を取得します。

**認証**: 必要

**クエリパラメータ**:
- `limit` (オプション): 取得件数（デフォルト: 20）
- `offset` (オプション): オフセット（デフォルト: 0）
- `start_date` (オプション): 開始日（YYYY-MM-DD形式）
- `end_date` (オプション): 終了日（YYYY-MM-DD形式）

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "content": "プレゼンで緊張して早口になってしまった",
      "score": 3,
      "created_at": "2024-01-01T00:00:00"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "content": "朝寝坊して遅刻した",
      "score": 4,
      "created_at": "2024-01-02T00:00:00"
    }
  ],
  "message": "Failure records retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー

---

### GET /failures/{id}
特定の失敗記録の詳細を取得します。

**認証**: 必要

**パスパラメータ**:
- `id`: 失敗記録のID

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "content": "プレゼンで緊張して早口になってしまった",
    "score": 3,
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "Failure record retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `404 NOT_FOUND`: 指定されたIDの失敗記録が存在しない、または他のユーザーの記録

---

### PATCH /failures/{id}
失敗記録を更新します。

**認証**: 必要

**パスパラメータ**:
- `id`: 失敗記録のID

**リクエストボディ** (すべてオプション):
```json
{
  "content": "プレゼンで緊張して早口になった。次は深呼吸してから話す。",
  "score": 2
}
```

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "content": "プレゼンで緊張して早口になった。次は深呼吸してから話す。",
    "score": 2,
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "Failure record updated successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `404 NOT_FOUND`: 指定されたIDの失敗記録が存在しない、または他のユーザーの記録
- `422 VALIDATION_ERROR`: バリデーションエラー

---

### DELETE /failures/{id}
失敗記録を削除します。

**認証**: 必要

**パスパラメータ**:
- `id`: 失敗記録のID

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": null,
  "message": "Failure record deleted successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `404 NOT_FOUND`: 指定されたIDの失敗記録が存在しない、または他のユーザーの記録

---

## 📊 統計エンドポイント

### GET /stats/summary
失敗記録の統計サマリーを取得します。

**認証**: 必要

**クエリパラメータ**:
- `period` (オプション): 集計期間 (`week`, `month`, `year`, `all`) デフォルト: `all`

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "total_failures": 150,
    "average_score": 3.2,
    "total_days": 45,
    "current_streak": 7,
    "longest_streak": 14,
    "score_distribution": {
      "1": 10,
      "2": 25,
      "3": 50,
      "4": 40,
      "5": 25
    }
  },
  "message": "Statistics summary retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー

---

### GET /stats/calendar
カレンダー形式の統計データを取得します（ヒートマップ用）。

**認証**: 必要

**クエリパラメータ**:
- `year` (必須): 年（例: 2024）
- `month` (オプション): 月（1-12）指定しない場合は年全体

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "2024-01-01": {
      "count": 2,
      "total_score": 6
    },
    "2024-01-02": {
      "count": 1,
      "total_score": 3
    },
    "2024-01-03": {
      "count": 0,
      "total_score": 0
    }
  },
  "message": "Calendar statistics retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `422 VALIDATION_ERROR`: バリデーションエラー（年が不正など）

---

### GET /stats/trends
時系列での失敗記録のトレンドを取得します。

**認証**: 必要

**クエリパラメータ**:
- `period` (必須): 集計単位 (`day`, `week`, `month`)
- `limit` (オプション): 取得する期間数（デフォルト: 30）

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "period": "2024-01-01",
      "count": 2,
      "average_score": 3.0
    },
    {
      "period": "2024-01-02",
      "count": 1,
      "average_score": 4.0
    },
    {
      "period": "2024-01-03",
      "count": 3,
      "average_score": 2.7
    }
  ],
  "message": "Trend statistics retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `422 VALIDATION_ERROR`: バリデーションエラー

---

## ⚙️ 設定エンドポイント

### GET /settings
ユーザーの設定を取得します（現在は通知設定のみ）。

**認証**: 必要

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "notification_time": "20:00",
    "notification_enabled": true
  },
  "message": "Settings retrieved successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー

---

### PATCH /settings
ユーザーの設定を更新します。

**認証**: 必要

**リクエストボディ** (すべてオプション):
```json
{
  "notification_time": "21:00",
  "notification_enabled": false
}
```

**レスポンス** (200 OK):
```json
{
  "success": true,
  "data": {
    "notification_time": "21:00",
    "notification_enabled": false
  },
  "message": "Settings updated successfully."
}
```

**エラー**:
- `401 UNAUTHORIZED`: 認証エラー
- `422 VALIDATION_ERROR`: バリデーションエラー（時刻形式が不正など）

---

## エラーコード一覧

| コード | 説明 |
|--------|------|
| `BAD_REQUEST` | リクエストが不正（重複データなど） |
| `UNAUTHORIZED` | 認証エラー（トークン無効、期限切れなど） |
| `NOT_FOUND` | リソースが見つからない |
| `VALIDATION_ERROR` | バリデーションエラー（入力値が不正） |

---

## データ型

### User
```typescript
{
  id: UUID
  email: string
  notification_time: string | null
  created_at: datetime
}
```

### Failure
```typescript
{
  id: UUID
  user_id: UUID
  content: string
  score: number (1-5)
  created_at: datetime
}
```

---

## 実装ステータス

| エンドポイント | メソッド | ステータス |
|---------------|---------|-----------|
| /auth/register | POST | ✅ 実装済み |
| /auth/login | POST | ✅ 実装済み |
| /auth/logout | POST | 📝 未実装 |
| /auth/me | GET | ✅ 実装済み |
| /auth/me | PATCH | 📝 未実装 |
| /failures | POST | 📝 未実装 |
| /failures | GET | 📝 未実装 |
| /failures/{id} | GET | 📝 未実装 |
| /failures/{id} | PATCH | 📝 未実装 |
| /failures/{id} | DELETE | 📝 未実装 |
| /stats/summary | GET | 📝 未実装 |
| /stats/calendar | GET | 📝 未実装 |
| /stats/trends | GET | 📝 未実装 |
| /settings | GET | 📝 未実装 |
| /settings | PATCH | 📝 未実装 |

---

## 開発時の注意事項

1. **認証の実装**: すべての保護されたエンドポイントは `Depends(get_current_user)` を使用
2. **ユーザー分離**: 各ユーザーは自分のデータのみアクセス可能（クエリに `user_id` フィルタを追加）
3. **バリデーション**: Pydanticスキーマで入力値を検証
4. **エラーハンドリング**: カスタム例外ハンドラーで統一されたエラーレスポンスを返す
5. **テスト**: 各エンドポイントの正常系・異常系テストを作成

---

最終更新: 2024-11-21
