"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient, getErrorMessage } from "@/lib/api/client";
import { User, AuthCredentials, ApiResponse } from "@/lib/types";

/**
 * 認証コンテキストの型定義
 * useAuthフックが返す値の型
 */
interface AuthContextType {
  user: User | null; // 現在ログイン中のユーザー（未ログインならnull）
  isLoading: boolean; // 認証状態確認中かどうか
  isAuthenticated: boolean; // ログイン済みかどうか
  updateUser: (user: User) => void; // ユーザー情報を上書きする
  login: (credentials: AuthCredentials) => Promise<void>; // ログイン関数
  register: (credentials: AuthCredentials) => Promise<void>; // 登録関数
  logout: () => void; // ログアウト関数
}

/**
 * 認証コンテキスト
 * 初期値はundefined（Providerで囲まれていない場合にエラーを出すため）
 */
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * 認証プロバイダーコンポーネント
 * アプリ全体をこのコンポーネントで囲むことで、どこからでも認証情報にアクセス可能
 *
 * @example
 * // app/layout.tsx
 * <AuthProvider>
 *   <Component />
 * </AuthProvider>
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  /**
   * 初回レンダリング時に認証状態を確認
   * localStorageにトークンがあれば、ユーザー情報を取得
   */
  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * 認証状態を確認する関数
   * localStorageからトークンを取得し、/auth/me APIでユーザー情報を取得
   */
  const checkAuth = async () => {
    try {
      const token = localStorage.getItem("access_token");

      // トークンがない場合は未認証
      if (!token) {
        setIsLoading(false);
        return;
      }

      // /auth/me APIでユーザー情報を取得
      const response = await apiClient.get<ApiResponse<User>>("/auth/me");

      // ユーザー情報をstateに保存
      setUser(response.data.data);
    } catch (error) {
      // エラー時はトークンを削除
      console.error("認証確認エラー:", getErrorMessage(error));
      localStorage.removeItem("access_token");
      setUser(null);
    } finally {
      // ローディング終了
      setIsLoading(false);
    }
  };

  /**
   * ログイン関数
   * メールアドレスとパスワードでログインし、トークンを保存
   *
   * @param credentials - メールアドレスとパスワード
   * @throws エラー時は呼び出し元でキャッチして処理
   */
  const login = async (credentials: AuthCredentials) => {
    try {
      // POST /auth/login APIでログイン
      const response = await apiClient.post<
        ApiResponse<User & { access_token: string }>
      >("/auth/login", credentials);

      const { access_token, ...userData } = response.data.data;

      // トークンをlocalStorageに保存
      localStorage.setItem("access_token", access_token);

      // ユーザー情報をstateに保存
      setUser(userData);

      // ダッシュボードへリダイレクト
      router.push("/");
    } catch (error) {
      // エラーを呼び出し元に投げる（フォームでエラー表示するため）
      throw error;
    }
  };

  /**
   * ユーザー登録関数
   * メールアドレスとパスワードで新規登録し、自動ログイン
   *
   * @param credentials - メールアドレスとパスワード
   * @throws エラー時は呼び出し元でキャッチして処理
   */
  const register = async (credentials: AuthCredentials) => {
    try {
      // POST /auth/register APIで登録
      const response = await apiClient.post<
        ApiResponse<User & { access_token: string }>
      >("/auth/register", credentials);

      const { access_token, ...userData } = response.data.data;

      // トークンをlocalStorageに保存
      localStorage.setItem("access_token", access_token);

      // ユーザー情報をstateに保存
      setUser(userData);

      // ダッシュボードへリダイレクト
      router.push("/");
    } catch (error) {
      // エラーを呼び出し元に投げる
      throw error;
    }
  };

  /**
   * ログアウト関数
   * トークンとユーザー情報を削除し、ログインページへリダイレクト
   */
  const logout = () => {
    // localStorageからトークンを削除
    localStorage.removeItem("access_token");

    // stateをクリア
    setUser(null);

    // ログインページへリダイレクト
    router.push("/login");
  };

  /**
   * ユーザー情報を上書きするユーティリティ
   * 外部（例：設定ページ）からユーザー情報を更新する際に使う
   */
  const updateUser = (newUser: User) => {
    setUser(newUser);
  };

  // コンテキストの値
  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user, // userがnullでなければtrue
    login,
    register,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * 認証フック
 * コンポーネント内で認証情報にアクセスするためのカスタムフック
 *
 * @returns 認証コンテキストの値
 * @throws Providerで囲まれていない場合はエラー
 *
 * @example
 * function MyComponent() {
 *   const { user, isAuthenticated, logout } = useAuth();
 *
 *   if (!isAuthenticated) {
 *     return <div>ログインしてください</div>;
 *   }
 *
 *   return (
 *     <div>
 *       <p>ようこそ、{user.email}さん</p>
 *       <button onClick={logout}>ログアウト</button>
 *     </div>
 *   );
 * }
 */
export function useAuth() {
  const context = useContext(AuthContext);

  // Providerで囲まれていない場合はエラー
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
