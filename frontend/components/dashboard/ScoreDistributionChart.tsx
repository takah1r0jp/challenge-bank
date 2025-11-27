"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, Failure } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartSkeleton } from "./ChartSkeleton";
import { PieChartIcon } from "lucide-react";

interface ScoreDistribution {
  score: number;
  count: number;
  percentage: number;
}

// Material Design 3のカラーパレット（トーナルカラー）
const COLORS = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"];

/**
 * スコア分布チャート
 * 失敗記録のスコア（1-5点）の分布を円グラフで可視化
 * Material Design 3: トーナルカラー、レスポンシブデザイン
 */
export function ScoreDistributionChart() {
  const [data, setData] = useState<ScoreDistribution[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [mostCommonScore, setMostCommonScore] = useState<number | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        // 最新100件の失敗記録を取得
        const response = await apiClient.get<ApiResponse<Failure[]>>(
          "/failures?limit=100"
        );

        const failures = response.data.data || [];

        // スコア別にカウント
        const scoreCounts = new Map<number, number>();
        for (let i = 1; i <= 5; i++) {
          scoreCounts.set(i, 0);
        }

        failures.forEach((failure) => {
          const score = failure.score;
          scoreCounts.set(score, (scoreCounts.get(score) || 0) + 1);
        });

        // 合計数を計算
        const total = failures.length;

        // データ整形
        const distribution: ScoreDistribution[] = [];
        let maxCount = 0;
        let maxScore = 1;

        for (let score = 1; score <= 5; score++) {
          const count = scoreCounts.get(score) || 0;
          if (count > maxCount) {
            maxCount = count;
            maxScore = score;
          }
          distribution.push({
            score,
            count,
            percentage: total > 0 ? (count / total) * 100 : 0,
          });
        }

        setData(distribution.filter((d) => d.count > 0)); // カウントが0のスコアは除外
        setMostCommonScore(maxCount > 0 ? maxScore : null);
      } catch (error) {
        console.error("Failed to fetch failures:", getErrorMessage(error));
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, []);

  if (isLoading) {
    return <ChartSkeleton />;
  }

  if (data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <PieChartIcon className="h-5 w-5 text-purple-600" />
            スコア分布
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-[300px] items-center justify-center">
            <p className="text-sm text-gray-400">データがありません</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // カスタムラベル（Material Design 3: タイポグラフィ）
  const renderCustomLabel = (entry: any) => {
    return `${entry.percentage.toFixed(0)}%`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
    >
      <Card className="shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <PieChartIcon className="h-5 w-5 text-purple-600" />
            スコア分布
          </CardTitle>
          <p className="text-sm text-gray-500">
            最新100件のチャレンジレベル（最多: {mostCommonScore}点）
          </p>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomLabel}
                outerRadius={100}
                innerRadius={60}
                fill="#8884d8"
                dataKey="count"
                animationBegin={0}
                animationDuration={800}
                animationEasing="ease-out"
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                    stroke="white"
                    strokeWidth={2}
                  />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255, 255, 255, 0.95)",
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px",
                  boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                  padding: "8px 12px",
                }}
                formatter={(value: number, name: string, entry: any) => [
                  `${value}回 (${entry.payload.percentage.toFixed(1)}%)`,
                  `${entry.payload.score}点`,
                ]}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                formatter={(value, entry: any) => `${entry.payload.score}点`}
                iconType="circle"
                wrapperStyle={{
                  fontSize: "14px",
                  paddingTop: "16px",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </motion.div>
  );
}
