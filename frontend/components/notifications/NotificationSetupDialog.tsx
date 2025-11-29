'use client';

import { useRouter } from 'next/navigation';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Bell, Sparkles, X } from 'lucide-react';

interface NotificationSetupDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSetupLater: () => void;
}

/**
 * 通知設定促進ダイアログ
 * Material Design 3準拠
 *
 * 最初の挑戦記録後に表示され、通知時刻の設定を促す
 */
export function NotificationSetupDialog({
  open,
  onOpenChange,
  onSetupLater,
}: NotificationSetupDialogProps) {
  const router = useRouter();

  const handleSetupNow = () => {
    onOpenChange(false);
    router.push('/settings');
  };

  const handleSetupLater = () => {
    onSetupLater();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          {/* アイコン + タイトル */}
          <div className="flex flex-col items-center gap-4 mb-2">
            {/* お祝いアイコン */}
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl" />
              <div className="relative bg-gradient-to-br from-primary to-primary/80 rounded-full p-4">
                <Sparkles className="h-8 w-8 text-primary-foreground" />
              </div>
            </div>

            <DialogTitle className="text-2xl font-bold text-center">
              🎉 最初の挑戦を記録しました！
            </DialogTitle>
          </div>

          <DialogDescription className="text-center text-base">
            おめでとうございます！
            <br />
            挑戦を習慣化するために、毎日のリマインダー通知を設定しませんか？
          </DialogDescription>
        </DialogHeader>

        {/* 通知機能の説明カード */}
        <div className="my-6 p-4 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg">
          <div className="flex items-start gap-3">
            <Bell className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-blue-900 dark:text-blue-100">
              <p className="font-medium mb-1">通知機能について</p>
              <p className="text-blue-700 dark:text-blue-200">
                毎日指定した時刻に、挑戦を記録するリマインダーが届きます。
                継続的な成長をサポートします。
              </p>
            </div>
          </div>
        </div>

        <DialogFooter className="flex-col sm:flex-row gap-2">
          {/* 後で設定ボタン */}
          <Button
            variant="outline"
            onClick={handleSetupLater}
            className="w-full sm:w-auto order-2 sm:order-1"
          >
            <X className="mr-2 h-4 w-4" />
            後で設定する
          </Button>

          {/* 今すぐ設定ボタン（Material Design 3: Filled Button） */}
          <Button
            onClick={handleSetupNow}
            className="w-full sm:w-auto order-1 sm:order-2 bg-primary hover:bg-primary/90"
          >
            <Bell className="mr-2 h-4 w-4" />
            今すぐ設定する
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
