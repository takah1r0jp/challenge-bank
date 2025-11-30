"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/context/AuthContext";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { ApiResponse, StatsSummary, Challenge } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { ChallengeCard } from "@/components/dashboard/ChallengeCard";
import { EmptyState } from "@/components/dashboard/EmptyState";
import { WeeklyTrendChart } from "@/components/dashboard/WeeklyTrendChart";
import { ScoreDistributionChart } from "@/components/dashboard/ScoreDistributionChart";
import { CalendarHeatmap } from "@/components/dashboard/CalendarHeatmap";
import { NotificationSetupBanner } from "@/components/notifications/NotificationSetupBanner";
import { Plus, Clock, Calendar as CalendarIcon, TrendingUp, Sun } from "lucide-react";

/**
 * ダッシュボードページ
 * - 新しい挑戦を記録するボタン
 * - 統計サマリー（今日、今週、全期間）
 * - 最近の挑戦記録（直近5件）
 */
export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();

  // 統計データ
  const [stats, setStats] = useState<StatsSummary | null>(null);
  // 最近の挑戦記録
  const [recentChallenges, setRecentChallenges] = useState<Challenge[]>([]);
  // ローディング状態
  const [isLoading, setIsLoading] = useState(true);

  /**
   * 認証チェック
   * 未認証の場合はログインページへリダイレクト
   */
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  /**
   * データ取得
   * 統計サマリーと最近の挑戦記録を並列で取得
   */
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchData = async () => {
      try {
        setIsLoading(true);

        // 並列でAPIを呼び出し
        const [statsResponse, challengesResponse] = await Promise.all([
          apiClient.get<ApiResponse<StatsSummary>>("/stats/summary"),
          apiClient.get<ApiResponse<Challenge[]>>("/challenges?limit=5"),
        ]);

        setStats(statsResponse.data.data);
        setRecentChallenges(challengesResponse.data.data || []);
      } catch (error) {
        console.error("データ取得エラー:", getErrorMessage(error));
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [isAuthenticated]);

  // 認証チェック中
  if (authLoading || !isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">読み込み中...</p>
      </div>
    );
  }

  // データ読み込み中
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">データを読み込んでいます...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* ページタイトル + 新規作成ボタン */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">ダッシュボード</h1>
          <p className="mt-1 text-sm text-gray-500">
            あなたの挑戦の記録を確認しましょう
          </p>
        </div>
        <Link href="/challenges/new">
          <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
            <Plus className="mr-2 h-5 w-5" />
            新しい挑戦を記録
          </Button>
        </Link>
      </div>

      {/* 通知設定バナー */}
      {user && !user.is_notification_setup_completed && (
        <NotificationSetupBanner />
      )}

      {/* 統計サマリー */}
      {stats && (
        <div>
          <h2 className="mb-4 text-xl font-semibold text-gray-900">
            📊 統計サマリー
          </h2>
          <div className="grid gap-4 md:grid-cols-3">
            <StatsCard
              title="今日"
              stats={stats.today}
              icon={<Sun className="h-5 w-5" />}
              delay={0}
            />
            <StatsCard
              title="今週"
              stats={stats.this_week}
              icon={<Clock className="h-5 w-5" />}
              delay={0.1}
            />
            <StatsCard
              title="全期間"
              stats={stats.all_time}
              icon={<TrendingUp className="h-5 w-5" />}
              delay={0.2}
            />
          </div>
        </div>
      )}

      {/* アナリティクスチャート（Material Design 3） */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-gray-900">
          📈 アナリティクス
        </h2>
        <div className="grid gap-6 lg:grid-cols-2">
          <WeeklyTrendChart />
          <ScoreDistributionChart />
        </div>
      </div>

      {/* 活動カレンダー */}
      <div>
        <CalendarHeatmap />
      </div>

      {/* 最近の挑戦記録 */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">
            📝 最近の挑戦記録
          </h2>
          {recentChallenges && recentChallenges.length > 0 && (
            <Link href="/challenges" className="text-sm text-blue-600 hover:underline">
              すべて見る →
            </Link>
          )}
        </div>

        {/* 挑戦記録がない場合 */}
        {!recentChallenges || recentChallenges.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="space-y-3">
            {recentChallenges.map((challenge) => (
              <ChallengeCard key={challenge.id} challenge={challenge} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
