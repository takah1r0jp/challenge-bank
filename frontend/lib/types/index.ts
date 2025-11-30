// ========== 認証関連の型 ==========

/**
 * ユーザー情報
 * バックエンドのUserモデルに対応
 */
export interface User {
  id: string;
  email: string;
  notification_time?: string; // "HH:MM" 形式（例: "20:00"）
  is_notification_setup_completed: boolean; // 通知設定完了フラグ
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

// ========== Challenge関連の型（MVP版） ==========

/**
 * Challenge型（MVP版：contentとscoreのみ）
 * バックエンドのChallengeモデルに対応
 */
export interface Challenge {
  id: string;
  user_id: string;
  content: string; // 挑戦内容（MVP版では1つのフィールドに統合）
  score: number; // 1-5のスコア（挑戦度や学びの大きさ）
  created_at: string;
}

/**
 * Challenge作成用型（MVP版）
 * POST /challenges のリクエストボディ
 */
export interface ChallengeCreate {
  content: string;
  score: number; // 1-5
}

/**
 * Challenge更新用型（MVP版）
 * PUT /challenges/{id} のリクエストボディ
 * すべてのフィールドがオプション（部分更新可能）
 */
export interface ChallengeUpdate {
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
    details?: unknown;
  };
}

// ========== 統計関連の型（MVP版） ==========

/**
 * 期間別統計
 * 挑戦記録の数、合計スコア、平均スコアを含む
 */
export interface PeriodStats {
  challenge_count: number;
  total_score: number;
  average_score: number;
}

/**
 * 統計サマリー
 * GET /stats/summary のレスポンス
 * 今日、今週、全期間の統計を含む
 */
export interface StatsSummary {
  today: PeriodStats;
  this_week: PeriodStats;
  all_time: PeriodStats;
}

/**
 * カレンダー日別データ
 * 特定の日の挑戦記録の統計
 */
export interface DayStats {
  date: string; // "YYYY-MM-DD" 形式
  challenge_count: number;
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
export interface ChallengeExtended {
  id: string;
  user_id: string;
  challenge_content: string;
  challenge_content: string;
  next_action: string;
  challenge_level: 1 | 2 | 3;
  novelty_level: 1 | 2 | 3;
  created_at: string;
  updated_at: string;
}
*/
