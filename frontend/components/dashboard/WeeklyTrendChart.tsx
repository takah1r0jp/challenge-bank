"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, Challenge } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  getJstDateString,
  isInCurrentWeekJst,
  getWeekDayDateString,
} from "@/lib/utils/timezone";
import { ChartSkeleton } from "./ChartSkeleton";
import { TrendingUp } from "lucide-react";
import { SCORE_COLORS, SCORE_RANGE } from "@/lib/constants/colors";

interface ChartDataPoint {
  date: string;
  displayDate: string;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  score5: number;
}

/**
 * 週次トレンドチャート
 * 今週（日曜始まり〜土曜終わり）の合計スコアをスコア別に色分けした積み上げ棒グラフで視覚化
 * Material Design 3: Material You colors, スムーズなアニメーション
 */
export function WeeklyTrendChart() {
  const [data, setData] = useState<ChartDataPoint[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);

        // 挑戦記録を取得（最新100件）
        const challengesResponse = await apiClient.get<ApiResponse<Challenge[]>>(
          "/challenges?limit=100"
        );
        const challenges = challengesResponse.data.data || [];

        // 今週のデータのみフィルタリング（JST基準、日曜始まり）
        const thisWeekChallenges = challenges.filter((challenge) =>
          isInCurrentWeekJst(challenge.created_at, 0)
        );

        // 日付ごとにグループ化（JST日付文字列を使用）
        const dailyScores = new Map<string, Map<number, number>>();

        thisWeekChallenges.forEach((challenge) => {
          const dateStr = getJstDateString(challenge.created_at);

          if (!dailyScores.has(dateStr)) {
            dailyScores.set(dateStr, new Map());
          }

          const scoreMap = dailyScores.get(dateStr)!;
          scoreMap.set(challenge.score, (scoreMap.get(challenge.score) || 0) + 1);
        });

        // 今週の7日分（日曜〜土曜）のデータを作成
        const chartData: ChartDataPoint[] = [];
        const weekDays = ["日", "月", "火", "水", "木", "金", "土"];

        for (let i = 0; i < 7; i++) {
          const dateStr = getWeekDayDateString(i, 0); // 0 = 日曜始まり
          const scoreMap = dailyScores.get(dateStr) || new Map();

          chartData.push({
            date: dateStr,
            displayDate: weekDays[i],
            score1: (scoreMap.get(1) || 0) * 1,
            score2: (scoreMap.get(2) || 0) * 2,
            score3: (scoreMap.get(3) || 0) * 3,
            score4: (scoreMap.get(4) || 0) * 4,
            score5: (scoreMap.get(5) || 0) * 5,
          });
        }

        setData(chartData);
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

  // データが0件でも7日分の枠は表示するため、このチェックは不要
  // if (data.length === 0) { ... }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <Card className="shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <TrendingUp className="h-5 w-5 text-blue-600" />
            今週の記録
          </CardTitle>
          <p className="text-sm text-gray-500">日曜日〜土曜日のスコア推移</p>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={data}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              {/* グリッド線（Material Design 3: subtle） */}
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />

              {/* X軸 */}
              <XAxis
                dataKey="displayDate"
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: "#e5e7eb" }}
              />

              {/* Y軸 */}
              <YAxis
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: "#e5e7eb" }}
                allowDecimals={false}
              />

              {/* ツールチップ（Material Design 3: elevation） */}
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255, 255, 255, 0.95)",
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px",
                  boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                  padding: "8px 12px",
                }}
                labelStyle={{
                  color: "#374151",
                  fontWeight: 600,
                  marginBottom: "4px",
                }}
                formatter={(value: number, name: string) => {
                  const scoreLabel = name.replace("score", "");
                  return [`${value}点`, `スコア${scoreLabel}`];
                }}
              />

              {/* 積み上げ棒グラフ（Material Design 3: Tonal colors） */}
              <Bar
                dataKey="score5"
                stackId="a"
                fill={SCORE_COLORS[5]}
                animationDuration={800}
                animationEasing="ease-out"
              />
              <Bar
                dataKey="score4"
                stackId="a"
                fill={SCORE_COLORS[4]}
                animationDuration={800}
                animationEasing="ease-out"
              />
              <Bar
                dataKey="score3"
                stackId="a"
                fill={SCORE_COLORS[3]}
                animationDuration={800}
                animationEasing="ease-out"
              />
              <Bar
                dataKey="score2"
                stackId="a"
                fill={SCORE_COLORS[2]}
                animationDuration={800}
                animationEasing="ease-out"
              />
              <Bar
                dataKey="score1"
                stackId="a"
                fill={SCORE_COLORS[1]}
                animationDuration={800}
                animationEasing="ease-out"
              />
            </BarChart>
          </ResponsiveContainer>

          {/* 凡例（Material Design 3: Label Medium） */}
          <div className="mt-4 flex flex-wrap justify-center gap-3">
            {SCORE_RANGE.map((score) => (
              <div key={score} className="flex items-center gap-1.5">
                <div
                  className="h-3 w-3 rounded-full"
                  style={{ backgroundColor: SCORE_COLORS[score] }}
                />
                <span
                  className="text-xs"
                  style={{ color: SCORE_COLORS[score] }}
                >
                  {score}点
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
