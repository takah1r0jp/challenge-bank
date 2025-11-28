import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Challenge } from "@/lib/types";
import { formatDistanceToNow } from "date-fns";
import { ja } from "date-fns/locale";
import { Pencil, Trash2 } from "lucide-react";

/**
 * 挑戦記録カードのProps
 */
interface ChallengeCardProps {
  challenge: Challenge;
  showActions?: boolean; // 編集・削除ボタンを表示するかどうか
  onEdit?: (id: string) => void; // 編集ボタンのクリックハンドラ
  onDelete?: (id: string) => void; // 削除ボタンのクリックハンドラ
}

/**
 * スコアを星で表示するヘルパー関数
 * 例: score = 3 → "★★★☆☆"
 */
function renderStars(score: number): string {
  const filledStars = "★".repeat(score);
  const emptyStars = "☆".repeat(5 - score);
  return filledStars + emptyStars;
}

/**
 * 挑戦記録カードコンポーネント
 * 挑戦内容（省略形）、スコア、相対時間を表示
 */
export function ChallengeCard({ challenge, showActions = false, onEdit, onDelete }: ChallengeCardProps) {
  // 挑戦内容を最初の100文字に省略
  const truncatedContent =
    challenge.content.length > 100
      ? challenge.content.slice(0, 100) + "..."
      : challenge.content;

  // 相対時間（"3時間前"など）
  const relativeTime = formatDistanceToNow(new Date(challenge.created_at), {
    addSuffix: true,
    locale: ja,
  });

  // アクションボタンがある場合は、カード全体をリンクにしない
  if (showActions) {
    return (
      <Card className="transition-shadow hover:shadow-md">
        <CardContent className="p-4">
          {/* 挑戦内容（省略形） */}
          <Link href={`/challenges/${challenge.id}`} className="block hover:text-blue-600">
            <p className="text-sm text-gray-700">{truncatedContent}</p>
          </Link>

          {/* スコア、時間、アクションボタン */}
          <div className="mt-3 flex items-center justify-between gap-2">
            <div className="flex items-center gap-3">
              {/* スコア（星で表示） */}
              <span className="text-lg text-yellow-500">
                {renderStars(challenge.score)}
              </span>

              {/* 相対時間 */}
              <span className="text-xs text-gray-500">{relativeTime}</span>
            </div>

            {/* アクションボタン */}
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit?.(challenge.id);
                }}
                className="h-8 w-8 p-0"
                aria-label="編集"
              >
                <Pencil className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete?.(challenge.id);
                }}
                className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                aria-label="削除"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  // アクションボタンがない場合は、従来通りカード全体をリンクにする
  return (
    <Link href={`/challenges/${challenge.id}`}>
      <Card className="cursor-pointer transition-shadow hover:shadow-md">
        <CardContent className="p-4">
          {/* 挑戦内容（省略形） */}
          <p className="text-sm text-gray-700">{truncatedContent}</p>

          {/* スコアと時間 */}
          <div className="mt-3 flex items-center justify-between">
            {/* スコア（星で表示） */}
            <span className="text-lg text-yellow-500">
              {renderStars(challenge.score)}
            </span>

            {/* 相対時間 */}
            <span className="text-xs text-gray-500">{relativeTime}</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
