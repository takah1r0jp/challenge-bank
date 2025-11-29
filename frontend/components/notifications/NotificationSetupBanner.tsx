'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Bell, X } from 'lucide-react';

interface NotificationSetupBannerProps {
  onDismiss?: () => void;
}

/**
 * 通知設定バナー
 * Material Design 3準拠
 *
 * 通知未設定のユーザーにダッシュボードで表示
 */
export function NotificationSetupBanner({ onDismiss }: NotificationSetupBannerProps) {
  const router = useRouter();
  const [isVisible, setIsVisible] = useState(true);

  const handleSetup = () => {
    router.push('/settings');
  };

  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss?.();
  };

  if (!isVisible) return null;

  return (
    <div
      className="relative overflow-hidden rounded-lg border border-blue-200 dark:border-blue-800 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 p-4 shadow-sm"
      role="alert"
      aria-live="polite"
    >
      {/* 背景装飾 */}
      <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-blue-200/30 dark:bg-blue-800/30 blur-2xl" />
      <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 rounded-full bg-indigo-200/30 dark:bg-indigo-800/30 blur-2xl" />

      <div className="relative flex items-start gap-4">
        {/* アイコン */}
        <div className="flex-shrink-0">
          <div className="rounded-full bg-blue-100 dark:bg-blue-900/50 p-2.5">
            <Bell className="h-5 w-5 text-blue-600 dark:text-blue-400" />
          </div>
        </div>

        {/* コンテンツ */}
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">
            通知時刻を設定しませんか？
          </h3>
          <p className="text-sm text-blue-700 dark:text-blue-200">
            毎日のリマインダー通知で、挑戦を習慣化しましょう。
          </p>

          {/* ボタン */}
          <div className="mt-3 flex flex-wrap gap-2">
            <Button
              size="sm"
              onClick={handleSetup}
              className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600 text-white"
            >
              <Bell className="mr-1.5 h-3.5 w-3.5" />
              設定する
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={handleDismiss}
              className="text-blue-700 dark:text-blue-200 hover:bg-blue-100 dark:hover:bg-blue-900/50"
            >
              後で
            </Button>
          </div>
        </div>

        {/* 閉じるボタン */}
        <button
          onClick={handleDismiss}
          className="flex-shrink-0 rounded-full p-1 text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 hover:text-blue-600 dark:hover:text-blue-300 transition-colors"
          aria-label="バナーを閉じる"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
