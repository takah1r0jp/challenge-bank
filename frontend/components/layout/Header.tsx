"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/context/AuthContext";
import { Button } from "@/components/ui/button";

/**
 * ヘッダーコンポーネント
 * - ロゴ/アプリ名
 * - ナビゲーションリンク
 * - ユーザー情報 + ログアウトボタン
 */
export function Header() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  /**
   * ナビゲーションリンクがアクティブかどうかを判定
   */
  const isActive = (path: string) => {
    if (path === "/") {
      return pathname === "/";
    }
    return pathname.startsWith(path);
  };

  return (
    <header className="border-b bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* ロゴ + ナビゲーション */}
          <div className="flex items-center gap-8">
            {/* ロゴ */}
            <Link href="/" className="text-xl font-bold text-gray-900">
              Challenge Bank
            </Link>

            {/* ナビゲーション */}
            <nav className="hidden md:flex md:gap-6">
              <Link
                href="/"
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  isActive("/") && pathname === "/"
                    ? "text-blue-600"
                    : "text-gray-600"
                }`}
              >
                ダッシュボード
              </Link>
              <Link
                href="/challenges"
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  isActive("/challenges") ? "text-blue-600" : "text-gray-600"
                }`}
              >
                挑戦一覧
              </Link>
              <Link
                href="/settings"
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  isActive("/settings") ? "text-blue-600" : "text-gray-600"
                }`}
              >
                設定
              </Link>
            </nav>
          </div>

          {/* ユーザー情報 + ログアウト */}
          {user && (
            <div className="flex items-center gap-4">
              {/* ユーザーメールアドレス */}
              <span className="hidden text-sm text-gray-600 sm:block">
                {user.email}
              </span>

              {/* ログアウトボタン */}
              <Button
                variant="outline"
                size="sm"
                onClick={logout}
                className="text-sm"
              >
                ログアウト
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
