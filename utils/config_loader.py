import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os

class ClineConfig:
    def __init__(self, config_path: str = "config/cline_config.yaml"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """設定ファイルを読み込む"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
            raise

    def get_api_settings(self) -> Dict[str, Any]:
        """Claude API設定を取得"""
        return self.config.get('claude_api', {})

    def get_session_settings(self) -> Dict[str, Any]:
        """セッション管理設定を取得"""
        return self.config.get('session_management', {})

    def get_error_settings(self) -> Dict[str, Any]:
        """エラーハンドリング設定を取得"""
        return self.config.get('error_handling', {})

    def get_directory_structure(self) -> Dict[str, Any]:
        """ディレクトリ構造設定を取得"""
        return self.config.get('directory_structure', {})

    def setup_project_structure(self) -> None:
        """プロジェクト構造を設定ファイルに基づいて作成"""
        structure = self.get_directory_structure()
        
        def create_directories(base_path: str, structure: Dict[str, Any]) -> None:
            for key, value in structure.items():
                path = Path(base_path) / key
                if isinstance(value, list):
                    # ファイルの場合
                    path.parent.mkdir(parents=True, exist_ok=True)
                    for file in value:
                        file_path = path / file
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        if not file_path.exists():
                            file_path.touch()
                elif isinstance(value, dict):
                    # ディレクトリの場合
                    path.mkdir(parents=True, exist_ok=True)
                    create_directories(str(path), value)

        create_directories(".", structure)

    def validate_environment(self) -> bool:
        """環境設定を検証"""
        env_config = self.config.get('environment', {})
        
        # Python バージョン確認
        python_version = env_config.get('python', {}).get('version', '')
        if python_version and not self._check_python_version(python_version):
            return False
            
        # Node.js バージョン確認
        nodejs_version = env_config.get('nodejs', {}).get('version', '')
        if nodejs_version and not self._check_nodejs_version(nodejs_version):
            return False
            
        return True

    def _check_python_version(self, required_version: str) -> bool:
        """Pythonバージョンを確認"""
        import sys
        current = sys.version_info
        required = required_version.replace('>=', '').split('.')
        return current.major >= int(required[0])

    def _check_nodejs_version(self, required_version: str) -> bool:
        """Node.jsバージョンを確認"""
        try:
            import subprocess
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            current = result.stdout.strip().replace('v', '')
            required = required_version.replace('>=', '').split('.')
            return int(current.split('.')[0]) >= int(required[0])
        except Exception:
            return False

    def update_config(self, section: str, key: str, value: Any) -> None:
        """設定を更新"""
        if section in self.config:
            self.config[section][key] = value
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        else:
            raise KeyError(f"設定セクション '{section}' が見つかりません。")
