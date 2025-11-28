import Link from "next/link";
import { Button } from "@/components/ui/button";

/**
 * 空状態コンポーネント
 * 挑戦記録がまだない場合に表示
 */
export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 p-12 text-center">
      {/* アイコン */}
      <div className="mb-4 text-6xl">📝</div>

      {/* メッセージ */}
      <h3 className="mb-2 text-lg font-semibold text-gray-900">
        まだ挑戦を記録していません
      </h3>
      <p className="mb-6 text-sm text-gray-500">
        最初の挑戦を記録して、挑戦の習慣を始めましょう！
      </p>

      {/* 新規作成ボタン */}
      <Link href="/challenges/new">
        <Button size="lg">最初の挑戦を記録する</Button>
      </Link>
    </div>
  );
}
