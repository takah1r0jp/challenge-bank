"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, CalendarStats, DayStats } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartSkeleton } from "./ChartSkeleton";
import { TrendingUp } from "lucide-react";

interface ChartDataPoint {
  date: string;
  failures: number;
  displayDate: string;
}

/**
 * 週次トレンドチャート
 * 過去7-14日の失敗記録数の推移を視覚化
 * Material Design 3: グラデーション、スムーズなアニメーション
 */
export function WeeklyTrendChart() {
  const [data, setData] = useState<ChartDataPoint[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth() + 1;

        const response = await apiClient.get<ApiResponse<CalendarStats>>(
          `/stats/calendar?year=${year}&month=${month}`
        );

        // 最新14日分を取得
        const days = response.data.data.days || [];
        const last14Days = days.slice(-14).map((day: DayStats) => {
          // 日付をMM/DD形式に変換
          const dateObj = new Date(day.date);
          const displayDate = `${dateObj.getMonth() + 1}/${dateObj.getDate()}`;

          return {
            date: day.date,
            failures: day.failure_count,
            displayDate,
          };
        });

        setData(last14Days);
      } catch (error) {
        console.error("Failed to fetch calendar data:", getErrorMessage(error));
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
            <TrendingUp className="h-5 w-5 text-blue-600" />
            週次トレンド
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
            週次トレンド
          </CardTitle>
          <p className="text-sm text-gray-500">過去14日間の記録推移</p>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart
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
                formatter={(value: number) => [`${value}回`, "失敗記録"]}
              />

              {/* グラデーション塗りつぶし（Material Design 3: tonal surface） */}
              <defs>
                <linearGradient id="colorFailures" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.05} />
                </linearGradient>
              </defs>

              <Area
                type="monotone"
                dataKey="failures"
                stroke="#3b82f6"
                strokeWidth={2.5}
                fill="url(#colorFailures)"
                animationDuration={1000}
                animationEasing="ease-in-out"
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </motion.div>
  );
}
