import logging
from typing import Optional, Dict, Any, Callable
from PIL import Image, ImageTk
import os
import platform

class ResourceManager:
    def __init__(self):
        self.images: Dict[str, ImageTk.PhotoImage] = {}
        self.setup_sounds()
        self.sound_enabled = True
        self.resource_dir = self._get_resource_dir()

    def _get_resource_dir(self) -> str:
        """リソースディレクトリのパスを取得"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resource_dir = os.path.join(base_dir, 'resources')
        os.makedirs(resource_dir, exist_ok=True)
        return resource_dir

    def setup_sounds(self):
        """プラットフォームに応じたサウンド設定"""
        if platform.system() == 'Windows':
            import winsound
            self.sounds = {
                'success': lambda: winsound.Beep(1000, 100),
                'error': lambda: winsound.Beep(500, 200),
                'click': lambda: winsound.Beep(1200, 50),
                'complete': lambda: winsound.Beep(1500, 150)
            }
        else:
            # Windows以外の場合は無音処理
            self.sounds = {
                'success': lambda: None,
                'error': lambda: None,
                'click': lambda: None,
                'complete': lambda: None
            }
            logging.warning("このプラットフォームではサウンドは利用できません")

    def load_image(self, path: str) -> Optional[ImageTk.PhotoImage]:
        """画像の読み込み（改善版）"""
        try:
            if path not in self.images:
                # 絶対パスの構築
                abs_path = path if os.path.isabs(path) else os.path.join(self.resource_dir, path)
                
                if not os.path.exists(abs_path):
                    logging.error(f"画像ファイルが存在しません: {abs_path}")
                    return None
                    
                image = Image.open(abs_path)
                photo = ImageTk.PhotoImage(image)
                self.images[path] = photo
                logging.debug(f"画像を読み込みました: {path}")
            return self.images[path]
        except Exception as e:
            logging.error(f"画像の読み込みに失敗: {path} - {str(e)}")
            return None

    def play_sound(self, sound_name: str) -> None:
        """サウンド再生（改善版）"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name]()
                logging.debug(f"サウンドを再生: {sound_name}")
            except Exception as e:
                logging.error(f"サウンド再生に失敗: {sound_name} - {str(e)}")
                # エラー後はサウンドを無効化
                self.sound_enabled = False
        else:
            logging.warning(f"未定義のサウンド: {sound_name}")

    def set_sound_enabled(self, enabled: bool) -> None:
        """サウンドの有効/無効を設定"""
        self.sound_enabled = enabled
        logging.info(f"サウンドを{'有効' if enabled else '無効'}にしました")

    def cleanup(self) -> None:
        """リソースの解放（改善版）"""
        try:
            for image in self.images.values():
                if hasattr(image, 'close'):
                    image.close()
            self.images.clear()
            logging.info("リソースマネージャーのクリーンアップが完了しました")
        except Exception as e:
            logging.error(f"リソースのクリーンアップに失敗: {str(e)}")