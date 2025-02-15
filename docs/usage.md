# Bolt.diy 使用方法ガイド

## 1. 開発環境のセットアップ

### 1.1 必要条件
- Node.js 18.x以上
- Python 3.10以上
- MongoDB（オプション）

### 1.2 初期セットアップ

1. 環境変数の設定
   ```bash
   # .env.exampleをコピーして.envを作成
   copy .env.example .env
   
   # .envファイルを編集して必要な設定を行う
   ```

2. 依存関係のインストール
   ```bash
   # フロントエンド
   scripts/build_frontend.bat
   
   # バックエンド
   scripts/build_backend.bat
   ```

## 2. アプリケーションの起動

### 2.1 開発モード
```bash
# フロントエンドとバックエンドを同時に起動
scripts/start_dev.bat

# アクセス
フロントエンド: http://localhost:3000
バックエンド API: http://localhost:5000
```

### 2.2 本番モード
```bash
# フロントエンドのビルド
scripts/build_frontend.bat

# バックエンドの起動（本番設定）
set NODE_ENV=production
scripts/build_backend.bat
```

## 3. 開発ワークフロー

### 3.1 フロントエンド開発
- `src/frontend/src/`ディレクトリで作業
- コンポーネントは`components/`に配置
- ページは`pages/`に配置
- 共通スタイルは`styles/`に配置

### 3.2 バックエンド開発
- `src/backend/`ディレクトリで作業
- APIルートは`routes/`に配置
- ビジネスロジックは`controllers/`に配置
- データモデルは`models/`に配置

### 3.3 共有リソース
- `src/shared/`ディレクトリに配置
- 型定義
- 定数
- ユーティリティ関数

## 4. テスト

### 4.1 フロントエンドテスト
```bash
cd src/frontend
npm test
```

### 4.2 バックエンドテスト
```bash
cd src/backend
python -m pytest
```

## 5. デバッグ

### 5.1 フロントエンド
- Chrome DevTools
- React Developer Tools
- Redux DevTools（Redux使用時）

### 5.2 バックエンド
- ログファイル: `logs/app.log`
- デバッグモード: `set DEBUG=true`

## 6. トラブルシューティング

### 6.1 よくある問題
1. ポートが既に使用されている
   ```bash
   # プロセスを確認
   netstat -ano | findstr :3000
   netstat -ano | findstr :5000
   
   # プロセスを終了
   taskkill /PID <プロセスID> /F
   ```

2. 依存関係のエラー
   ```bash
   # node_modulesを削除して再インストール
   cd src/frontend
   rmdir /s /q node_modules
   npm install
   ```

### 6.2 エラーログの確認
- フロントエンド: ブラウザのコンソール
- バックエンド: `logs/app.log`

## 7. デプロイ

### 7.1 本番環境の準備
1. 環境変数の設定
2. 設定ファイルの確認
3. ビルドの実行

### 7.2 デプロイ手順
1. 本番用ビルド
2. 静的ファイルの配置
3. バックエンドの起動
