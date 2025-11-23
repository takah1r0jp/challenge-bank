// ========== 認証関連の型 ==========

/**
 * ユーザー情報
 * バックエンドのUserモデルに対応
 */
export interface User {
  id: string;
  email: string;
  notification_time?: string; // "HH:MM" 形式（例: "20:00"）
  created_at: string;
}

/**
 * トークン情報
 * ログイン・登録時にバックエンドから返される
 */
export interface Token {
  access_token: string;
  token_type: string;
}

/**
 * ユーザー登録・ログイン用の入力データ
 */
export interface AuthCredentials {
  email: string;
  password: string;
}

/**
 * ユーザー登録用の入力データ（確認パスワード付き）
 */
export interface RegisterCredentials extends AuthCredentials {
  confirmPassword: string;
}

// ========== Failure関連の型（MVP版） ==========

/**
 * Failure型（MVP版：contentとscoreのみ）
 * バックエンドのFailureモデルに対応
 */
export interface Failure {
  id: string;
  user_id: string;
  content: string; // 失敗内容（MVP版では1つのフィールドに統合）
  score: number; // 1-5のスコア（挑戦度や学びの大きさ）
  created_at: string;
}

/**
 * Failure作成用型（MVP版）
 * POST /failures のリクエストボディ
 */
export interface FailureCreate {
  content: string;
  score: number; // 1-5
}

/**
 * Failure更新用型（MVP版）
 * PUT /failures/{id} のリクエストボディ
 * すべてのフィールドがオプション（部分更新可能）
 */
export interface FailureUpdate {
  content?: string;
  score?: number; // 1-5
}

// ========== API レスポンス型 ==========

/**
 * 統一レスポンス型
 * バックエンドの全APIエンドポイントがこの形式で返す
 *
 * @example
 * {
 *   "success": true,
 *   "data": { "id": "123", "email": "user@example.com" },
 *   "message": "User created successfully"
 * }
 */
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

/**
 * エラーレスポンス型
 * バックエンドがエラー時に返す形式
 *
 * @example
 * {
 *   "success": false,
 *   "error": {
 *     "code": "UNAUTHORIZED",
 *     "message": "Invalid email or password",
 *     "details": null
 *   }
 * }
 */
export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

// ========== 統計関連の型（MVP版） ==========

/**
 * 期間別統計
 * 失敗記録の数、合計スコア、平均スコアを含む
 */
export interface PeriodStats {
  failure_count: number;
  total_score: number;
  average_score: number;
}

/**
 * 統計サマリー
 * GET /stats/summary のレスポンス
 * 全期間、今週、今月の統計を含む
 */
export interface StatsSummary {
  all_time: PeriodStats;
  this_week: PeriodStats;
  this_month: PeriodStats;
}

/**
 * カレンダー日別データ
 * 特定の日の失敗記録の統計
 */
export interface DayStats {
  date: string; // "YYYY-MM-DD" 形式
  failure_count: number;
  total_score: number;
  average_score: number;
}

/**
 * カレンダーレスポンス
 * GET /stats/calendar のレスポンス
 * 指定月の全日付の統計を含む
 */
export interface CalendarStats {
  year: number;
  month: number;
  days: DayStats[];
}

// ========== ユーティリティ型 ==========

/**
 * ページネーション用のクエリパラメータ
 */
export interface PaginationParams {
  limit?: number;
  offset?: number;
}

/**
 * ローディング状態を持つデータ型
 * カスタムフックで使用
 */
export interface AsyncData<T> {
  data: T | null;
  isLoading: boolean;
  error: string | null;
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
