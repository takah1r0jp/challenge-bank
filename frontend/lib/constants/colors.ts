/**
 * Material Design 3カラーパレット
 *
 * アプリケーション全体で使用するスコア関連の色定義
 * スコア1-5に対応するトーナルカラー
 */

export const SCORE_COLORS = {
  1: "#10b981", // Green
  2: "#f59e0b", // Amber
  3: "#ec4899", // Pink
  4: "#8b5cf6", // Purple
  5: "#3b82f6", // Blue
} as const;

/**
 * スコア配列（1-5）
 */
export const SCORE_RANGE = [1, 2, 3, 4, 5] as const;

/**
 * スコアに対応する色を取得
 */
export function getScoreColor(score: number): string {
  return SCORE_COLORS[score as keyof typeof SCORE_COLORS] || SCORE_COLORS[1];
}
