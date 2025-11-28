"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import toast from "react-hot-toast";
import { useAuth } from "@/lib/context/AuthContext";
import { loginSchema, LoginFormData } from "@/lib/utils/validators";
import { getErrorMessage } from "@/lib/api/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

/**
 * ログインページ
 * メールアドレスとパスワードでログイン
 */
export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  // React Hook Formのセットアップ
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema), // Zodバリデーション
  });

  /**
   * フォーム送信ハンドラー
   * ログイン処理を実行し、成功/挑戦をトースト通知
   */
  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);

    try {
      // AuthContextのlogin関数を呼び出し
      await login(data);

      // 成功時はトースト通知（リダイレクトは login() 内で自動実行）
      toast.success("ログインしました");
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
          <CardTitle className="text-2xl font-bold">ログイン</CardTitle>
          <CardDescription>
            メールアドレスとパスワードを入力してログインしてください
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
                placeholder="パスワードを入力"
                {...register("password")}
                disabled={isLoading}
              />
              {errors.password && (
                <p className="text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            {/* ログインボタン */}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "ログイン中..." : "ログイン"}
            </Button>

            {/* 登録ページへのリンク */}
            <div className="text-center text-sm">
              <span className="text-gray-600">アカウントをお持ちでない方は</span>{" "}
              <Link href="/register" className="text-blue-600 hover:underline">
                新規登録
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
