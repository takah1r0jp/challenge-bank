"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PeriodStats } from "@/lib/types";

/**
 * 統計カードのProps
 */
interface StatsCardProps {
  title: string; // カードのタイトル（例: "今日", "今週", "全期間"）
  stats: PeriodStats; // 統計データ
  icon?: React.ReactNode; // アイコン（オプション）
  delay?: number; // アニメーション遅延（オプション）
}

/**
 * 統計カードコンポーネント
 * Material Design 3準拠
 * - エレベーション: Level 1 (rest) → Level 2 (hover)
 * - Shape: Medium corner radius (12px)
 * - Motion: Standard easing curve with appropriate duration
 * - Typography: Display Small for primary metric
 * - State layers: Hover effect with surface tint
 */
export function StatsCard({ title, stats, icon, delay = 0 }: StatsCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.4,
        delay,
        ease: [0.4, 0, 0.2, 1], // Material Design 3: Standard easing
      }}
      whileHover={{
        y: -4,
        transition: {
          duration: 0.2,
          ease: [0.4, 0, 0.2, 1],
        },
      }}
    >
      <Card
        className="relative overflow-hidden rounded-xl border-0 bg-white shadow-md transition-shadow duration-200 hover:shadow-lg"
        style={{
          // Material Design 3: Elevation Level 1
          boxShadow: "0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)",
        }}
      >
        {/* State Layer for hover */}
        <motion.div
          className="absolute inset-0 bg-blue-500"
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 0.05 }}
          transition={{ duration: 0.2 }}
        />

        <CardHeader className="relative flex flex-row items-center justify-between space-y-0 pb-3">
          {/* Material Design 3: Label Medium */}
          <CardTitle className="text-sm font-medium tracking-wide text-gray-600">
            {title}
          </CardTitle>
          {icon && (
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-50">
              <div className="text-blue-600">{icon}</div>
            </div>
          )}
        </CardHeader>

        <CardContent className="relative">
          {/* Material Design 3: Display Small - Primary metric (total_score) */}
          <div className="mb-4">
            <div className="text-4xl font-bold tracking-tight text-gray-900">
              {stats.total_score}
              <span className="ml-1 text-2xl font-normal text-gray-500">点</span>
            </div>
          </div>

          {/* Material Design 3: Body Small - Secondary metrics */}
          <div className="mb-4 flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="text-gray-500">挑戦数</span>
              <span className="font-semibold text-gray-900">{stats.challenge_count}</span>
              <span className="text-gray-500">回</span>
            </div>
            <div className="h-3 w-px bg-gray-200" />
            <div className="flex items-center gap-1.5">
              <span className="text-gray-500">平均</span>
              <span className="font-semibold text-gray-900">
                {stats.average_score.toFixed(1)}
              </span>
              <span className="text-gray-500">点</span>
            </div>
          </div>

          {/* Material Design 3: Linear Progress Indicator */}
          <div className="relative">
            <div className="h-1 w-full overflow-hidden rounded-full bg-gray-100">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-blue-500 to-blue-600"
                initial={{ width: 0 }}
                animate={{
                  width: `${Math.min((stats.total_score / 100) * 100, 100)}%`,
                }}
                transition={{
                  duration: 1,
                  delay: delay + 0.3,
                  ease: [0.4, 0, 0.2, 1], // Material Design 3: Standard easing
                }}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
