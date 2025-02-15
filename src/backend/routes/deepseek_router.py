from flask import Blueprint, request, jsonify, current_app
from pydantic import BaseModel
import os
import requests
from typing import Optional, Dict, Any
import logging
import time
from functools import lru_cache
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Blueprintの設定
deepseek_router = Blueprint('deepseek', __name__)

# OpenRouter設定
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5
RETRY_STATUS_FORCELIST = [500, 502, 503, 504]

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# リトライ設定付きのセッション作成
def create_retry_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# レスポンスキャッシュ（1時間有効）
@lru_cache(maxsize=100)
def get_cached_response(text: str, model: str, max_tokens: int, temperature: float) -> Dict:
    return _make_openrouter_request(text, model, max_tokens, temperature)

class InferenceRequest(BaseModel):
    text: str
    model: Optional[str] = "deepseek-coder-33b-instruct"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

def _make_openrouter_request(text: str, model: str, max_tokens: int, temperature: float) -> Dict:
    """OpenRouterへのリクエストを実行する内部関数"""
    session = create_retry_session()
    
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': os.getenv('ALLOWED_REFERER', 'http://localhost:3000'),
    }

    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': text}],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }

    try:
        response = session.post(
            f'{OPENROUTER_BASE_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'OpenRouter API request failed: {str(e)}')
        raise

@deepseek_router.route('/infer', methods=['POST'])
def infer():
    try:
        # リクエストの検証
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid request. Text field is required.'
            }), 400

        inference_request = InferenceRequest(**data)

        # キャッシュされたレスポンスを取得
        try:
            result = get_cached_response(
                inference_request.text,
                inference_request.model,
                inference_request.max_tokens,
                inference_request.temperature
            )
        except requests.exceptions.RequestException as e:
            logger.error(f'API request failed after retries: {str(e)}')
            return jsonify({
                'success': False,
                'error': 'API request failed. Please try again later.'
            }), 503

        return jsonify({
            'success': True,
            'response': result['choices'][0]['message']['content'] if 'choices' in result else '',
            'model': result.get('model', inference_request.model),
            'usage': result.get('usage', {}),
            'cached': True
        })

    except Exception as e:
        logger.error(f'Error in inference: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred.'
        }), 500

@deepseek_router.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'deepseek-api'
    })
