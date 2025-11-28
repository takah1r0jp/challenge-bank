# AWS Lambda コンソール設定ガイド

**IAMロール設定完了後の手順**を順を追って説明します。

---

## 📋 前提条件

✅ IAMロール作成済み（Lambda実行権限のみ）  
✅ Resend API キー取得済み  
✅ バックエンド `.env` に以下が設定済み：
- `RESEND_API_KEY`
- `NOTIFICATION_API_KEY` （APIキー）

---

## Step 1️⃣: Lambda 関数の作成

### 1.1 AWS Lambda コンソールを開く

```
https://console.aws.amazon.com/lambda/
```

### 1.2 「関数を作成」をクリック

| 項目 | 設定値 |
|------|--------|
| **関数の作成方法** | 一から作成 |
| **関数名** | `challenge-bank-notifications` |
| **ランタイム** | `Python 3.11` または `Python 3.12` |
| **アーキテクチャ** | `x86_64` |
| **実行ロール** | 既存のロールを使用 → IAMロール選択 |

✅ 「関数を作成」をクリック

---

## Step 2️⃣: 関数コードの設定

### 2.1 コードエディタでコードを貼り付け

Lambda コンソール内の Code editor に以下をコピー&ペースト：

```python
import json
import os
import urllib.request
from typing import Any, Dict


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda エントリーポイント
    毎時 EventBridge から呼び出されます
    """
    backend_url = os.environ.get("BACKEND_URL")
    api_key = os.environ.get("NOTIFICATION_API_KEY")
    
    if not backend_url or not api_key:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": "Missing required environment variables"
            })
        }
    
    endpoint = f"{backend_url}/notifications/send"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(
            endpoint,
            method="POST",
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)
            
            print(f"✅ Notification batch completed successfully")
            print(f"  Total users: {result.get('data', {}).get('total_users', 0)}")
            print(f"  Emails sent: {result.get('data', {}).get('emails_sent', 0)}")
            print(f"  Emails failed: {result.get('data', {}).get('emails_failed', 0)}")
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "success": True,
                    "message": "Notification batch executed successfully",
                    "result": result
                })
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        error_message = f"HTTP Error {e.code}: {error_body}"
        print(f"❌ HTTP Error: {error_message}")
        
        return {
            "statusCode": e.code,
            "body": json.dumps({
                "success": False,
                "error": error_message
            })
        }
        
    except urllib.error.URLError as e:
        error_message = f"Connection Error: {str(e.reason)}"
        print(f"❌ Network Error: {error_message}")
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": error_message
            })
        }
        
    except json.JSONDecodeError as e:
        error_message = f"JSON Parse Error: {str(e)}"
        print(f"❌ Parse Error: {error_message}")
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": error_message
            })
        }
        
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(f"❌ Unexpected Error: {error_message}")
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": error_message
            })
        }
```

### 2.2 「Deploy」ボタンをクリック

✅ コードがデプロイされます

---

## Step 3️⃣: 環境変数の設定

### 3.1 左パネルの「Configuration」タブをクリック

### 3.2 「Environment variables」をクリック

### 3.3 「Edit」ボタンをクリック

### 3.4 以下の環境変数を追加

| キー | 値 | 説明 |
|------|-----|------|
| `BACKEND_URL` | `https://your-api.example.com` | バックエンドのURL（例：Render等のデプロイ先） |
| `NOTIFICATION_API_KEY` | `your-internal-api-key-here` | バックエンド `.env` の `NOTIFICATION_API_KEY` と**完全に同じ値** |

> ⚠️ **重要**: `NOTIFICATION_API_KEY` が完全に一致していないと、認証失敗（403 Forbidden）になります

### 3.5 「Save」をクリック

✅ 環境変数が保存されます

---

## Step 4️⃣: タイムアウトとメモリ設定

### 4.1 Configuration → General configuration をクリック

### 4.2 「Edit」ボタンをクリック

| 項目 | 推奨値 |
|------|--------|
| **Memory** | 128 MB |
| **Timeout** | 30 sec |
| **Ephemeral storage** | 512 MB（デフォルト） |

### 4.3 「Save」をクリック

✅ 設定が保存されます

---

## Step 5️⃣: Lambda テスト実行

### 5.1 「Test」タブをクリック

### 5.2 テストイベント名を入力

例: `EventBridgeTest`

### 5.3 以下のテストペイロードを入力

```json
{
  "source": "aws.events",
  "detail-type": "Scheduled Event",
  "detail": {}
}
```

### 5.4 「Test」ボタンをクリック

### 5.5 実行結果を確認

**成功時:**
```
Response: {
  "statusCode": 200,
  "body": "{\"success\": true, ...}"
}

Logs: 
✅ Notification batch completed successfully
  Total users: 15
  Emails sent: 14
  Emails failed: 0
```

**失敗時:**
```
statusCode: 500
error: "Missing required environment variables"
```

→ 環境変数が正しく設定されているか確認

---

## Step 6️⃣: EventBridge スケジュール設定

### 6.1 AWS EventBridge コンソールを開く

```
https://console.aws.amazon.com/events/
```

### 6.2 「ルールを作成」をクリック

#### 6.2.1 詳細を定義

| 項目 | 値 |
|------|-----|
| **名前** | `challenge-bank-hourly-notification` |
| **説明** | `Hourly email notification trigger for Challenge Bank` |
| **イベントバス** | `default` |
| **ルールの状態** | `Enabled` |

### 6.2.2 スケジュールパターンを定義

- **ルールタイプ**: `Schedule`
- **パターン**: `Cron expression`
- **Cron 式**: `cron(0 * * * ? *)`

**説明:**
```
cron(0 * * * ? *)
     ↓ ↓ ↓ ↓ ↓ ↓
     分 時 日 月 曜 年

毎時0分に実行
例: 11:00 UTC = 20:00 JST
```

> 💡 ヒント: JST は UTC+9 なので、  
> 11:00 UTC = 20:00 JST です

### 6.2.3 ターゲットを選択

- **ターゲット 1**: `AWS Lambda function`
- **関数**: `challenge-bank-notifications`（ドロップダウンから選択）

### 6.2.4 「ルールを作成」をクリック

✅ EventBridge ルールが作成されます

---

## Step 7️⃣: CloudWatch ログで実行履歴を確認

### 7.1 CloudWatch コンソールを開く

```
https://console.aws.amazon.com/cloudwatch/
```

### 7.2 左パネルから「ロググループ」をクリック

### 7.3 `/aws/lambda/challenge-bank-notifications` を検索

### 7.4 ロググループをクリック

### 7.5 最新のログストリームを選択

**ログ例:**
```
2024-01-15T20:00:15.123Z	request id	✅ Notification batch completed successfully
2024-01-15T20:00:15.456Z	request id	  Total users: 15
2024-01-15T20:00:15.789Z	request id	  Emails sent: 14
2024-01-15T20:00:15.912Z	request id	  Emails failed: 0
```

---

## 🔍 トラブルシューティング

### ❌ 環境変数エラー

**エラー:**
```
Missing required environment variables
```

**原因:** `BACKEND_URL` または `NOTIFICATION_API_KEY` が未設定

**対策:**
1. Configuration → Environment variables を確認
2. 両方の変数が設定されているか確認
3. 特に `NOTIFICATION_API_KEY` が正確に入力されているか確認

---

### ❌ 認証エラー (403 Forbidden)

**ログ:**
```
HTTP Error 403: {"detail": "Invalid or missing API key"}
```

**原因:** `NOTIFICATION_API_KEY` がバックエンドの値と一致していない

**対策:**
1. バックエンドの `.env` ファイルで `NOTIFICATION_API_KEY` を確認
2. Lambda の環境変数と**完全に一致**させる
3. スペースや余分な文字がないか確認

---

### ❌ 接続エラー (Connection Error)

**ログ:**
```
Connection Error: [Errno -3] Temporary failure in name resolution
```

**原因:** バックエンドURL にアクセスできない

**対策:**
1. `BACKEND_URL` が正しいか確認
   - 例: `https://your-api.example.com` （スラッシュなし）
2. バックエンドサーバーが起動しているか確認
3. セキュリティグループで Lambda からのアクセスを許可しているか確認

---

### ❌ タイムアウト

**ログ:**
```
timeout exceeded
```

**原因:** バックエンドの応答が遅い

**対策:**
1. Lambda のタイムアウトを 30秒 → 60秒 に増やす
2. バックエンドのパフォーマンスを確認

---

### ✅ メール送信が 0 件

**成功したが:**
```
Emails sent: 0
Emails failed: 0
```

**原因:** 対応時刻のユーザーがいない

**対策:**
1. ユーザーの `notification_time` を確認
2. テスト用エンドポイント (`/notifications/test`) で動作確認
3. バックエンドのログを確認

---

## 📊 実行スケジュール確認

EventBridge コンソール → ルール → `challenge-bank-hourly-notification` を選択:

```
次の実行予定:
2024-01-15 20:00:00 UTC（JST: 翌日 05:00）
2024-01-15 21:00:00 UTC（JST: 翌日 06:00）
2024-01-15 22:00:00 UTC（JST: 翌日 07:00）
...
```

---

## ✅ 設定完了チェックリスト

- [ ] Lambda 関数を作成した
- [ ] コードを貼り付けてデプロイした
- [ ] 環境変数を設定した（BACKEND_URL, NOTIFICATION_API_KEY）
- [ ] タイムアウト（30秒）、メモリ（128MB）を設定した
- [ ] Lambda テストで成功を確認した
- [ ] EventBridge ルール（毎時0分）を作成した
- [ ] CloudWatch ログで実行履歴を確認した

---

## 🚀 本番運用

これ以降は:

1. **毎時0分に自動実行** — EventBridge が Lambda を呼び出し
2. **メール送信** — 対応時刻のユーザーに送信
3. **ログ記録** — CloudWatch に実行結果が記録

定期的に CloudWatch ログで以下を確認してください：
- ✅ 毎時実行されているか
- ✅ 送信数が期待値か
- ✅ エラーがないか

---

## 📞 参考リンク

- [AWS Lambda コンソール](https://console.aws.amazon.com/lambda/)
- [AWS EventBridge コンソール](https://console.aws.amazon.com/events/)
- [CloudWatch ログ](https://console.aws.amazon.com/cloudwatch/)
- [Cron式リファレンス](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cron-expressions.html)

