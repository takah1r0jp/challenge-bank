import { Header } from "@/components/layout/Header";

/**
 * ダッシュボードレイアウト
 * ログイン後のすべてのページで共通のレイアウトを提供
 * - ヘッダー（ナビゲーション + ユーザー情報）
 * - メインコンテンツエリア
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <Header />

      {/* メインコンテンツ */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
