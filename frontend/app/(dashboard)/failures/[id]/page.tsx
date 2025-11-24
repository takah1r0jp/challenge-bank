"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { Failure, ApiResponse } from "@/lib/types";
import { toast } from "react-hot-toast";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ArrowLeft, Pencil, Trash2, Calendar } from "lucide-react";
import { formatDistanceToNow, format } from "date-fns";
import { ja } from "date-fns/locale";
import Link from "next/link";

/**
 * スコアを星で表示するヘルパー関数
 * 例: score = 3 → "★★★☆☆"
 */
function renderStars(score: number): string {
  const filledStars = "★".repeat(score);
  const emptyStars = "☆".repeat(5 - score);
  return filledStars + emptyStars;
}

export default function FailureDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [failure, setFailure] = useState<Failure | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // データ取得
  useEffect(() => {
    const fetchFailure = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get<ApiResponse<Failure>>(
          `/failures/${id}`
        );
        setFailure(response.data.data);
      } catch (error) {
        const errorMessage = getErrorMessage(error);
        toast.error(errorMessage);
        // データ取得失敗時は一覧ページへリダイレクト
        router.push("/failures");
      } finally {
        setIsLoading(false);
      }
    };

    fetchFailure();
  }, [id, router]);

  // 削除処理
  const handleDelete = () => {
    setShowDeleteDialog(true);
  };

  const confirmDelete = async () => {
    setIsDeleting(true);
    try {
      await apiClient.delete(`/failures/${id}`);
      toast.success("失敗記録を削除しました");
      setShowDeleteDialog(false);
      // 削除成功時は一覧ページへリダイレクト
      router.push("/failures");
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  const cancelDelete = () => {
    setShowDeleteDialog(false);
  };

  // データ読み込み中
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">読み込み中...</p>
      </div>
    );
  }

  // データが取得できなかった場合（エラー時は既にリダイレクト済み）
  if (!failure) {
    return null;
  }

  // 相対時間（「3時間前」など）
  const relativeTime = formatDistanceToNow(new Date(failure.created_at), {
    addSuffix: true,
    locale: ja,
  });

  // 絶対時間（「2024年1月15日 14:30」）
  const absoluteTime = format(
    new Date(failure.created_at),
    "yyyy年MM月dd日 HH:mm",
    { locale: ja }
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* アクションボタン（上部） */}
        <div className="mb-6 flex items-center justify-between">
          <Link href="/failures">
            <Button variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              一覧へ戻る
            </Button>
          </Link>
          <div className="flex gap-2">
            <Link href={`/failures/${id}/edit`}>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Pencil className="mr-2 h-4 w-4" />
                編集
              </Button>
            </Link>
            <Button variant="destructive" onClick={handleDelete}>
              <Trash2 className="mr-2 h-4 w-4" />
              削除
            </Button>
          </div>
        </div>

        {/* 詳細カード */}
        <Card className="shadow-md">
          <CardContent className="p-6 space-y-6">
            {/* スコア表示 */}
            <div className="flex items-center gap-3">
              <span className="text-3xl text-yellow-500">
                {renderStars(failure.score)}
              </span>
              <span className="text-xl font-semibold text-gray-700">
                {failure.score}点
              </span>
            </div>

            {/* 区切り線 */}
            <div className="border-t border-gray-200"></div>

            {/* 失敗内容（全文） */}
            <div>
              <p className="text-base text-gray-800 leading-relaxed whitespace-pre-wrap">
                {failure.content}
              </p>
            </div>

            {/* 区切り線 */}
            <div className="border-t border-gray-200"></div>

            {/* 日付表示 */}
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Calendar className="h-4 w-4" />
              <span>
                {relativeTime} ({absoluteTime})
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 削除確認ダイアログ */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>この失敗記録を削除しますか？</DialogTitle>
            <DialogDescription>
              この操作は取り消せません。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={cancelDelete}
              disabled={isDeleting}
            >
              キャンセル
            </Button>
            <Button
              variant="destructive"
              onClick={confirmDelete}
              disabled={isDeleting}
            >
              {isDeleting ? "削除中..." : "削除する"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
