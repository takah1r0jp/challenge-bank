"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import type { PieLabelRenderProps, LegendPayload } from "recharts";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, Challenge } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartSkeleton } from "./ChartSkeleton";
import { PieChartIcon } from "lucide-react";
import { getScoreColor } from "@/lib/constants/colors";

interface ScoreDistribution {
  score: number;
  count: number;
  percentage: number;
  [key: string]: number; // Recharts互換のためのインデックスシグネチャ
}

/**
 * スコア分布チャート
 * 挑戦記録のスコア（1-5点）の分布を円グラフで可視化
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
        // 最新100件の挑戦記録を取得
        const response = await apiClient.get<ApiResponse<Challenge[]>>(
          "/challenges?limit=100"
        );

        const challenges = response.data.data || [];

        // スコア別にカウント
        const scoreCounts = new Map<number, number>();
        for (let i = 1; i <= 5; i++) {
          scoreCounts.set(i, 0);
        }

        challenges.forEach((challenge) => {
          const score = challenge.score;
          scoreCounts.set(score, (scoreCounts.get(score) || 0) + 1);
        });

        // 合計数を計算
        const total = challenges.length;

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
        console.error("Failed to fetch challenges:", getErrorMessage(error));
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
  const renderCustomLabel = (props: PieLabelRenderProps) => {
    // PieLabelRenderProps は `percent` (0..1) と `payload` (original data)を提供する.
    // Prefer 提供されたpercentが利用可能であればそれを使い、そうでなければpayload.percentageを使う.
    const percentFromProps = typeof props?.percent === "number" ? props.percent * 100 : undefined;
    const percentFromPayload = typeof props?.payload?.percentage === "number" ? props.payload.percentage : undefined;
    const pct = percentFromProps ?? percentFromPayload ?? 0;
    return `${Math.round(pct)}%`;
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
            最新100件のチャレンジスコア（最多: {mostCommonScore}点）
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
                {data.map((entry) => (
                  <Cell
                    key={`cell-${entry.score}`}
                    fill={getScoreColor(entry.score)}
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
                formatter={(
                  value: number,
                  name: string,
                  entry: { payload?: ScoreDistribution } | undefined
                ) => {
                  const percent = entry?.payload?.percentage;
                  const percentText = typeof percent === "number" ? `${percent.toFixed(1)}%` : "-";
                  const score = entry?.payload?.score ?? "-";
                  return [`${value}回 (${percentText})`, `${score}点`];
                }}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                formatter={(
                  value: string | number | undefined,
                  entry: LegendPayload | undefined
                ) => {
                  // LegendPayload.payload はチャートによって異なる型になる可能性があるため、ガードしてスコアを抽出
                  const payload = entry?.payload as unknown;
                  const hasScore =
                    typeof payload === "object" && payload !== null && "score" in (payload as Record<string, unknown>);
                  const score = hasScore ? (payload as ScoreDistribution).score : "-";
                  return `${score}点`;
                }}
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
