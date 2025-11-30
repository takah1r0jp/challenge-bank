/**
 * タイムゾーン変換ユーティリティ
 *
 * このアプリケーションでは：
 * - データベース: UTC（タイムゾーン情報なし）で保存
 * - UI表示: JST（日本標準時、UTC+9）
 *
 * バックエンドのパターン（main.py lines 529-530）に倣った実装：
 * created_at_jst = challenge.created_at.replace(tzinfo=timezone.utc).astimezone(jst)
 * date_str = created_at_jst.strftime("%Y-%m-%d")
 */

// JST（日本標準時）のオフセット: UTC+9時間
const JST_OFFSET_MS = 9 * 60 * 60 * 1000;

/**
 * UTC ISO文字列をJST日付文字列（YYYY-MM-DD）に変換
 *
 * バックエンドの変換ロジックと同じ動作を保証：
 * - UTC naive datetime → UTC aware → JST aware → 日付文字列
 *
 * @param utcIsoString - UTC ISO 8601文字列（例: "2024-01-01T15:30:00"）
 * @returns JST日付文字列（例: "2024-01-02"）
 *
 * @example
 * getJstDateString("2024-01-01T15:30:00") // "2024-01-02" (JSTでは翌日)
 * getJstDateString("2024-01-01T14:59:59") // "2024-01-01" (まだ同じ日)
 */
export function getJstDateString(utcIsoString: string): string {
  const utcDate = new Date(utcIsoString);

  // UTCタイムスタンプにJSTオフセットを加算してJST時刻を計算
  const jstDate = new Date(utcDate.getTime() + JST_OFFSET_MS);

  // UTC基準でyear/month/dayを取得（JSTオフセット済みなので実質JST日付）
  const year = jstDate.getUTCFullYear();
  const month = String(jstDate.getUTCMonth() + 1).padStart(2, '0');
  const day = String(jstDate.getUTCDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

/**
 * 今週の開始日（JST基準）を取得
 *
 * @param weekStartDay - 週の開始曜日（0=日曜, 1=月曜, ..., 6=土曜）
 * @returns JST基準の今週開始日（00:00:00）のDateオブジェクト
 *
 * @example
 * // 日曜日始まり（デフォルト）
 * getCurrentWeekStartJst(0)
 *
 * // 月曜日始まり
 * getCurrentWeekStartJst(1)
 */
export function getCurrentWeekStartJst(weekStartDay: number = 0): Date {
  const now = new Date();

  // 現在時刻をJSTに変換
  const jstNow = new Date(now.getTime() + JST_OFFSET_MS);

  // JST基準の曜日を取得（0=日曜 ~ 6=土曜）
  const currentDayOfWeek = jstNow.getUTCDay();

  // 週の開始日からの経過日数を計算
  const daysFromWeekStart = (currentDayOfWeek - weekStartDay + 7) % 7;

  // 今週の開始日を計算
  const weekStart = new Date(jstNow);
  weekStart.setUTCDate(jstNow.getUTCDate() - daysFromWeekStart);
  weekStart.setUTCHours(0, 0, 0, 0);

  return weekStart;
}

/**
 * 今週の終了日（JST基準）を取得
 *
 * @param weekStartDay - 週の開始曜日（0=日曜, 1=月曜, ..., 6=土曜）
 * @returns JST基準の今週終了日（23:59:59.999）のDateオブジェクト
 *
 * @example
 * // 日曜日始まり → 土曜日終わり
 * getCurrentWeekEndJst(0)
 *
 * // 月曜日始まり → 日曜日終わり
 * getCurrentWeekEndJst(1)
 */
export function getCurrentWeekEndJst(weekStartDay: number = 0): Date {
  const weekStart = getCurrentWeekStartJst(weekStartDay);
  const weekEnd = new Date(weekStart);

  // 週の開始から6日後（7日目の最後）
  weekEnd.setUTCDate(weekStart.getUTCDate() + 6);
  weekEnd.setUTCHours(23, 59, 59, 999);

  return weekEnd;
}

/**
 * UTC ISO文字列が今週（JST基準）に含まれるか判定
 *
 * @param utcIsoString - UTC ISO 8601文字列
 * @param weekStartDay - 週の開始曜日（0=日曜, 1=月曜, ..., 6=土曜）
 * @returns 今週に含まれる場合true
 *
 * @example
 * // 日曜日始まりの今週に含まれるか
 * isInCurrentWeekJst("2024-01-01T15:30:00", 0)
 */
export function isInCurrentWeekJst(
  utcIsoString: string,
  weekStartDay: number = 0
): boolean {
  const challengeDate = new Date(utcIsoString);

  // UTC時刻をJSTに変換
  const jstChallengeDate = new Date(challengeDate.getTime() + JST_OFFSET_MS);

  const weekStart = getCurrentWeekStartJst(weekStartDay);
  const weekEnd = getCurrentWeekEndJst(weekStartDay);

  return jstChallengeDate >= weekStart && jstChallengeDate <= weekEnd;
}

/**
 * 今週の指定曜日のJST日付文字列を取得
 *
 * チャート表示用に、今週の各曜日（日〜土）の日付文字列を生成
 *
 * @param dayOfWeek - 取得したい曜日（0=日曜 ~ 6=土曜）
 * @param weekStartDay - 週の開始曜日（0=日曜, 1=月曜, ..., 6=土曜）
 * @returns YYYY-MM-DD形式の日付文字列
 *
 * @example
 * // 日曜日始まりの週の各曜日
 * getWeekDayDateString(0, 0) // 今週の日曜日
 * getWeekDayDateString(1, 0) // 今週の月曜日
 * getWeekDayDateString(6, 0) // 今週の土曜日
 */
export function getWeekDayDateString(
  dayOfWeek: number,
  weekStartDay: number = 0
): string {
  const weekStart = getCurrentWeekStartJst(weekStartDay);
  const targetDate = new Date(weekStart);

  // 週の開始日から指定曜日までの日数を加算
  targetDate.setUTCDate(weekStart.getUTCDate() + dayOfWeek);

  const year = targetDate.getUTCFullYear();
  const month = String(targetDate.getUTCMonth() + 1).padStart(2, '0');
  const day = String(targetDate.getUTCDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}
