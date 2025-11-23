import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Failure } from "@/lib/types";
import { formatDistanceToNow } from "date-fns";
import { ja } from "date-fns/locale";

/**
 * 失敗記録カードのProps
 */
interface FailureCardProps {
  failure: Failure;
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
 * 失敗記録カードコンポーネント
 * 失敗内容（省略形）、スコア、相対時間を表示
 */
export function FailureCard({ failure }: FailureCardProps) {
  // 失敗内容を最初の100文字に省略
  const truncatedContent =
    failure.content.length > 100
      ? failure.content.slice(0, 100) + "..."
      : failure.content;

  // 相対時間（"3時間前"など）
  const relativeTime = formatDistanceToNow(new Date(failure.created_at), {
    addSuffix: true,
    locale: ja,
  });

  return (
    <Link href={`/failures/${failure.id}`}>
      <Card className="cursor-pointer transition-shadow hover:shadow-md">
        <CardContent className="p-4">
          {/* 失敗内容（省略形） */}
          <p className="text-sm text-gray-700">{truncatedContent}</p>

          {/* スコアと時間 */}
          <div className="mt-3 flex items-center justify-between">
            {/* スコア（星で表示） */}
            <span className="text-lg text-yellow-500">
              {renderStars(failure.score)}
            </span>

            {/* 相対時間 */}
            <span className="text-xs text-gray-500">{relativeTime}</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
