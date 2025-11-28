import { z } from "zod";

/**
 * ユーザー登録スキーマ
 * メールアドレス、パスワード、確認パスワードのバリデーション
 */
export const registerSchema = z
  .object({
    email: z.string().email("有効なメールアドレスを入力してください"),
    password: z.string().min(8, "パスワードは8文字以上である必要があります"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "パスワードが一致しません",
    path: ["confirmPassword"], // エラーをconfirmPasswordフィールドに表示
  });

/**
 * 登録スキーマから型を推論
 * React Hook Formで使用
 */
export type RegisterFormData = z.infer<typeof registerSchema>;

/**
 * ログインスキーマ
 * メールアドレスとパスワードのバリデーション
 */
export const loginSchema = z.object({
  email: z.string().email("有効なメールアドレスを入力してください"),
  password: z.string().min(1, "パスワードを入力してください"),
});

/**
 * ログインスキーマから型を推論
 */
export type LoginFormData = z.infer<typeof loginSchema>;

/**
 * 挑戦記録スキーマ（MVP版：contentとscoreのみ）
 * 挑戦内容とスコアのバリデーション
 */
export const challengeSchema = z.object({
  content: z
    .string()
    .min(1, "挑戦内容を入力してください")
    .max(1000, "挑戦内容は1000文字以内で入力してください"),
  score: z
    .number({
      message: "スコアを選択してください",
    })
    .int("スコアは整数である必要があります")
    .min(1, "スコアは1以上である必要があります")
    .max(5, "スコアは5以下である必要があります"),
});

/**
 * 挑戦記録スキーマから型を推論
 */
export type ChallengeFormData = z.infer<typeof challengeSchema>;

// ========== Phase 2以降で拡張予定 ==========
/*
export const challengeSchemaExtended = z.object({
  challenge_content: z
    .string()
    .min(1, "挑戦内容を入力してください")
    .max(500, "挑戦内容は500文字以内で入力してください"),
  challenge_content: z
    .string()
    .min(1, "挑戦内容を入力してください")
    .max(1000, "挑戦内容は1000文字以内で入力してください"),
  next_action: z
    .string()
    .min(1, "ネクストアクションを入力してください")
    .max(500, "ネクストアクションは500文字以内で入力してください"),
  challenge_level: z.number().int().min(1).max(3),
  novelty_level: z.number().int().min(1).max(3),
});
*/
