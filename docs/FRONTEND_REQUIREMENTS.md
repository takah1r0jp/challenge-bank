# Failure Bank - フロントエンド開発要件書

**挑戦を習慣化し、成長を可視化するWebアプリケーション - フロントエンド仕様**

## プロジェクト概要

Failure Bankは、ユーザーが日々の失敗を記録・可視化し、挑戦を習慣化するためのWebアプリケーションです。このドキュメントでは、Next.js (App Router) を使用したフロントエンドの開発要件を定義します。

## 技術スタック

### Core
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 3.0+
- **State Management**: React Context API + hooks（または Zustand/Jotai）
- **Form Management**: React Hook Form + Zod（バリデーション）
- **HTTP Client**: Axios または Fetch API
- **Deploy**: Vercel

### UI/UX
- **Component Library**: shadcn/ui（推奨）または Radix UI
- **Icons**: Lucide React または Heroicons
- **Charts**: Recharts または Chart.js
- **Calendar**: React Big Calendar または FullCalendar
- **Animations**: Framer Motion（必要に応じて）
- **Toast/Notifications**: react-hot-toast または sonner

### 開発ツール
- **Linter**: ESLint
- **Formatter**: Prettier
- **Type Checking**: TypeScript strict mode
- **Testing**: Jest + React Testing Library（推奨）
- **E2E Testing**: Playwright または Cypress（後期フェーズ）

## プロジェクト構造

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx              # 認証済みレイアウト
│   │   ├── page.tsx                # ダッシュボード
│   │   ├── failures/
│   │   │   ├── page.tsx            # 失敗一覧
│   │   │   ├── new/
│   │   │   │   └── page.tsx        # 失敗記録作成
│   │   │   └── [id]/
│   │   │       ├── page.tsx        # 失敗詳細
│   │   │       └── edit/
│   │   │           └── page.tsx    # 失敗編集
│   │   ├── statistics/
│   │   │   └── page.tsx            # 統計・可視化
│   │   └── settings/
│   │       └── page.tsx            # 設定
│   ├── layout.tsx                  # ルートレイアウト
│   └── globals.css                 # グローバルスタイル
├── components/
│   ├── ui/                         # shadcn/ui コンポーネント
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── failures/
│   │   ├── FailureCard.tsx
│   │   ├── FailureForm.tsx
│   │   └── FailureList.tsx
│   ├── statistics/
│   │   ├── TotalCounter.tsx
│   │   ├── CalendarView.tsx
│   │   └── StatsChart.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── common/
│       ├── Loading.tsx
│       └── ErrorBoundary.tsx
├── lib/
│   ├── api/
│   │   ├── client.ts               # API クライアント設定
│   │   ├── auth.ts                 # 認証API
│   │   ├── failures.ts             # 失敗記録API
│   │   └── statistics.ts           # 統計API
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useFailures.ts
│   │   └── useStatistics.ts
│   ├── context/
│   │   └── AuthContext.tsx
│   ├── utils/
│   │   ├── validators.ts           # Zodスキーマ
│   │   ├── formatters.ts           # 日付・数値フォーマット
│   │   └── constants.ts
│   └── types/
│       └── index.ts                # 型定義
├── public/
│   ├── icons/
│   └── images/
├── .env.local                      # 環境変数
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── FRONTEND_REQUIREMENTS.md        # このファイル
```

## MVP機能仕様

### 1. 認証機能

#### 1.1 ユーザー登録 (`/register`)
- メールアドレス入力フォーム
- パスワード入力フォーム（8文字以上、確認用フィールド付き）
- バリデーション：
  - メールアドレス形式チェック
  - パスワード強度チェック
  - パスワード一致チェック
- 登録成功後、自動ログイン → ダッシュボードへリダイレクト
- エラーハンドリング（メール重複、サーバーエラーなど）

#### 1.2 ログイン (`/login`)
- メールアドレス入力フォーム
- パスワード入力フォーム
- 「ログイン状態を保持する」チェックボックス（オプション）
- ログイン成功後、ダッシュボードへリダイレクト
- 未登録の場合は登録ページへのリンク表示

#### 1.3 認証状態管理
- JWTトークンをlocalStorageまたはhttpOnly Cookie（推奨）に保存
- 認証が必要なページへのアクセス時、トークン有効性チェック
- トークン期限切れ時、自動ログアウト → ログインページへリダイレクト
- 認証済みユーザーは `/login`, `/register` にアクセス不可（ダッシュボードへリダイレクト）

#### 1.4 ログアウト
- ヘッダーに「ログアウト」ボタン配置
- トークン削除 → ログインページへリダイレクト

---

### 2. 失敗記録機能（Core）

#### 2.1 失敗記録作成 (`/failures/new`)

**フォームフィールド（MVP版）**
- **失敗内容（content）**（必須）
  - プレースホルダー: "どんな失敗をしたの？（例: 環境構築で1日溶かした）"
  - テキストエリア（複数行対応）
  - 最大文字数: 1000文字

- **スコア（score）**（必須）
  - ラジオボタンまたはスライダー（1-5段階）
  - ラベル: ★で表す
  - 説明: "この失敗の価値は？（挑戦度や学びの大きさ）"

**バリデーション**
- すべてのフィールドが必須
- 文字数制限チェック
- スコアは1-5の範囲内

**送信処理**
- `POST /failures` API呼び出し
- 成功時: トースト通知 → 失敗一覧ページへリダイレクト
- 失敗時: エラーメッセージ表示

**Note（将来拡張）**
Phase 2では以下のフィールドを追加予定：
- challenge_content（挑戦内容）
- failure_content（失敗内容）
- next_action（ネクストアクション）
- challenge_level（チャレンジ度合い）
- novelty_level（新しい度合い）

#### 2.2 失敗記録一覧 (`/failures`)

**表示内容（MVP版）**
- 失敗記録のリスト表示（カード形式推奨）
- 各カードに表示する情報：
  - 失敗内容（content）- 省略形（最初の100文字）
  - スコア（score）- ★アイコンで視覚化（例: ★★★☆☆）
  - 記録日時（created_at）- 相対時間表示（"3時間前"、"2日前"など）
  - 詳細ページへのリンク

**機能（MVP版）**
- ページネーション（1ページ20件）
- ソート（新しい順/古い順）

**UI/UX**
- 空状態の表示（記録がない場合）
  - メッセージ: "まだ失敗を記録していません"
  - "失敗を記録する" ボタン → `/failures/new`

**Note（Phase 2で追加予定）**
- 日付範囲フィルタ（開始日・終了日）
- スコアフィルタ（1-5）
- 検索機能

#### 2.3 失敗記録詳細 (`/failures/[id]`)

**表示内容（MVP版）**
- すべてのフィールドを完全に表示
  - 失敗内容（content）- 全文表示
  - スコア（score）- ★アイコンで視覚的表現
  - 作成日時（created_at）- フルフォーマット表示

**アクション**
- 編集ボタン → `/failures/[id]/edit`
- 削除ボタン（確認ダイアログ付き）
- 一覧へ戻るボタン

#### 2.4 失敗記録編集 (`/failures/[id]/edit`)

**フォーム**
- 作成フォームと同じUI
- 既存データを初期値として表示

**送信処理**
- `PUT /failures/{id}` API呼び出し
- 成功時: トースト通知 → 詳細ページへリダイレクト
- 失敗時: エラーメッセージ表示

#### 2.5 失敗記録削除

**確認ダイアログ**
- "本当に削除しますか？この操作は取り消せません。"
- キャンセル / 削除ボタン

**送信処理**
- `DELETE /failures/{id}` API呼び出し
- 成功時: トースト通知 → 一覧ページへリダイレクト

---

### 3. ダッシュボード (`/`)

**表示内容**
- **累積失敗数カウンター**（大きく強調表示）
  - "あなたの失敗貯金: XX回"
  - アニメーション効果（カウントアップ）

- **今週の記録数**
  - "今週の挑戦: XX回"

- **最近の失敗記録**（最新5件）
  - カード形式で表示
  - "もっと見る" → `/failures`

- **今週の統計プレビュー**
  - 簡易的な折れ線グラフ
  - "詳細を見る" → `/statistics`

**アクション**
- "失敗を記録する" ボタン（目立つ配置） → `/failures/new`

---

### 4. 統計・可視化 (`/statistics`)

#### 4.1 累積失敗数カウンター
- 全期間の総記録数を大きく表示
- 前月比の増減（+XX回、-XX回）

#### 4.2 カレンダービュー

**表示内容**
- 月次カレンダー形式
- 記録がある日にマークを表示
  - マークの大きさ/色の濃淡で記録数を視覚化
  - チャレンジ度合いや新しい度合いの平均値で色分け（オプション）

**インタラクション**
- 日付クリックで、その日の失敗記録をポップアップ表示
- 月切り替えボタン（前月/次月）

**API呼び出し**
- `GET /statistics/calendar?year=2024&month=1`

#### 4.3 統計グラフ

**週次統計**
- 過去4週間の記録数を折れ線グラフまたは棒グラフで表示
- X軸: 週（例: "1/1-1/7", "1/8-1/14"）
- Y軸: 記録数

**月次統計**
- 過去12ヶ月の記録数を折れ線グラフまたは棒グラフで表示
- X軸: 月（例: "1月", "2月"）
- Y軸: 記録数

**インタラクション**
- タブ切り替え（週次/月次）
- ホバーで詳細データ表示

---

### 5. 設定ページ (`/settings`)

#### 5.1 プロフィール設定（Phase 2）
- メールアドレス表示（変更不可）
- パスワード変更機能（将来実装）

#### 5.2 通知設定（将来実装）
- 通知のON/OFF切り替え
- 通知時刻の設定
- 通知方法の選択（メール/プッシュ）

---

## UI/UXデザインガイドライン

### デザインコンセプト
- **ポジティブで温かみのあるデザイン**: 失敗を肯定的に捉える
- **シンプルで直感的**: 記録の障壁を最小限に
- **視覚的フィードバック**: 成長が実感できる

### カラーパレット（例）
- **Primary**: 挑戦を表す色（例: 青 #3B82F6）
- **Secondary**: 成長を表す色（例: 緑 #10B981）
- **Accent**: 失敗を温かく受け止める色（例: オレンジ #F59E0B）
- **Background**: クリーンな背景（例: 白 #FFFFFF、グレー #F9FAFB）
- **Text**: 読みやすい色（例: ダークグレー #1F2937）

### タイポグラフィ
- **見出し**: 太字で目立つフォント（例: Inter Bold, Noto Sans JP Bold）
- **本文**: 読みやすいフォント（例: Inter Regular, Noto Sans JP Regular）
- **サイズ**: レスポンシブ対応（モバイル: 16px、デスクトップ: 18px）

### レスポンシブデザイン
- **モバイルファースト**: スマホでの使いやすさを最優先
- **ブレークポイント**:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

### アクセシビリティ
- ARIA属性の適切な使用
- キーボード操作対応
- コントラスト比の確保（WCAG 2.1 AA準拠）
- スクリーンリーダー対応

---

## 状態管理

### 認証状態
- グローバルな状態として管理（Context API または Zustand）
- 保持する情報:
  - `user`: ユーザー情報（id, email, created_at）
  - `token`: JWTアクセストークン
  - `isAuthenticated`: 認証状態フラグ
  - `isLoading`: 認証状態確認中フラグ

### フォーム状態
- React Hook Form で管理
- Zod でバリデーションスキーマ定義

### API レスポンス状態
- ローディング状態（`isLoading`）
- エラー状態（`error`）
- データ状態（`data`）
- カスタムフック（`useFailures`, `useStatistics`）で抽象化

---

## API統合

### ベースURL
- 開発環境: `http://localhost:8000`
- 本番環境: `https://api.failure-bank.com`（環境変数で管理）

### 認証ヘッダー
```typescript
Authorization: Bearer <access_token>
```

### エンドポイント一覧

#### 認証
- `POST /auth/register`: ユーザー登録
- `POST /auth/login`: ログイン
- `GET /auth/me`: 認証済みユーザー情報取得

#### 失敗記録
- `POST /failures`: 失敗記録作成
- `GET /failures`: 失敗記録一覧取得
- `GET /failures/{id}`: 失敗記録詳細取得
- `PUT /failures/{id}`: 失敗記録更新
- `DELETE /failures/{id}`: 失敗記録削除

#### 統計（MVP版）
- `GET /stats/summary`: 統計サマリー取得（全期間、今週、今月）
- `GET /stats/calendar?year=2024&month=1`: カレンダーデータ取得

### エラーハンドリング

**HTTPステータスコード**
- `401 Unauthorized`: 認証エラー → ログインページへリダイレクト
- `403 Forbidden`: 権限エラー → エラーメッセージ表示
- `404 Not Found`: リソース未発見 → 404ページ表示
- `422 Unprocessable Entity`: バリデーションエラー → フォームにエラー表示
- `500 Internal Server Error`: サーバーエラー → エラーページ表示

**エラーレスポンス形式**
```typescript
{
  "detail": "エラーメッセージ"
}
```

**トースト通知**
- 成功: 緑色、3秒表示
- エラー: 赤色、5秒表示

---

## 型定義（TypeScript）

```typescript
// lib/types/index.ts

// ========== 認証関連の型 ==========

// User型
export interface User {
  id: string;
  email: string;
  notification_time?: string; // "HH:MM" 形式（例: "20:00"）
  created_at: string;
}

// Token型
export interface Token {
  access_token: string;
  token_type: string;
}

// ========== Failure関連の型（MVP版） ==========

// Failure型（MVP版：contentとscoreのみ）
export interface Failure {
  id: string;
  user_id: string;
  content: string;       // 失敗内容（MVP版では1つのフィールドに統合）
  score: number;         // 1-5のスコア（挑戦度や学びの大きさ）
  created_at: string;
}

// Failure作成用型（MVP版）
export interface FailureCreate {
  content: string;
  score: number;         // 1-5
}

// Failure更新用型（MVP版）
export interface FailureUpdate {
  content?: string;
  score?: number;        // 1-5
}

// ========== API レスポンス型 ==========

// 統一レスポンス型
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

// エラーレスポンス型
export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

// ========== 統計関連の型（MVP版） ==========

// 期間別統計
export interface PeriodStats {
  failure_count: number;
  total_score: number;
  average_score: number;
}

// 統計サマリー
export interface StatsSummary {
  all_time: PeriodStats;
  this_week: PeriodStats;
  this_month: PeriodStats;
}

// カレンダー日別データ
export interface DayStats {
  date: string;          // "YYYY-MM-DD" 形式
  failure_count: number;
  total_score: number;
  average_score: number;
}

// カレンダーレスポンス
export interface CalendarStats {
  year: number;
  month: number;
  days: DayStats[];
}

// ========== Phase 2以降で拡張予定 ==========
/*
export interface FailureExtended {
  id: string;
  user_id: string;
  challenge_content: string;
  failure_content: string;
  next_action: string;
  challenge_level: 1 | 2 | 3;
  novelty_level: 1 | 2 | 3;
  created_at: string;
  updated_at: string;
}
*/
```

---

## バリデーションスキーマ（Zod）

```typescript
// lib/utils/validators.ts
import { z } from "zod";

// ユーザー登録スキーマ
export const registerSchema = z.object({
  email: z.string().email("有効なメールアドレスを入力してください"),
  password: z
    .string()
    .min(8, "パスワードは8文字以上である必要があります"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "パスワードが一致しません",
  path: ["confirmPassword"],
});

// ログインスキーマ
export const loginSchema = z.object({
  email: z.string().email("有効なメールアドレスを入力してください"),
  password: z.string().min(1, "パスワードを入力してください"),
});

// 失敗記録スキーマ（MVP版：contentとscoreのみ）
export const failureSchema = z.object({
  content: z
    .string()
    .min(1, "失敗内容を入力してください")
    .max(1000, "失敗内容は1000文字以内で入力してください"),
  score: z
    .number()
    .int("スコアは整数である必要があります")
    .min(1, "スコアは1以上である必要があります")
    .max(5, "スコアは5以下である必要があります"),
});

// Phase 2以降で拡張予定
/*
export const failureSchemaExtended = z.object({
  challenge_content: z
    .string()
    .min(1, "挑戦内容を入力してください")
    .max(500, "挑戦内容は500文字以内で入力してください"),
  failure_content: z
    .string()
    .min(1, "失敗内容を入力してください")
    .max(1000, "失敗内容は1000文字以内で入力してください"),
  next_action: z
    .string()
    .min(1, "ネクストアクションを入力してください")
    .max(500, "ネクストアクションは500文字以内で入力してください"),
  challenge_level: z.number().int().min(1).max(3),
  novelty_level: z.number().int().min(1).max(3),
});
*/
```

---

## 環境変数

```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Failure Bank
```

---

## 開発ガイドライン

### コーディング規約
- TypeScript strict mode 有効化
- 1行の最大文字数: 100文字
- フォーマッター: Prettier（セミコロンあり、シングルクォート）
- 命名規則:
  - コンポーネント: PascalCase（例: `FailureCard.tsx`）
  - 関数/変数: camelCase（例: `getUserData`）
  - 定数: UPPER_SNAKE_CASE（例: `API_BASE_URL`）
  - 型: PascalCase（例: `User`, `FailureCreate`）

### コンポーネント設計原則
- **単一責任の原則**: 1つのコンポーネントは1つの責務のみ
- **再利用性**: 汎用的なコンポーネントは `components/common/` に配置
- **Props型定義**: すべてのPropsに型を定義
- **デフォルトProps**: 必要に応じてデフォルト値を設定

### パフォーマンス最適化
- 画像最適化（Next.js Image コンポーネント使用）
- コード分割（Dynamic Import）
- React.memo の適切な使用
- useMemo, useCallback の適切な使用

### セキュリティ
- XSS対策: ユーザー入力をエスケープ
- CSRF対策: トークンベース認証
- HTTPSのみでの通信（本番環境）
- 機密情報は環境変数で管理

---

## テスト戦略

### 単体テスト（Jest + React Testing Library）
- コンポーネントのレンダリングテスト
- ユーザーインタラクションのテスト
- APIモック（MSW推奨）

**テスト対象**
- すべてのフォームコンポーネント
- バリデーション関数
- カスタムフック
- ユーティリティ関数

### 統合テスト
- ページ全体の動作確認
- 認証フローのテスト
- API統合のテスト

### E2Eテスト（Phase 2）
- クリティカルパスのテスト
  - ユーザー登録 → ログイン → 失敗記録作成
  - 失敗記録の編集・削除

---

## CI/CD

### GitHub Actions

**トリガー**
- `main` ブランチへのpush
- `develop` ブランチへのpush
- Pull Request作成時

**実行内容**
1. **Lint**: ESLint実行
2. **Format Check**: Prettier チェック
3. **Type Check**: TypeScript コンパイル
4. **Test**: Jest 実行
5. **Build**: Next.js ビルド

### Vercel デプロイ
- `main` ブランチマージ時に自動デプロイ
- プレビュー環境: PR作成時に自動生成

---

## ロードマップ

### MVP Phase（Phase 1）
- [x] 認証機能（登録・ログイン・ログアウト）
- [ ] 失敗記録CRUD
- [ ] ダッシュボード
- [ ] 統計・可視化（累積カウンター、カレンダー、グラフ）

### Phase 2
- [ ] 通知設定
- [ ] プロフィール編集
- [ ] パスワードリセット
- [ ] タグ・カテゴリ機能
- [ ] 検索機能
- [ ] エクスポート機能（CSV、JSON）

### Phase 3
- [ ] ダークモード
- [ ] 多言語対応（i18n）
- [ ] PWA対応（オフライン機能、インストール可能）
- [ ] ソーシャル機能（失敗の共有）
- [ ] AI分析・アドバイス生成

---

## 参考リンク

- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [React公式ドキュメント](https://react.dev/)
- [Tailwind CSS公式ドキュメント](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)

---

**Last Updated**: 2024-01-XX

このドキュメントはプロジェクトの進行に合わせて随時更新してください。
