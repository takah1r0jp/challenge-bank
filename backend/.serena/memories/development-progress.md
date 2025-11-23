# Failure Bank 開発進捗

## 最終更新: 2024-11-23

---

## バックエンド実装状況

### ✅ 実装完了（MVP達成）

#### 認証エンドポイント
- `POST /auth/register` - ユーザー登録（notification_time対応）
- `POST /auth/login` - ログイン
- `GET /auth/me` - 認証済みユーザー情報取得

#### 失敗記録CRUD
- `POST /failures` - 失敗記録作成（content, score）
- `GET /failures` - 失敗記録一覧取得（limit/offset対応）
- `GET /failures/{id}` - 失敗記録詳細取得
- `PUT /failures/{id}` - 失敗記録更新
- `DELETE /failures/{id}` - 失敗記録削除

#### 統計エンドポイント
- `GET /stats/summary` - 統計サマリー（全期間/今週/今月）
- `GET /stats/calendar` - カレンダーデータ（年月指定、JST対応）

### 🔧 技術スタック（バックエンド）
- FastAPI 0.121.1+
- SQLAlchemy 2.0.44+
- JWT + Argon2認証
- pytest（全テスト通過）
- Pydantic スキーマ

### 📝 今後の実装予定
- フィルタリング機能（日付範囲、ソート）
- 通知機能（SendGrid/Resend統合）
- Failureモデル拡張（将来的）

---

## フロントエンド実装状況

### ✅ 実装完了

#### 環境構築
- Next.js 16.0.3（App Router）
- TypeScript
- Tailwind CSS 4
- shadcn/ui コンポーネント

#### 実装済みページ
- `/register` - ユーザー登録ページ
- `/login` - ログインページ
- `/` (dashboard) - ダッシュボード（認証必須）

#### 実装済みコンポーネント
- UI: Button, Input, Form, Card, Dialog, Calendar, Badge, Textarea, Label
- Layout: Header
- Dashboard: FailureCard, StatsCard, EmptyState

#### 実装済みライブラリ
- API Client（axios）
- Form管理（react-hook-form + zod）
- 日付処理（date-fns）
- グラフ（recharts）
- トースト通知（react-hot-toast）

### 🔧 技術スタック（フロントエンド）
- Next.js 16 (React 19)
- TypeScript 5
- Tailwind CSS 4
- shadcn/ui
- Zod 4バリデーション
- Axios APIクライアント

### 📝 今後の実装予定
- カレンダービュー実装
- 統計グラフ実装
- 失敗記録の詳細表示・編集
- レスポンシブ対応の強化
