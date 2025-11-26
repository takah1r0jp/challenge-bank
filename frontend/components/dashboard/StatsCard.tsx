"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PeriodStats } from "@/lib/types";

/**
 * 統計カードのProps
 */
interface StatsCardProps {
  title: string; // カードのタイトル（例: "全期間", "今週", "今月"）
  stats: PeriodStats; // 統計データ
  icon?: React.ReactNode; // アイコン（オプション）
  delay?: number; // アニメーション遅延（オプション）
}

/**
 * 統計カードコンポーネント
 * 失敗記録数、合計スコア、平均スコアを表示
 * Material Design 3: エレベーション、マイクロインタラクション
 */
export function StatsCard({ title, stats, icon, delay = 0 }: StatsCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: "easeOut" }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
    >
      <Card className="shadow-md transition-shadow hover:shadow-lg">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
          {icon && <div className="text-blue-500">{icon}</div>}
        </CardHeader>
        <CardContent>
          {/* 失敗記録数（大きく表示、Material Design 3: Emphasis） */}
          <div className="text-3xl font-bold text-gray-900">{stats.failure_count}回</div>

          {/* 合計スコアと平均スコア */}
          <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
            <div className="flex items-center gap-1">
              <span>合計:</span>
              <span className="font-semibold text-gray-700">{stats.total_score}点</span>
            </div>
            <div className="flex items-center gap-1">
              <span>平均:</span>
              <span className="font-semibold text-gray-700">
                {stats.average_score.toFixed(1)}点
              </span>
            </div>
          </div>

          {/* プログレスバー（Material Design 3: Tonal surface） */}
          <div className="mt-3">
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-gray-100">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-blue-500 to-blue-600"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min((stats.failure_count / 100) * 100, 100)}%` }}
                transition={{ duration: 1, delay: delay + 0.3, ease: "easeOut" }}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
