# OpenRouter統合ガイド

## 1. 前提条件

- OpenRouterアカウントとAPIキー
- デプロイ済みのBolt.diyバックエンド
- HTTPSが有効なドメイン

## 2. 環境設定

1. `.env`ファイルの設定
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ALLOWED_REFERER=https://your-domain.com
   ```

2. OpenRouterの設定
   - OpenRouter管理画面にログイン
   - 「カスタムモデル」セクションで新規モデルを追加
   - エンドポイント: `https://your-domain.com/api/deepseek/infer`
   - 認証方式: Bearer Token
   - ヘッダー設定:
     ```
     Content-Type: application/json
     Authorization: Bearer ${OPENROUTER_API_KEY}
     ```

## 3. APIエンドポイント

### 推論リクエスト
```bash
POST /api/deepseek/infer
Content-Type: application/json
Authorization: Bearer your-api-key

{
    "text": "推論したいテキスト",
    "model": "deepseek-coder-33b-instruct",
    "max_tokens": 1000,
    "temperature": 0.7
}
```

### レスポンス
```json
{
    "success": true,
    "response": "生成されたテキスト",
    "model": "使用されたモデル名",
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579
    }
}
```

## 4. エラーハンドリング

- ログの確認
  ```bash
  tail -f src/backend/logs/app.log
  ```

- 一般的なエラー:
  1. 認証エラー: APIキーの確認
  2. CORS エラー: ALLOWED_ORIGINSの設定確認
  3. タイムアウト: Gunicornのタイムアウト設定調整

## 5. セキュリティ考慮事項

1. APIキーの保護
   - 環境変数での管理
   - Git履歴からの除外

2. リクエスト制限
   - レート制限の実装
   - IPベースのフィルタリング

3. HTTPS
   - 常時SSL/TLS通信の確保
   - 証明書の定期更新

## 6. 運用監視

1. ヘルスチェック
   ```bash
   GET /api/deepseek/health
   ```

2. メトリクス監視
   - リクエスト数
   - レスポンスタイム
   - エラーレート

3. コスト管理
   - トークン使用量の監視
   - 予算制限の設定

## 7. トラブルシューティング

1. OpenRouter接続エラー
   - ネットワーク接続の確認
   - APIキーの有効性確認
   - リクエスト形式の検証

2. バックエンドエラー
   - ログファイルの確認
   - メモリ使用量の監視
   - プロセス状態の確認

3. 復旧手順
   ```bash
   # サービス再起動
   scripts/deploy_backend.bat
