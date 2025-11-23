"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import toast from "react-hot-toast";
import { useAuth } from "@/lib/context/AuthContext";
import { registerSchema, RegisterFormData } from "@/lib/utils/validators";
import { getErrorMessage } from "@/lib/api/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

/**
 * ユーザー登録ページ
 * メールアドレス、パスワード、確認パスワードで新規登録
 */
export default function RegisterPage() {
  const [isLoading, setIsLoading] = useState(false);
  const { register: registerUser } = useAuth();

  // React Hook Formのセットアップ
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema), // Zodバリデーション
  });

  /**
   * フォーム送信ハンドラー
   * ユーザー登録処理を実行し、成功/失敗をトースト通知
   */
  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);

    try {
      // AuthContextのregister関数を呼び出し
      // confirmPasswordは送信しない（バリデーションのみで使用）
      await registerUser({
        email: data.email,
        password: data.password,
      });

      // 成功時はトースト通知（リダイレクトは registerUser() 内で自動実行）
      toast.success("アカウントを作成しました");
    } catch (error) {
      // エラーメッセージを抽出してトースト表示
      const message = getErrorMessage(error);
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">新規登録</CardTitle>
          <CardDescription>
            メールアドレスとパスワードを入力してアカウントを作成してください
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* メールアドレス入力 */}
            <div className="space-y-2">
              <Label htmlFor="email">メールアドレス</Label>
              <Input
                id="email"
                type="email"
                placeholder="user@example.com"
                {...register("email")}
                disabled={isLoading}
              />
              {errors.email && (
                <p className="text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            {/* パスワード入力 */}
            <div className="space-y-2">
              <Label htmlFor="password">パスワード</Label>
              <Input
                id="password"
                type="password"
                placeholder="8文字以上のパスワード"
                {...register("password")}
                disabled={isLoading}
              />
              {errors.password && (
                <p className="text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            {/* 確認パスワード入力 */}
            <div className="space-y-2">
              <Label htmlFor="confirmPassword">パスワード（確認）</Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="パスワードを再入力"
                {...register("confirmPassword")}
                disabled={isLoading}
              />
              {errors.confirmPassword && (
                <p className="text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>

            {/* 登録ボタン */}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "登録中..." : "アカウントを作成"}
            </Button>

            {/* ログインページへのリンク */}
            <div className="text-center text-sm">
              <span className="text-gray-600">すでにアカウントをお持ちの方は</span>{" "}
              <Link href="/login" className="text-blue-600 hover:underline">
                ログイン
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
