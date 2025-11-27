/**
 * チャートローディングスケルトンコンポーネント
 * Material Design 3のプログレスインジケーターに基づくデザイン
 */
export function ChartSkeleton() {
  return (
    <div className="animate-pulse space-y-4">
      {/* タイトル部分 */}
      <div className="h-6 w-32 rounded-md bg-gray-200" />

      {/* チャート本体 */}
      <div className="h-[300px] w-full rounded-lg bg-gray-100">
        <div className="flex h-full items-center justify-center">
          <div className="text-center">
            {/* ローディングドット（Material Design 3風） */}
            <div className="flex items-center justify-center space-x-2">
              <div
                className="h-3 w-3 animate-bounce rounded-full bg-blue-400"
                style={{ animationDelay: "0ms" }}
              />
              <div
                className="h-3 w-3 animate-bounce rounded-full bg-blue-400"
                style={{ animationDelay: "150ms" }}
              />
              <div
                className="h-3 w-3 animate-bounce rounded-full bg-blue-400"
                style={{ animationDelay: "300ms" }}
              />
            </div>
            <p className="mt-3 text-sm text-gray-400">読み込み中...</p>
          </div>
        </div>
      </div>
    </div>
  );
}
