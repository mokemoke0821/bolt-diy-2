from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from routes.deepseek_router import deepseek_router
import logging

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # CORS設定
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # ルーターの登録
    app.register_blueprint(deepseek_router, url_prefix='/api/deepseek')

    # ヘルスチェックエンドポイント
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'bolt-diy-backend'}

    return app

# アプリケーションインスタンスを作成
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    logger.info(f'Starting server on port {port} in {"debug" if debug else "production"} mode')
    app.run(host='0.0.0.0', port=port, debug=debug)
