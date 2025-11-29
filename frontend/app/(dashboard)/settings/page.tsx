'use client';

import { useEffect, useState, useRef } from 'react';
import { useAuth } from '@/lib/context/AuthContext';
import { apiClient, getErrorMessage } from '@/lib/api/client';
import { ApiResponse, User } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';
import { toast } from 'react-hot-toast';
import { Clock, Save, Loader2 } from 'lucide-react';

export default function SettingsPage() {
  const { user, isLoading: authLoading, updateUser } = useAuth();
  const [selectedHour, setSelectedHour] = useState<number>(20); // デフォルト20時
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [savedNotificationTime, setSavedNotificationTime] = useState<string>('');
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // 24時間の選択肢を生成（上下にパディング用の空要素を追加）
  const hours = Array.from({ length: 24 }, (_, i) => i);

  // 初期値の設定：ユーザー情報から通知時刻を取得
  useEffect(() => {
    if (user?.notification_time) {
      // "HH:MM" 形式から時間部分を取得
      const hour = parseInt(user.notification_time.split(':')[0], 10);
      setSelectedHour(hour);
      setSavedNotificationTime(user.notification_time);

      // 初期スクロール位置を設定
      setTimeout(() => {
        scrollToHour(hour, false);
      }, 100);
    }
  }, [user]);

  // 特定の時刻にスクロール
  const scrollToHour = (hour: number, smooth: boolean = true) => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const itemHeight = 60; // 各アイテムの高さ
    const scrollPosition = hour * itemHeight;

    container.scrollTo({
      top: scrollPosition,
      behavior: smooth ? 'smooth' : 'auto',
    });
  };

  // スクロールイベントハンドラ：中央の時刻を選択
  const handleScroll = () => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const itemHeight = 60;
    const scrollTop = container.scrollTop;
    const centerIndex = Math.round(scrollTop / itemHeight);

    if (centerIndex >= 0 && centerIndex < 24) {
      setSelectedHour(centerIndex);
    }
  };

  // バリデーション
  const validateTime = (): boolean => {
    if (selectedHour < 0 || selectedHour > 23) {
      setError('有効な時刻を選択してください');
      return false;
    }

    setError('');
    return true;
  };

  // フォーム送信ハンドラ
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // バリデーション
    if (!validateTime()) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // HH:MM形式に変換
      const notificationTime = `${selectedHour.toString().padStart(2, '0')}:00`;

      // PUT /auth/me APIで通知時刻と設定完了フラグを更新
      const response = await apiClient.put<ApiResponse<User>>('/auth/me', {
        notification_time: notificationTime,
        is_notification_setup_completed: true,
      });

      // 保存済みの設定を更新
      setSavedNotificationTime(notificationTime);

      // AuthContext のユーザー情報も更新して、ダッシュボードのバナー表示条件を即時反映させる
      // APIから返却された最新ユーザー情報で上書きする
      if (response?.data?.data && updateUser) {
        updateUser(response.data.data);
      }

      // 成功時のトースト通知
      toast.success('通知時刻を更新しました', {
        duration: 3000,
        icon: '✅',
      });

      console.log('Updated user:', response.data.data);
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      toast.error(`更新に失敗しました: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  // 認証チェック中
  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-8 px-4">
      <div className="mx-auto max-w-2xl">
        {/* ページタイトル */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">設定</h1>
          <p className="mt-2 text-sm text-gray-600">
            アプリの各種設定を管理できます
          </p>
        </div>

        {/* 通知設定カード */}
        <Card className="shadow-md hover:shadow-lg transition-shadow duration-200">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-primary/10 p-2">
                <Clock className="h-5 w-5 text-primary" />
              </div>
              <div>
                <CardTitle className="text-xl">通知設定</CardTitle>
                <CardDescription className="mt-1">
                  日次リマインダーの通知時刻を設定できます
                </CardDescription>
              </div>
            </div>
          </CardHeader>

          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-6">
              {/* 通知時刻選択 */}
              <div className="space-y-3">
                <Label className="text-base font-medium">
                  通知時刻（1時間単位）
                </Label>

                {/* スクロール式時刻ピッカー */}
                <div className="relative">
                  {/* 中央選択エリアのハイライト */}
                  <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-[60px] pointer-events-none z-10">
                    <div className="h-full bg-primary/10 border-y-2 border-primary rounded-lg shadow-inner" />
                  </div>

                  {/* スクロールコンテナ */}
                  <div
                    ref={scrollContainerRef}
                    onScroll={handleScroll}
                    className="h-[180px] overflow-y-scroll snap-y snap-mandatory scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent hover:scrollbar-thumb-primary/40 relative"
                    style={{
                      scrollbarWidth: 'thin',
                    }}
                  >
                    {/* 上部パディング */}
                    <div className="h-[60px]" />

                    {/* 時刻リスト */}
                    {hours.map((hour) => {
                      const isSelected = selectedHour === hour;
                      return (
                        <div
                          key={hour}
                          onClick={() => {
                            setSelectedHour(hour);
                            scrollToHour(hour);
                          }}
                          className={`
                            h-[60px] flex items-center justify-center cursor-pointer
                            snap-center transition-all duration-200
                            ${
                              isSelected
                                ? 'text-primary text-3xl font-bold scale-110'
                                : 'text-muted-foreground text-xl font-medium hover:text-foreground hover:scale-105'
                            }
                          `}
                        >
                          {hour.toString().padStart(2, '0')}:00
                        </div>
                      );
                    })}

                    {/* 下部パディング */}
                    <div className="h-[60px]" />
                  </div>

                  {/* グラデーション効果（上下のフェードアウト） */}
                  <div className="absolute top-0 left-0 right-0 h-[60px] bg-gradient-to-b from-card to-transparent pointer-events-none" />
                  <div className="absolute bottom-0 left-0 right-0 h-[60px] bg-gradient-to-t from-card to-transparent pointer-events-none" />
                </div>

                {/* ヒントテキスト */}
                {!error && (
                  <p id="time-hint" className="text-sm text-muted-foreground text-center">
                    スクロールまたはタップして通知時刻を選択してください
                  </p>
                )}

                {/* エラーメッセージ */}
                {error && (
                  <p id="time-error" className="text-sm text-destructive flex items-center justify-center gap-1">
                    <span className="inline-block h-4 w-4">⚠️</span>
                    {error}
                  </p>
                )}
              </div>

              {/* 現在の設定値表示 */}
              {savedNotificationTime && (
                <div className="rounded-lg bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 p-4">
                  <p className="text-sm text-blue-900 dark:text-blue-100 text-center">
                    <span className="font-medium">保存済みの設定:</span>{' '}
                    <span className="font-semibold">{savedNotificationTime}</span>
                  </p>
                </div>
              )}
            </CardContent>

            <CardFooter className="flex justify-end gap-3 border-t pt-6">
              {/* 保存ボタン */}
              <Button
                type="submit"
                disabled={isLoading || selectedHour === null || selectedHour === undefined}
                className="min-w-[120px]"
                size="lg"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    保存中...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    保存する
                  </>
                )}
              </Button>
            </CardFooter>
          </form>
        </Card>

        {/* 将来の拡張用プレースホルダー */}
        <div className="mt-6 rounded-lg border-2 border-dashed border-gray-300 p-8 text-center">
          <p className="text-sm text-gray-500">
            その他の設定項目（アカウント設定、パスワード変更など）は今後追加予定です
          </p>
        </div>
      </div>
    </div>
  );
}