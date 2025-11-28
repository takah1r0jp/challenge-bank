"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, CalendarStats, DayStats } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartSkeleton } from "./ChartSkeleton";
import { Calendar } from "lucide-react";

interface HeatmapDay {
  date: string;
  count: number;
  displayDate: string;
}

/**
 * カレンダーヒートマップ
 * GitHub風の貢献カレンダー
 * Material Design 3: トーナルカラー、マイクロインタラクション
 */
export function CalendarHeatmap() {
  const [data, setData] = useState<HeatmapDay[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [hoveredDay, setHoveredDay] = useState<HeatmapDay | null>(null);
  const [currentMonth, setCurrentMonth] = useState<{ year: number; month: number }>({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const { year, month } = currentMonth;

        const response = await apiClient.get<ApiResponse<CalendarStats>>(
          `/stats/calendar?year=${year}&month=${month}`
        );

        const days = response.data.data.days || [];
        const heatmapData = days.map((day: DayStats) => {
          const dateObj = new Date(day.date);
          return {
            date: day.date,
            count: day.challenge_count,
            displayDate: `${dateObj.getMonth() + 1}/${dateObj.getDate()}`,
          };
        });

        setData(heatmapData);
      } catch (error) {
        console.error("Failed to fetch calendar data:", getErrorMessage(error));
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [currentMonth]);

  // 色の濃淡を計算（Material Design 3のトーナルカラー）
  const getColor = (count: number): string => {
    if (count === 0) return "bg-gray-100";
    if (count === 1) return "bg-blue-200";
    if (count === 2) return "bg-blue-300";
    if (count === 3) return "bg-blue-400";
    if (count >= 4) return "bg-blue-600";
    return "bg-gray-100";
  };

  // 月のカレンダーグリッドを生成
  const generateCalendarGrid = (): (HeatmapDay | null)[][] => {
    if (data.length === 0) return [];

    const { year, month } = currentMonth;
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    const startDayOfWeek = firstDay.getDay(); // 0 = Sunday
    const daysInMonth = lastDay.getDate();

    const weeks: (HeatmapDay | null)[][] = [];
    let currentWeek: (HeatmapDay | null)[] = [];

    // 最初の週の空白を埋める
    for (let i = 0; i < startDayOfWeek; i++) {
      currentWeek.push(null);
    }

    // 日付を埋める
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
      const dayData = data.find((d) => d.date === dateStr);

      currentWeek.push(
        dayData || {
          date: dateStr,
          count: 0,
          displayDate: `${month}/${day}`,
        }
      );

      if (currentWeek.length === 7) {
        weeks.push(currentWeek);
        currentWeek = [];
      }
    }

    // 最後の週の空白を埋める
    if (currentWeek.length > 0) {
      while (currentWeek.length < 7) {
        currentWeek.push(null);
      }
      weeks.push(currentWeek);
    }

    return weeks;
  };

  if (isLoading) {
    return <ChartSkeleton />;
  }

  const weeks = generateCalendarGrid();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
    >
      <Card className="shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Calendar className="h-5 w-5 text-green-600" />
            活動カレンダー
          </CardTitle>
          <p className="text-sm text-gray-500">
            {currentMonth.year}年{currentMonth.month}月の記録状況
          </p>
        </CardHeader>
        <CardContent>
          {/* 曜日ヘッダー */}
          <div className="mb-2 grid grid-cols-7 gap-2 text-center text-xs text-gray-500">
            <div>日</div>
            <div>月</div>
            <div>火</div>
            <div>水</div>
            <div>木</div>
            <div>金</div>
            <div>土</div>
          </div>

          {/* カレンダーグリッド */}
          <div className="space-y-2">
            {weeks.map((week, weekIndex) => (
              <div key={weekIndex} className="grid grid-cols-7 gap-2">
                {week.map((day, dayIndex) => (
                  <motion.div
                    key={dayIndex}
                    className={`relative aspect-square rounded-md ${
                      day ? getColor(day.count) : "bg-transparent"
                    } transition-all duration-200 hover:scale-110 hover:shadow-lg ${
                      day ? "cursor-pointer" : ""
                    }`}
                    onMouseEnter={() => day && setHoveredDay(day)}
                    onMouseLeave={() => setHoveredDay(null)}
                    whileHover={{ scale: day ? 1.1 : 1 }}
                  >
                    {day && (
                      <div className="flex h-full items-center justify-center text-xs font-medium text-gray-700">
                        {new Date(day.date).getDate()}
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            ))}
          </div>

          {/* ツールチップ（ホバー時） */}
          {hoveredDay && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 rounded-lg bg-blue-50 p-3 text-sm"
            >
              <div className="font-medium text-gray-900">{hoveredDay.displayDate}</div>
              <div className="text-gray-600">{hoveredDay.count}回の記録</div>
            </motion.div>
          )}

          {/* 凡例 */}
          <div className="mt-4 flex items-center justify-end gap-2 text-xs text-gray-500">
            <span>少</span>
            <div className="flex gap-1">
              <div className="h-3 w-3 rounded-sm bg-gray-100" />
              <div className="h-3 w-3 rounded-sm bg-blue-200" />
              <div className="h-3 w-3 rounded-sm bg-blue-300" />
              <div className="h-3 w-3 rounded-sm bg-blue-400" />
              <div className="h-3 w-3 rounded-sm bg-blue-600" />
            </div>
            <span>多</span>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
