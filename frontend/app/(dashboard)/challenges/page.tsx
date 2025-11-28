"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/context/AuthContext";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { Challenge, ApiResponse } from "@/lib/types";
import { ChallengeCard } from "@/components/dashboard/ChallengeCard";
import { EmptyState } from "@/components/dashboard/EmptyState";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "react-hot-toast";
import Link from "next/link";
import { Plus } from "lucide-react";

export default function ChallengesListPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingChallengeId, setDeletingChallengeId] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // データ取得
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchChallenges = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get<ApiResponse<Challenge[]>>(
          "/challenges?limit=50"
        );
        setChallenges(response.data.data);
      } catch (error) {
        console.error("Failed to fetch challenges:", getErrorMessage(error));
        toast.error("挑戦記録の取得に挑戦しました");
      } finally {
        setIsLoading(false);
      }
    };

    fetchChallenges();
  }, [isAuthenticated]);

  // 編集ボタンのハンドラ
  const handleEdit = (id: string) => {
    // 将来実装: 編集ページへ遷移
    router.push(`/challenges/${id}/edit`);
  };

  // 削除ボタンのハンドラ
  const handleDelete = (id: string) => {
    setDeletingChallengeId(id);
    setDeleteDialogOpen(true);
  };

  // 削除確認
  const confirmDelete = async () => {
    if (!deletingChallengeId) return;

    setIsDeleting(true);
    try {
      await apiClient.delete(`/challenges/${deletingChallengeId}`);

      // 楽観的UI更新: リストから削除
      setChallenges((prev) => prev.filter((f) => f.id !== deletingChallengeId));

      toast.success("挑戦記録を削除しました");
      setDeleteDialogOpen(false);
      setDeletingChallengeId(null);
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  // 削除キャンセル
  const cancelDelete = () => {
    setDeleteDialogOpen(false);
    setDeletingChallengeId(null);
  };

  // 認証チェック中
  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">読み込み中...</p>
      </div>
    );
  }

  // 未認証
  if (!isAuthenticated) {
    return null;
  }

  // データ読み込み中
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">読み込み中...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* ヘッダー */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-800">挑戦の記録</h1>
          <Link href="/challenges/new">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="mr-2 h-4 w-4" />
              新しい挑戦を記録
            </Button>
          </Link>
        </div>

        {/* 挑戦記録一覧 */}
        {challenges.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="space-y-4">
            {challenges.map((challenge) => (
              <ChallengeCard
                key={challenge.id}
                challenge={challenge}
                showActions
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>

      {/* 削除確認ダイアログ */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>この挑戦記録を削除しますか？</DialogTitle>
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
