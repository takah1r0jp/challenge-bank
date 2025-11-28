import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from "axios";
import { ApiError } from "@/lib/types";

/**
 * バックエンドAPIのベースURL
 * .env.localから取得
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

/**
 * Axiosインスタンス
 * すべてのAPI呼び出しでこのインスタンスを使用
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10秒でタイムアウト
});

/**
 * リクエストインターセプター
 * すべてのリクエストに自動で認証トークンを追加
 *
 * 【動作】
 * 1. localStorageからトークンを取得
 * 2. トークンが存在すれば、Authorizationヘッダーに追加
 * 3. リクエストを送信
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // localStorageからトークンを取得
    const token = localStorage.getItem("access_token");

    // トークンが存在する場合、Authorizationヘッダーに追加
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    // リクエストエラー時の処理
    return Promise.reject(error);
  }
);

/**
 * レスポンスインターセプター
 * エラーハンドリングを統一
 *
 * 【動作】
 * - 成功時: そのままレスポンスを返す
 * - 401エラー: トークン削除 → ログインページへリダイレクト
 * - その他のエラー: エラーメッセージを整形して返す
 */
apiClient.interceptors.response.use(
  (response) => {
    // 成功時はそのまま返す
    return response;
  },
  (error: AxiosError<ApiError>) => {
    // 401 Unauthorized: トークン期限切れまたは無効
    if (error.response?.status === 401) {
      // トークンを削除
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");

      // ログインページへリダイレクト（現在のページがログインページでない場合）
      if (typeof window !== "undefined" && window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    // エラーオブジェクトをそのまま返す
    return Promise.reject(error);
  }
);

/**
 * APIエラーからエラーメッセージを抽出
 *
 * @param error - Axiosエラーオブジェクト
 * @returns エラーメッセージ文字列
 *
 * @example
 * try {
 *   await apiClient.post("/challenges", data);
 * } catch (error) {
 *   const message = getErrorMessage(error);
 *   toast.error(message);
 * }
 */
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;

    // バックエンドからのエラーレスポンスがある場合
    if (axiosError.response?.data?.error) {
      return axiosError.response.data.error.message;
    }

    // HTTPエラーメッセージ
    if (axiosError.response?.statusText) {
      return axiosError.response.statusText;
    }

    // ネットワークエラー
    if (axiosError.message) {
      return axiosError.message;
    }
  }

  // その他のエラー
  return "An unexpected error occurred";
};
