import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PeriodStats } from "@/lib/types";

/**
 * 統計カードのProps
 */
interface StatsCardProps {
  title: string; // カードのタイトル（例: "全期間", "今週", "今月"）
  stats: PeriodStats; // 統計データ
  icon?: React.ReactNode; // アイコン（オプション）
}

/**
 * 統計カードコンポーネント
 * 失敗記録数、合計スコア、平均スコアを表示
 */
export function StatsCard({ title, stats, icon }: StatsCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon && <div className="text-gray-400">{icon}</div>}
      </CardHeader>
      <CardContent>
        {/* 失敗記録数（大きく表示） */}
        <div className="text-2xl font-bold">{stats.failure_count}回</div>

        {/* 合計スコアと平均スコア */}
        <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
          <div>
            合計: <span className="font-medium text-gray-700">{stats.total_score}点</span>
          </div>
          <div>
            平均:{" "}
            <span className="font-medium text-gray-700">
              {stats.average_score.toFixed(1)}点
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
