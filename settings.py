# settings.py
import json
import logging
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppSettings:
    DEFAULT_SETTINGS = {
        'shortcuts': {
            'fullscreen': 'F11',
            'previous': 'Left',
            'next': 'Right',
            'help': 'F1',
            'save': 'Control-s'
        },
        'display': {
            'animations': True,
            'transition_speed': 'normal',
            'theme': 'dark'
        },
        'sound': True
    }

    def __init__(self):
        """設定クラスの初期化"""
        # デフォルト設定をコピー
        self.settings = self.DEFAULT_SETTINGS.copy()
        
        # 設定ファイルの保存先を決定
        self.settings_dir = self._get_settings_dir()
        self.settings_path = os.path.join(self.settings_dir, 'settings.json')
        
        # 設定を読み込み
        self.load()

    def _get_settings_dir(self) -> str:
        """OS毎に適切な設定ファイル保存先を取得"""
        try:
            # OSに応じて基準ディレクトリを決定
            if os.name == 'nt':  # Windows
                base_dir = os.path.expandvars('%APPDATA%')
            else:  # Unix系
                base_dir = os.path.expanduser('~/.config')
            
            # アプリケーション固有のディレクトリを作成
            settings_dir = os.path.join(base_dir, 'ancient_cipher')
            os.makedirs(settings_dir, exist_ok=True)
            return settings_dir
            
        except Exception as e:
            logging.error(f"設定ディレクトリの作成に失敗: {str(e)}")
            # 失敗した場合はカレントディレクトリを使用
            return os.path.dirname(os.path.abspath(__file__))

    def load(self) -> None:
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                self.validate_and_update(loaded_settings)
                logging.info("設定ファイルを読み込みました")
            else:
                logging.info("設定ファイルが存在しないため、デフォルト設定を使用します")
                self.save()  # デフォルト設定を保存
                
        except json.JSONDecodeError:
            logging.error("設定ファイルの形式が無効です")
            self._backup_and_reset()
            
        except Exception as e:
            logging.error(f"設定の読み込みに失敗: {str(e)}")
            self._backup_and_reset()

    def validate_and_update(self, new_settings: Dict[str, Any]) -> None:
        """設定の検証と更新"""
        try:
            validated_settings = self.DEFAULT_SETTINGS.copy()
            
            for category, values in new_settings.items():
                if category in validated_settings:
                    if isinstance(values, dict) and isinstance(validated_settings[category], dict):
                        # 辞書型の設定は既存のキーのみを更新
                        for k, v in values.items():
                            if k in validated_settings[category]:
                                validated_settings[category][k] = v
                    elif category == 'sound':
                        # サウンド設定は真偽値に変換
                        validated_settings[category] = bool(values)
            
            self.settings = validated_settings
            logging.info("設定を検証し更新しました")
            
        except Exception as e:
            logging.error(f"設定の検証に失敗: {str(e)}")
            self.settings = self.DEFAULT_SETTINGS.copy()

    def _backup_and_reset(self) -> None:
        """破損した設定ファイルのバックアップとリセット"""
        try:
            if os.path.exists(self.settings_path):
                # バックアップファイル名を生成（既存なら連番を付与）
                backup_path = f"{self.settings_path}.bak"
                counter = 1
                while os.path.exists(backup_path):
                    backup_path = f"{self.settings_path}.bak.{counter}"
                    counter += 1
                    
                # 破損ファイルをバックアップ
                os.rename(self.settings_path, backup_path)
                logging.info(f"破損した設定ファイルをバックアップ: {backup_path}")
            
            # デフォルト設定に戻してセーブ
            self.settings = self.DEFAULT_SETTINGS.copy()
            self.save()
            
        except Exception as e:
            logging.error(f"設定のバックアップに失敗: {str(e)}")

    def save(self) -> None:
        """設定の保存"""
        try:
            # 一時ファイルに保存
            temp_path = f"{self.settings_path}.tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            
            # 一時ファイルを本番ファイルに移動（アトミック操作）
            if os.path.exists(self.settings_path):
                os.replace(temp_path, self.settings_path)
            else:
                os.rename(temp_path, self.settings_path)
                
            logging.info("設定を保存しました")
            
        except PermissionError:
            logging.error("設定ファイルへの書き込み権限がありません")
            # 代替保存先（ユーザーホーム）に保存を試みる
            try:
                home_path = os.path.expanduser('~/ancient_cipher_settings.json')
                with open(home_path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, indent=4, ensure_ascii=False)
                logging.info(f"設定を代替位置に保存: {home_path}")
                
            except Exception as e:
                logging.error(f"代替位置への設定保存にも失敗: {str(e)}")
                
        except Exception as e:
            logging.error(f"設定の保存に失敗: {str(e)}")

    def get_settings(self) -> Dict[str, Any]:
        """現在の設定を取得"""
        return self.settings