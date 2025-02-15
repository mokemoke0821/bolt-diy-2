import tkinter as tk
from tkinter import messagebox
import logging
import os
import sys
import shutil
import json


def setup_environment():
    """環境設定を初期化"""
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))

        # 必要なディレクトリを作成
        directories = ['logs', 'resources', 'puzzles', 'screens', 'utils']
        for directory in directories:
            dir_path = os.path.join(project_root, directory)
            os.makedirs(dir_path, exist_ok=True)

        # デフォルト設定ファイルを作成
        settings_path = os.path.join(project_root, 'settings.json')
        if not os.path.exists(settings_path):
            default_settings = {
                'sound_enabled': True,
                'fullscreen': False,
                'animation_speed': 'normal'
            }
            with open(settings_path, 'w') as f:
                json.dump(default_settings, f)

    except Exception as e:
        logging.error(f"環境設定の初期化エラー: {str(e)}")
        sys.exit(1)


def setup_logging():
    """ロギングを設定"""
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'app.log')

        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True
        )
        logging.info("ロギングが設定されました")

    except Exception as e:
        print(f"ロギング設定のエラー: {str(e)}")
        sys.exit(1)


def check_dependencies():
    """依存関係をチェック"""
    required = {
        'PIL': 'Pillow',
        'tkinter': 'tkinter',
        'json': 'json',
        'logging': 'logging'
    }

    missing = []
    for package, install_name in required.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(install_name)

    if missing:
        logging.error(f"不足している依存関係: {', '.join(missing)}")
        messagebox.showerror("エラー", 
                             f"必要なパッケージが不足しています:\n{', '.join(missing)}")
        sys.exit(1)


def setup_exception_handler(root):
    """予期せぬ例外をキャッチする"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        logging.error("予期せぬエラー", 
                      exc_info=(exc_type, exc_value, exc_traceback))
        messagebox.showerror("エラー",
                             f"予期せぬエラーが発生しました:\n{str(exc_value)}")

    sys.excepthook = handle_exception


def main():
    try:
        setup_environment()
        setup_logging()
        check_dependencies()

        root = tk.Tk()
        setup_exception_handler(root)

        # ウィンドウ設定
        root.title("Ancient Cipher")
        root.configure(background='#1a1a1a')

        # 画面中央に配置
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # アプリケーション初期化
        from cipher_app import CipherApp
        app = CipherApp(root)

        # 終了処理の設定
        def on_closing():
            try:
                if messagebox.askokcancel("確認", "終了してもよろしいですか？"):
                    app.cleanup()
                    root.destroy()
                    sys.exit()
            except Exception as e:
                logging.error(f"終了処理エラー: {str(e)}")
                root.destroy()
                sys.exit(1)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    except Exception as e:
        logging.error(f"起動エラー: {str(e)}")
        messagebox.showerror("エラー", 
                             f"アプリケーションの起動に失敗しました:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
