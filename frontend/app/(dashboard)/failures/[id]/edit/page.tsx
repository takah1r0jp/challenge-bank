"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { failureSchema } from "@/lib/utils/validators";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { Failure, ApiResponse } from "@/lib/types";
import { toast } from "react-hot-toast";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

type FailureFormData = {
  content: string;
  score: number;
};

export default function EditFailurePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCancelDialog, setShowCancelDialog] = useState(false);
  const [failure, setFailure] = useState<Failure | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isDirty },
  } = useForm<FailureFormData>({
    resolver: zodResolver(failureSchema),
    defaultValues: {
      content: "",
      score: undefined,
    },
  });

  const watchScore = watch("score");
  const watchContent = watch("content");

  // データ取得
  useEffect(() => {
    const fetchFailure = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get<ApiResponse<Failure>>(
          `/failures/${id}`
        );
        const failureData = response.data.data;
        setFailure(failureData);

        // フォームに初期値をセット（shouldDirty: false で「変更なし」扱い）
        setValue("content", failureData.content, { shouldDirty: false });
        setValue("score", failureData.score, { shouldDirty: false });
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
  }, [id, router, setValue]);

  // 更新処理
  const onSubmit = async (data: FailureFormData) => {
    setIsSubmitting(true);
    try {
      await apiClient.put(`/failures/${id}`, data);
      toast.success("失敗記録を更新しました");
      router.push("/failures");
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  // キャンセル処理
  const handleCancel = () => {
    // 変更がある場合は確認ダイアログを表示
    if (isDirty) {
      setShowCancelDialog(true);
    } else {
      router.push("/failures");
    }
  };

  const confirmCancel = () => {
    setShowCancelDialog(false);
    router.push("/failures");
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

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <Card className="shadow-md">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-gray-800">
              ✏️ 失敗記録を編集
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* 失敗内容 */}
              <div className="space-y-2">
                <Label htmlFor="content" className="text-base font-medium">
                  失敗内容 <span className="text-red-600">*</span>
                </Label>
                <Textarea
                  id="content"
                  placeholder="どんな挑戦をして、どんな失敗をしましたか？"
                  rows={5}
                  className={cn(
                    "resize-none",
                    errors.content && "border-red-500 focus:ring-red-500"
                  )}
                  {...register("content")}
                />
                <div className="flex justify-between items-center">
                  <p className="text-sm text-gray-500">1-1000文字</p>
                  {watchContent && (
                    <p
                      className={cn(
                        "text-sm",
                        watchContent.length > 1000
                          ? "text-red-600"
                          : "text-gray-500"
                      )}
                    >
                      {watchContent.length} / 1000
                    </p>
                  )}
                </div>
                {errors.content && (
                  <p className="text-sm text-red-600" role="alert">
                    {errors.content.message}
                  </p>
                )}
              </div>

              {/* スコア */}
              <div className="space-y-2">
                <Label className="text-base font-medium">
                  スコア <span className="text-red-600">*</span>
                </Label>
                <div className="flex gap-2 sm:gap-3">
                  {[1, 2, 3, 4, 5].map((value) => (
                    <button
                      key={value}
                      type="button"
                      onClick={() => setValue("score", value, { shouldDirty: true })}
                      aria-label={`スコア ${value} を選択`}
                      className={cn(
                        "flex-1 py-3 sm:py-4 rounded-lg border-2 font-semibold text-lg transition-all",
                        "hover:scale-105 active:scale-95",
                        watchScore === value
                          ? "bg-blue-600 text-white border-blue-600 shadow-md"
                          : "bg-white text-gray-700 border-gray-300 hover:border-blue-400"
                      )}
                    >
                      {value}
                    </button>
                  ))}
                </div>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>小さな一歩</span>
                  <span>大きな挑戦</span>
                </div>
                {errors.score && (
                  <p className="text-sm text-red-600" role="alert">
                    {errors.score.message}
                  </p>
                )}
              </div>

              {/* ボタン */}
              <div className="flex gap-3 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleCancel}
                  disabled={isSubmitting}
                  className="flex-1"
                >
                  キャンセル
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  {isSubmitting ? "更新中..." : "更新する"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* キャンセル確認ダイアログ */}
      <Dialog open={showCancelDialog} onOpenChange={setShowCancelDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>変更を破棄しますか？</DialogTitle>
            <DialogDescription>
              編集した内容は保存されません。本当に戻りますか？
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowCancelDialog(false)}
            >
              編集を続ける
            </Button>
            <Button
              variant="destructive"
              onClick={confirmCancel}
            >
              破棄して戻る
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
