# Bolt.diy アーキテクチャ設計書

## 1. システム概要

Bolt.diyは、フロントエンドとバックエンドが分離された現代的なウェブアプリケーションです。

### 1.1 技術スタック

#### フロントエンド
- React
- TypeScript
- Vite
- CSS Modules

#### バックエンド
- Python
- Flask/FastAPI
- MongoDB

## 2. ディレクトリ構造

```
bolt-diy/
├── src/
│   ├── frontend/      # Reactアプリケーション
│   │   ├── public/    # 静的ファイル
│   │   └── src/       # ソースコード
│   ├── backend/       # Pythonバックエンド
│   │   ├── controllers/
│   │   ├── models/
│   │   └── routes/
│   └── shared/        # 共有リソース
├── config/            # 環境設定
├── scripts/           # 実行スクリプト
└── docs/             # ドキュメント
```

## 3. アプリケーションフロー

1. フロントエンド（ポート3000）
   - React RouterによるSPA実装
   - コンポーネントベースのUI設計
   - 状態管理（Context API/Redux）

2. バックエンド（ポート5000）
   - RESTful API
   - JWT認証
   - データベース操作

## 4. セキュリティ考慮事項

- CORS設定
- JWT認証
- 環境変数による機密情報管理
- 入力バリデーション

## 5. 開発フロー

1. ローカル開発
   ```bash
   # 開発環境起動
   scripts/start_dev.bat
   ```

2. ビルド
   ```bash
   # フロントエンドビルド
   scripts/build_frontend.bat
   
   # バックエンドビルド
   scripts/build_backend.bat
   ```

## 6. デプロイメント

1. 環境設定
   - development.json
   - production.json

2. デプロイ手順
   - 本番環境の設定
   - ビルド実行
   - サーバーへのデプロイ

## 7. 保守・運用

- ログ管理
- エラーハンドリング
- パフォーマンスモニタリング
- バックアップ戦略
