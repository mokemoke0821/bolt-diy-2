from settings import AppSettings
from event_manager import EventManager
from resource_manager import ResourceManager
import tkinter as tk
import time
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import json
import logging
from typing import Optional, Dict, Any
from PIL import Image, ImageTk
import math
import os
import random
from game_state import GameState
from theme_manager import ThemeManager
from animation_manager import AnimationManager
from typing import Optional, Dict, Any, Callable
from puzzle_manager import PuzzleManager
from puzzles.circular_cipher import CircularCipherPuzzle
from puzzles.dual_dial import DualDialCipher
from puzzles.final_cipher import FinalCipher
import sys
class CipherApp:
    # theme_manager.py の ThemeManager クラスを更新
    def __init__(self, root):
        self.root = root
        self.root.title("Ancient Cipher")
            
        # マネージャーの初期化
        self.settings = AppSettings()
        self.event_manager = EventManager(root)
        self.resource_manager = ResourceManager()
        self.theme_manager = ThemeManager()
        self.animation_manager = AnimationManager(root)
        self.game_state = GameState(root, self.animation_manager)
            
        # アプリケーションの状態管理
        self.state = {
            'is_fullscreen': False,
            'animation_enabled': True,
            'current_slide': 0,
            'solved_puzzles': set()
        }
            
        # パズルの説明文
        self.puzzle_descriptions = {
            1: """最古の暗号装置が起動しました。
            この装置は、文字を2桁の数字に変換する
            シンプルな機構を持っています。
            
            解読のヒント:
            - 2桁の数字は1つのアルファベットに対応
            - 変換表を参考に規則性を見つけ出せ
            - 意味のある英単語になるはず""",
            
            2: """第2の暗号装置が起動しました。
            この装置は特定のパターンで数値を変換します。
            
            解読のヒント:
            - 入力と出力の対応から規則性を見つけ出せ
            - 計算ユニットの動作を理解せよ
            - 変換後の数字を文字に置き換えると...
            - 最終的に意味のある英単語になる""",
            
            3: """円環暗号装置が起動しました。
            この装置は文字を円環状に配置し、回転させることで暗号化を行います。
            
            解読のヒント:
            - 外側の環は数字を表示
            - 内側の環は文字を表示
            - 環を回転させることで対応が変化
            - 最初の文字は 'f' であることが判明""",
            
            4: """二重暗号システムが起動しました。

            解読のヒント:
            - 赤と青のダイヤルは、それぞれ4文字の英単語を示しています
            - 赤のダイヤル(A-D)と青のダイヤル(W-Z)を組み合わせると8文字の単語になります
            - 各ダイヤルを切り替えると、数字のパターンが変化します
            - 数字の組み合わせが意味のある単語を表しています
            
            目標：「子供たち」を意味する8文字の英単語を見つけ出せ！""",
            
            5: """最終暗号装置が起動しました。
            この装置は3つのモードを組み合わせた最も高度な暗号化システムです。
            
            解読のヒント:
            - MODE-α: 通常の文字を処理
            - MODE-β: 特殊文字を処理
            - MODE-γ: スペースを処理
            
            2つの単語を組み合わせたフレーズになります"""
        }

        # スライドの内容を管理
        self.slides = [
            self.create_intro_slide,
            self.create_puzzle_one,
            self.create_puzzle_two,
            self.create_puzzle_three,
            self.create_puzzle_four,
            self.create_puzzle_five,
            self.create_birthday
        ]
            
        # コールバックの設定
        self._setup_callbacks()
            
        # アプリケーションのセットアップを実行
        self.setup_application()
    def setup_ui(self):
        """UIコンポーネントの初期化"""
        # メインフレームの設定
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill='both', expand=True)

        # ステータスバーの作成
        self.create_status_bar()
        
        # ナビゲーションの作成
        self.create_navigation()

        # テーマの初期設定
        self.theme_manager.apply_theme('cyber')
        
        # タイマーの初期化
        self.start_timer()
        # パズルマネージャーの初期化を追加
        self.puzzle_manager = PuzzleManager(self.game_state, self.resource_manager)
    def start_timer(self):
        """タイマーの開始"""
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """タイマーの更新"""
        if hasattr(self, 'start_time'):
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.configure(text=f"経過時間: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
    def show_help(self):
        """ヘルプ画面を表示"""
        tk.messagebox.showinfo("ヘルプ", "ここにヘルプの内容を記載してください。")
    def _setup_callbacks(self):
        """コールバック関数の登録"""
        callbacks = {
            'fullscreen': self.toggle_fullscreen,
            'previous': self.prev_slide,
            'next': self.next_slide,
            'help': self.show_help,
            'save': self.save_progress
        }
        for action, callback in callbacks.items():
            self.event_manager.register_callback(action, callback)

    def setup_application(self):
        """アプリケーションのセットアップ"""
        try:
            logging.info("アプリケーションのセットアップを開始")
            
            # ウィンドウの基本設定
            self.root.configure(background='#1a1a1a')  # バックグラウンドカラーを設定
            
            # メインフレームが存在する場合は削除
            if hasattr(self, 'main_frame'):
                self.main_frame.destroy()
            
            # 新しいメインフレームを作成
            self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
            self.main_frame.pack(fill='both', expand=True)
            
            # UI初期化の前にスタイルを設定
            self.setup_style()
            logging.info("スタイルの設定完了")
            
            # UI初期化
            self.setup_ui()
            logging.info("UIの初期化完了")
            
            # サウンドの設定
            self.setup_sounds()
            logging.info("サウンドの設定完了")
            
            # メニューの作成
            self.create_menu()
            logging.info("メニューの作成完了")

            # イベントとショートカットの設定
            self.event_manager.bind_shortcuts(self.settings.settings['shortcuts'])
            logging.info("ショートカットの設定完了")
            
            # 初期スライドの表示
            self.show_slide(0)
            logging.info("初期スライドの表示完了")
            
            # 明示的に更新を要求
            self.root.update()
            logging.info("アプリケーションのセットアップ完了")
            
        except Exception as e:
            logging.error(f"アプリケーションの初期化に失敗: {str(e)}", exc_info=True)
            messagebox.showerror("エラー", 
                            f"アプリケーションの初期化に失敗しました:\n{str(e)}")
    # cipher_app.py のスタイル設定を更新
    def setup_style(self):
        style = ttk.Style()
        
        # サイバー風のスタイル設定
        style.configure('Cyber.TFrame',
                    background='#001122')
        
        style.configure('Cyber.TLabelframe',
                    background='#001122',
                    foreground='#00FFFF')
        
        style.configure('Cyber.TLabelframe.Label',
                    background='#001122',
                    foreground='#00FFFF',
                    font=('Courier', 10))
        
        style.configure('CyberText.TLabel',
                    background='#1a1a1a',
                    foreground='#00FF00',
                    font=('Helvetica', 12))
        
        style.configure('Cyber.TButton',
                    padding=5,
                    relief='raised',
                    background='#002244',
                    foreground='#00FFFF')
        
        style.configure('Cyber.TEntry',
                    fieldbackground='#1a1a1a',
                    foreground='#00FFFF',
                    insertcolor='#00FFFF')
    def setup_sounds(self):
        """サウンド設定"""
        self.resource_manager.set_sound_enabled(self.settings.settings['sound'])

    def play_sound(self, sound_name: str):
        """サウンド再生"""
        self.resource_manager.play_sound(sound_name)

    def create_menu(self):
        """メニューバーの作成"""
        menubar = tk.Menu(self.root)  # self.root.configの前にmenubarを定義
        self.root.config(menu=menubar)
        
        # ファイルメニュー
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="進捗を保存", command=self.save_progress)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.confirm_exit)
        
        # 表示メニュー
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="表示", menu=view_menu)
        self.fullscreen_var = tk.BooleanVar(value=self.state['is_fullscreen'])
        view_menu.add_checkbutton(label="全画面表示", 
                                command=self.toggle_fullscreen,
                                variable=self.fullscreen_var)
    def create_status_bar(self):
        """ステータスバーの作成"""
        self.status_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.status_frame.pack(side='bottom', fill='x')

        # スコア表示を作成してGameStateに登録
        score_label = ttk.Label(self.status_frame,
                            text="スコア: 0",
                            style='Text.TLabel')
        score_label.pack(side='left', padx=10)
        self.game_state.setup_score_display(score_label)

        # ヒント残数表示
        self.hints_label = ttk.Label(self.status_frame,
                                    text="ヒント: 3",
                                    style='Text.TLabel')
        self.hints_label.pack(side='left', padx=10)

        # タイマー表示
        self.timer_label = ttk.Label(self.status_frame,
                                    text="経過時間: 00:00",
                                    style='Text.TLabel')
        self.timer_label.pack(side='right', padx=10)
    def create_navigation(self):
        """ナビゲーションバーの作成"""
        # ナビゲーションフレームの作成
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(side='bottom', fill='x', pady=10)
        
        # 前へボタン
        self.prev_button = ttk.Button(self.nav_frame, 
                                    text="◀ 前へ",
                                    style='Cyber.TButton',
                                    command=self.prev_slide)
        self.prev_button.pack(side='left', padx=5)
        
        # 次へボタン
        self.next_button = ttk.Button(self.nav_frame,
                                    text="次へ ▶",
                                    style='Cyber.TButton',
                                    command=self.next_slide)
        self.next_button.pack(side='right', padx=5)
        
        # スライド番号ラベル
        self.slide_label = ttk.Label(self.nav_frame,
                                    text="1/7",
                                    style='CyberText.TLabel')
        self.slide_label.pack(side='right', padx=20)
    def show_slide(self, index: int):
        """スライドの表示"""
        if not 0 <= index < len(self.slides):
            logging.warning(f"無効なスライドインデックス: {index}")
            return

        try:
            # 古いスライドのクリーンアップ
            if hasattr(self, 'current_slide_frame'):
                self.animation_manager.fade_out(self.current_slide_frame)
                self.current_slide_frame.destroy()

            # 新しいスライドを作成
            self.current_slide_frame = ttk.Frame(self.root)
            self.current_slide_frame.pack(fill='both', expand=True)

            self.state['current_slide'] = index
            self.slides[index](self.current_slide_frame)

            # フェードインの追加
            self.animation_manager.fade_in(self.current_slide_frame)

            # ナビゲーションの更新
            self.update_navigation_buttons()
            self.update_slide_number()
        except Exception as e:
            logging.error(f"スライド表示エラー: {str(e)}", exc_info=True)
            self.show_error_message(f"スライドの表示に失敗しました: {e}")

    def _cleanup_old_frame(self, old_frame):
        """古いフレームのクリーンアップ"""
        try:
            if old_frame and old_frame.winfo_exists():
                old_frame.destroy()
        except Exception as e:
            logging.error(f"フレームのクリーンアップに失敗: {str(e)}")

    def next_slide(self):
        """次のスライドへ"""
        current = self.state['current_slide']
        if current < len(self.slides) - 1:
            self.show_slide(current + 1)

    def prev_slide(self):
        """前のスライドへ"""
        current = self.state['current_slide']
        if current > 0:
            self.show_slide(current - 1)

    def cleanup_current_slide(self):
        """現在のスライドのクリーンアップ"""
        if hasattr(self, 'main_frame'):
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.delete('all')
                widget.destroy()

    def update_slide_number(self):
        """スライド番号の更新"""
        self.slide_label.configure(
            text=f"{self.state['current_slide'] + 1}/{len(self.slides)}"
        )

    def update_navigation_buttons(self):
        """ナビゲーションボタンの状態更新"""
        logging.info(f"現在のスライド: {self.state['current_slide']}")
        logging.info(f"スライド数: {len(self.slides)}")

        # 前へボタンの状態を設定
        if self.state['current_slide'] > 0:
            self.prev_button.state(['!disabled'])
            logging.info("前へボタンを有効化")
        else:
            self.prev_button.state(['disabled'])
            logging.info("前へボタンを無効化")

        # 次へボタンの状態を設定
        if self.state['current_slide'] < len(self.slides) - 1:
            self.next_button.state(['!disabled'])
            logging.info("次へボタンを有効化")
        else:
            self.next_button.state(['disabled'])
            logging.info("次へボタンを無効化")
    
    def prev_slide(self):
        """前のスライドへ移動"""
        if self.state['current_slide'] > 0:
            if self.state['animation_enabled']:
                self.animate_slide_transition('prev')
            else:
                self.show_slide(self.state['current_slide'] - 1)
            self.play_sound('click')

    def next_slide(self):
        """次のスライドへ移動"""
        logging.info(f"現在のスライド: {self.state['current_slide']}")
        if self.state['current_slide'] < len(self.slides) - 1:
            try:
                if self.state['animation_enabled']:
                    self.animate_slide_transition('next')
                else:
                    self.show_slide(self.state['current_slide'] + 1)
                self.play_sound('click')
            except Exception as e:
                logging.error(f"スライド遷移エラー: {str(e)}")

    def animate_slide_transition(self, direction: str):
        """スライド遷移のアニメーション"""
        old_frame = ttk.Frame(self.root)
        old_frame.place(x=0, y=0, relwidth=1, relheight=1)

        for widget in self.main_frame.winfo_children():
            widget.lift()  # 明示的に順序を変更

        new_index = self.state['current_slide'] + (1 if direction == 'next' else -1)
        self.show_slide(new_index)

        # アニメーションの設定
        speed = self.settings.settings['display']['transition_speed']
        duration = {'slow': 20, 'normal': 10, 'fast': 5}[speed]

        def animate_step(step=0):
            if step <= 10:
                distance = self.root.winfo_width() * (0.1 * (10 - step))
                x = distance if direction == 'next' else -distance
                old_frame.place(x=x)
                self.root.after(duration, lambda: animate_step(step + 1))
            else:
                old_frame.destroy()

        animate_step()


    def toggle_fullscreen(self):
        """フルスクリーンモードの切り替え"""
        self.state['is_fullscreen'] = not self.state['is_fullscreen']
        self.root.attributes('-fullscreen', self.state['is_fullscreen'])
        self.fullscreen_var.set(self.state['is_fullscreen'])
        self.play_sound('click')

    def save_progress(self):
        """進捗状況の保存（改善版）"""
        progress = {
            'current_slide': self.state['current_slide'],
            'solved_puzzles': list(self.state['solved_puzzles']),
            'score': self.game_state.get_score(),
            'hints_remaining': self.game_state.get_hints_remaining(),
            'timestamp': time.time(),
            'completed_hints': self.game_state.hint_levels
        }
        
        try:
            # 一時ファイルに保存
            temp_file = 'progress_temp.json'
            with open(temp_file, 'w') as f:
                json.dump(progress, f)
                
            # 成功したら本番ファイルに移動
            os.replace(temp_file, 'progress.json')
            self.show_message("進捗を保存しました", "success")
            
        except Exception as e:
            logging.error(f"進捗の保存に失敗: {str(e)}")
            self.show_message("進捗の保存に失敗しました", "error")
    def confirm_exit(self):
        """終了確認と処理"""
        if messagebox.askokcancel("終了確認", "進捗を保存して終了しますか？"):
            try:
                self.save_progress()  # 進捗保存
                self.cleanup()       # クリーンアップ
                self.root.quit()     # メインループ終了
                self.root.destroy()  # ウィンドウ破棄
                sys.exit(0)         # プログラム終了
            except Exception as e:
                logging.error(f"終了処理エラー: {str(e)}")
                self.root.destroy()  # エラー時は強制終了
                sys.exit(1)

    def cleanup(self):
        """アプリケーションのクリーンアップ"""
        try:
            self.resource_manager.cleanup()
            self.event_manager.unbind_all()
            self.settings.save()
            # ゲーム状態の保存
            self.game_state.save_state()
        except Exception as e:
            logging.error(f"クリーンアップに失敗: {str(e)}")

    def check_answer(self, puzzle_number):
        """問題の回答をチェック"""
        answers = {
            1: "river",
            2: "bread",
            3: "forest",
            4: "children",
            5: "brick house"
        }
        
        if self.answer_var.get().lower() == answers[puzzle_number]:
            self.resource_manager.play_sound('success')
            self.state['solved_puzzles'].add(puzzle_number)
            self.game_state.update_score(100)  # スコア更新
            self.save_progress()
            self.show_success_message()
            self.root.after(2000, self.next_slide)
        else:
            self.resource_manager.play_sound('error')
            self.game_state.update_score(-10)  # 不正解時のペナルティ
            self.show_error_message()

    def show_message(self, message: str, message_type: str = "info"):
        """メッセージ表示"""
        colors = {
            "success": "#00ff00",
            "error": "#ff0000",
            "info": "#ffffff",
            "warning": "#ffff00"
        }
        
        message_window = tk.Toplevel(self.root)
        message_window.configure(bg='#1a1a1a')
        message_window.overrideredirect(True)
        
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 200
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 50
        message_window.geometry(f"400x100+{x}+{y}")
        
        ttk.Label(message_window,
                 text=message,
                 font=('Helvetica', 14),
                 foreground=colors.get(message_type, "#ffffff")).pack(pady=20)
        
        if message_type == "success":
            self.play_sound('success')
        elif message_type == "error":
            self.play_sound('error')
        
        message_window.after(1500, message_window.destroy)
    # cipher_app.py に追加
    def show_hint(self, puzzle_number):
        """ヒントの改善版表示"""
        hint = self.game_state.use_hint(puzzle_number)
        if hint:
            hint_window = tk.Toplevel(self.root)
            hint_window.configure(bg=self.theme_manager.get_current_theme_colors()['background'])
            hint_window.attributes('-topmost', True)
            
            # ウィンドウ位置を画面中央に設定
            x = self.root.winfo_x() + self.root.winfo_width()//2 - 200
            y = self.root.winfo_y() + self.root.winfo_height()//2 - 100
            hint_window.geometry(f"400x200+{x}+{y}")
            
            # ヒント表示
            hint_text = ttk.Label(hint_window,
                            text=hint,
                            wraplength=350,
                            style='Text.TLabel')
            hint_text.pack(pady=20, padx=20)
            
            # 閉じるボタンの追加
            close_button = ttk.Button(hint_window,
                                text="閉じる",
                                command=hint_window.destroy)
            close_button.pack(pady=10)
            
            # スコア減少とヒント残数の更新
            self.game_state.update_score(-50)
            self.game_state.update_hints_display(self.hints_label)
        else:
            self.show_message("ヒントを使い切りました", "error")
    def show_success_message(self):
        """正解時のメッセージ表示"""
        success_window = tk.Toplevel(self.root)
        theme_colors = self.theme_manager.get_current_theme_colors()
        success_window.configure(bg=theme_colors['background'])
        success_window.attributes('-topmost', True)
        
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 200
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 100
        success_window.geometry(f"400x200+{x}+{y}")
        
        # 成功メッセージ
        message = ttk.Label(success_window,
                        text="正解！",
                        font=('Helvetica', 24, 'bold'),
                        foreground=theme_colors['success'])
        message.pack(pady=20)
        
        # アニメーション効果を適用
        self.animation_manager.fade_in(success_window)
        
        # 得点アップのメッセージ
        points = 100  # 基本点
        bonus = self.game_state.calculate_bonus()  # ボーナス点
        total = points + bonus
        
        ttk.Label(success_window,
                text=f"+{total} points!",
                font=('Helvetica', 18),
                foreground=theme_colors['success']).pack(pady=10)
        
        success_window.after(2000, success_window.destroy)

    def show_error_message(self, message="エラーが発生しました"):
        """エラーメッセージを表示"""
        error_window = tk.Toplevel(self.root)
        error_window.configure(bg='#1a1a1a')
        
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 200
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 100
        error_window.geometry(f"400x200+{x}+{y}")
        
        ttk.Label(error_window,
                text=message,
                font=('Helvetica', 24, 'bold'),
                foreground='#ff0000').pack(pady=20)
        
        error_window.after(2000, error_window.destroy)

    def show_result_screen(self):
        """結果画面の表示"""
        result_window = tk.Toplevel(self.root)
        result_window.title("クリア結果")
        result_window.configure(bg=self.theme_manager.get_current_theme_colors()['background'])
        
        ttk.Label(result_window,
                text="クリア おめでとうございます！",
                style='Title.TLabel').pack(pady=20)
                
        ttk.Label(result_window,
                text=f"最終スコア: {self.game_state.get_score()}",
                style='Text.TLabel').pack(pady=10)
        
        if self.game_state.get_score() > self.game_state.get_high_score():
            ttk.Label(result_window,
                    text="新記録達成！",
                    style='Success.TLabel').pack(pady=10)
    
    def create_decoration_line(self, parent):
        """装飾的なラインを作成"""
        line_frame = ttk.Frame(parent)
        line_frame.pack(fill='x', padx=100)
        ttk.Label(line_frame,
                 text="="*50,
                 font=('Courier', 12),
                 foreground='#00ff00').pack()

    def place_items_on_circle(self, items, radius, color, center_x, center_y):
        """円周上にアイテムを配置"""
        for i, item in enumerate(items):
            angle = math.radians(i * 60)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.cipher_canvas.create_text(x, y,
                                         text=str(item),
                                         font=('Courier', 14),
                                         fill=color)

    def rotate_dial(self):
        """ダイヤルを回転させる"""
        self.play_sound('rotation')

    def dial_click(self, dial_type: str, letter: str):
        """ダイヤルのクリックを処理"""
        self.play_sound('click')

    def check_final_answer(self):
        """最終問題の回答をチェック"""
        if self.answer_var.get().lower() == "brick house":
            self.play_sound('complete')
            self.state['solved_puzzles'].add(5)
            self.save_progress()
            self.show_final_success()
        else:
            self.play_sound('error')
            self.show_error_message()

    def create_dial_with_buttons(self, parent, dial_type):
        """ダイヤル制御インターフェースを作成"""
        value_frame = ttk.Frame(parent)
        value_frame.pack(pady=5)
        
        ttk.Label(value_frame,
                 text="VALUE:",
                 font=('Courier', 8)).pack(side='left')
        ttk.Label(value_frame,
                 text="1",
                 font=('Courier', 14),
                 foreground='#ffff00').pack(side='left', padx=5)

        control_frame = ttk.Frame(parent)
        control_frame.pack(pady=5)
        
        ttk.Button(control_frame,
                  text="-",
                  width=3,
                  command=lambda: self.adjust_dial(dial_type, -1)).pack(side='left', padx=2)
        ttk.Button(control_frame,
                  text="+",
                  width=3,
                  command=lambda: self.adjust_dial(dial_type, 1)).pack(side='left', padx=2)

    def adjust_dial(self, dial_type: str, value: int):
        """ダイヤル値を調整"""
        self.play_sound('click')
    def create_intro_slide(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        title_frame = ttk.Frame(frame)
        title_frame.pack(pady=20, fill='x')
        
        self.create_decoration_line(title_frame)
        title = ttk.Label(title_frame, 
                         text="発掘調査団特別レポート",
                         font=('Helvetica', 32, 'bold'))
        title.pack(pady=10)
        
        subtitle = ttk.Label(title_frame,
                           text="プロジェクトコード: ENIGMA-X",
                           font=('Courier', 18))
        subtitle.pack(pady=5)
        self.create_decoration_line(title_frame)
        
        info_frame = ttk.LabelFrame(frame, text="調査情報")
        info_frame.pack(pady=30, padx=50)
        
        info = [
            ("発見場所", "南方遺跡群 地下深層部"),
            ("発見日時", "2024年1月5日"),
            ("調査責任者", "Dr. なおちゃん"),
            ("機密レベル", "LEVEL-S")
        ]
        
        for label, value in info:
            info_row = ttk.Frame(info_frame)
            info_row.pack(pady=10, padx=20, fill='x')
            ttk.Label(info_row,
                     text=f"{label}:",
                     font=('Courier', 12)).pack(side='left', padx=10)
            ttk.Label(info_row,
                     text=value,
                     font=('Courier', 12)).pack(side='left', padx=10)
        
        desc_frame = ttk.Frame(frame)
        desc_frame.pack(pady=30, padx=50)
        
        description = """
        地下深層部で発見された5台の謎の装置について報告いたします。
        これらの装置は、古代文明の暮らしを記録した「生活記録装置」と推測されています。
        各装置は異なる時代に作られたと見られ、技術の進化が確認できます。
        """
        
        ttk.Label(desc_frame,
                 text=description,
                 wraplength=600,
                 justify='left',
                 font=('Helvetica', 12)).pack()
    def create_puzzle_base(self, parent, title, puzzle_number):
        """パズル画面の基本レイアウトを作成"""
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='both', expand=True)
        
        # タイトルフレーム
        title_frame = ttk.Frame(frame, style='Main.TFrame')
        title_frame.pack(pady=20, fill='x')
        
        self.create_decoration_line(title_frame)
        ttk.Label(title_frame, 
                text=title,
                style='Title.TLabel').pack(pady=10)
        self.create_decoration_line(title_frame)

        # コンテンツ用の2カラムレイアウト
        content_frame = ttk.Frame(frame, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20)
        
        # パズル表示エリア（左側）
        puzzle_frame = ttk.LabelFrame(content_frame, 
                                    text="PUZZLE AREA",
                                    style='Main.TLabelframe')
        puzzle_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # 情報表示エリア（右側）
        info_frame = ttk.LabelFrame(content_frame,
                                text="INFORMATION",
                                style='Main.TLabelframe')
        info_frame.pack(side='right', fill='both', expand=True, padx=10)

        return frame, puzzle_frame, info_frame
    def create_cipher_display(self, parent, cipher_text, description=""):
        """暗号表示エリアの作成"""
        display_frame = ttk.LabelFrame(parent, text="CIPHER TEXT", style='Main.TLabelframe')
        display_frame.pack(pady=10, padx=20, fill='x')
        
        # 暗号テキストの表示
        cipher_label = ttk.Label(display_frame,
                            text=cipher_text,
                            font=('DS-Digital', 40) if 'DS-Digital' in tkfont.families() else ('Courier', 40),
                            style='Cipher.TLabel')
        cipher_label.pack(pady=10)
        
        if description:
            ttk.Label(display_frame,
                    text=description,
                    style='Text.TLabel').pack(pady=(0, 10))
        
        return cipher_label
    def create_puzzle_info(self, parent, puzzle_number, description):
        """パズル情報エリアの作成"""
        # ミッション情報
        mission_frame = ttk.LabelFrame(parent, text="ミッション情報",
                                    style='Cyber.TLabelframe')
        mission_frame.pack(pady=10, padx=20, fill='x')
        
        desc_label = ttk.Label(mission_frame,
                            text=description,
                            wraplength=300,
                            justify='left',
                            style='CyberText.TLabel')
        desc_label.pack(pady=10, padx=10)
        
        # 解答入力エリア
        answer_frame = ttk.LabelFrame(parent, text="解答入力",
                                    style='Cyber.TLabelframe')
        answer_frame.pack(pady=10, padx=20, fill='x')
        
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(answer_frame,
                            textvariable=self.answer_var,
                            font=('Courier', 14))
        answer_entry.pack(pady=10, padx=10, fill='x')
        
        # ボタンフレーム
        button_frame = ttk.Frame(answer_frame)
        button_frame.pack(pady=10)
        
        hint_button = ttk.Button(button_frame,
                            text="ヒントを表示",
                            command=lambda: self.show_hint(puzzle_number))
        hint_button.pack(side='left', padx=5)
        
        check_button = ttk.Button(button_frame,
                                text="解答をチェック",
                                command=lambda: self.check_answer(puzzle_number))
        check_button.pack(side='right', padx=5)
        
        return answer_entry
    def create_conversion_table(self, parent):
        """変換表の作成"""
        table_frame = ttk.LabelFrame(parent, text="Conversion Table")
        table_frame.pack(pady=10, padx=20, fill='x')
        
        table_contents = [
            ('01', 'a'), ('08', 'h'), ('15', 'o'), ('22', 'v'),
            ('02', 'b'), ('09', 'i'), ('16', 'p'), ('23', 'w'),
            ('03', 'c'), ('10', 'j'), ('17', 'q'), ('24', 'x'),
            ('04', 'd'), ('11', 'k'), ('18', 'r'), ('25', 'y'),
            ('05', 'e'), ('12', 'l'), ('19', 's'), ('26', 'z'),
            ('06', 'f'), ('13', 'm'), ('20', 't'), ('27', ' '),
            ('07', 'g'), ('14', 'n'), ('21', 'u')
        ]
        
        grid_frame = ttk.Frame(table_frame)
        grid_frame.pack(pady=10)
        
        for i, (num, letter) in enumerate(table_contents):
            row = i // 4
            col = i % 4
            cell_frame = ttk.Frame(grid_frame)
            cell_frame.grid(row=row, column=col, padx=5, pady=2)
            ttk.Label(cell_frame,
                    text=f"{num} → {letter}",
                    font=('Courier', 12)).pack()
    def create_puzzle_one(self, parent):
        """第1問の作成"""
        frame, puzzle_frame, info_frame = self.create_puzzle_base(
            parent,
            "第1問 - 最古の記録装置",
            1
        )
        
        # 暗号表示部分の作成
        self.create_cipher_display(puzzle_frame, "18 09 22 05 18")
        
        # 変換表の作成
        self.create_conversion_table(puzzle_frame)
        
        # 情報とインプット部分の作成
        description = """
        最古の暗号装置が起動しました。
        この装置は、文字を2桁の数字に変換する
        シンプルな機構を持っています。

        解読のヒント:
        - 2桁の数字は1つのアルファベットに対応
        - 変換表を参考に規則性を見つけ出せ
        - 意味のある英単語になるはず
        """
        self.create_puzzle_info(info_frame, 1, description)
        
        # アニメーション効果を適用
        self.animation_manager.fade_in(frame)   
    def create_puzzle_two(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        title_frame = ttk.Frame(frame)
        title_frame.pack(pady=20, fill='x')
        
        self.create_decoration_line(title_frame)
        title = ttk.Label(title_frame, 
                         text="第2問 - 技術の痕跡",
                         font=('Helvetica', 24, 'bold'))
        title.pack(pady=10)
        self.create_decoration_line(title_frame)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill='both', expand=True, padx=20)

        device_frame = ttk.LabelFrame(content_frame, text="PATTERN ANALYSIS DEVICE")
        device_frame.pack(side='left', fill='both', expand=True, padx=10)

        display_frame = ttk.LabelFrame(device_frame, text="ENCRYPTED INPUT")
        display_frame.pack(pady=10, padx=20, fill='x')
        ttk.Label(display_frame,
                 text="9 41 15 7 13",
                 font=('DS-Digital', 40) if 'DS-Digital' in tkfont.families() else ('Courier', 40),
                 foreground='#00ff00').pack(pady=10)

        analysis_frame = ttk.LabelFrame(device_frame, text="PATTERN ANALYSIS")
        analysis_frame.pack(pady=10, padx=20, fill='x')

        patterns = [
            ("1", "7"),
            ("2", "9"),
            ("3", "11"),
            ("4", "13"),
            ("5", "15")
        ]

        table_frame = ttk.Frame(analysis_frame)
        table_frame.pack(pady=10)

        for i, (input_val, output_val) in enumerate(patterns, 1):
            ttk.Label(table_frame,
                     text=input_val,
                     font=('Courier', 12)).grid(row=i, column=0, padx=10, pady=2)
            ttk.Label(table_frame,
                     text="→",
                     font=('Courier', 12)).grid(row=i, column=1, padx=10, pady=2)
            ttk.Label(table_frame,
                     text=output_val,
                     font=('Courier', 12)).grid(row=i, column=2, padx=10, pady=2)

        info_frame = ttk.LabelFrame(content_frame, text="Mission Information")
        info_frame.pack(side='right', fill='both', expand=True, padx=10)

        description = """
        第2の暗号装置が起動しました。
        この装置は特定のパターンで数値を変換します。

        解読のヒント:
        - 入力と出力の対応から規則性を見つけ出せ
        - 計算ユニットの動作を理解せよ
        - 変換後の数字を文字に置き換えると...
        - 最終的に意味のある英単語になる
        """

        ttk.Label(info_frame,
                 text=description,
                 wraplength=300,
                 justify='left',
                 font=('Helvetica', 12)).pack(pady=20, padx=20)

        input_frame = ttk.LabelFrame(info_frame, text="Answer Input")
        input_frame.pack(fill='x', padx=20, pady=20)

        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(input_frame,
                               textvariable=self.answer_var,
                               font=('Courier', 14))
        answer_entry.pack(pady=10, padx=10, fill='x')

        check_button = ttk.Button(input_frame,
                                text="CHECK ANSWER",
                                command=lambda: self.check_answer(2))
        check_button.pack(pady=10)

        answer_entry.bind('<Return>', lambda e: self.check_answer(2))

    def create_puzzle_three(self, parent):
        """第3問 - 円環暗号"""
        # メインフレーム
        main_frame = ttk.Frame(parent, style='Main.TFrame')
        main_frame.pack(fill='both', expand=True)
        
        # 問題文エリア（固定配置）
        desc_frame = ttk.LabelFrame(main_frame, text="Mission Information", style='Main.TLabelframe')
        desc_frame.pack(fill='x', padx=20, pady=5)
        
        desc_text = tk.Text(desc_frame, wrap='word', height=6, font=('Helvetica', 10))
        desc_text.insert('1.0', self.puzzle_descriptions[3])
        desc_text.configure(state='disabled')
        desc_text.pack(fill='x', padx=5, pady=5)
        
        # パズルエリア
        puzzle_frame = ttk.Frame(main_frame)
        puzzle_frame.pack(fill='both', expand=True, padx=20)
        
        # 制御ボタン
        control_frame = ttk.Frame(puzzle_frame)
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame, 
                text="時計回り",
                command=lambda: self.cipher_puzzle.rotate(60)).pack(side='left', padx=5)
        ttk.Button(control_frame,
                text="反時計回り", 
                command=lambda: self.cipher_puzzle.rotate(-60)).pack(side='left', padx=5)
        
        self.angle_label = ttk.Label(control_frame, text="0°")
        self.angle_label.pack(side='left', padx=20)
        
        # 暗号表示
        cipher_frame = ttk.LabelFrame(puzzle_frame, text="CIPHER TEXT")
        cipher_frame.pack(fill='x', pady=5)
        ttk.Label(cipher_frame,
                text="4 3 5 1 1 4",
                font=('DS-Digital', 40)).pack(pady=10)
        
        # 円環メカニズム
        canvas = tk.Canvas(puzzle_frame, width=400, height=400, bg='#1a1a1a')
        canvas.pack(pady=10)
        self.cipher_puzzle = CircularCipherPuzzle(canvas, self.root)
        
        # 解答入力エリア
        answer_frame = ttk.LabelFrame(main_frame, text="Answer Input")
        answer_frame.pack(fill='x', padx=20, pady=5)
        
        self.answer_var = tk.StringVar()
        ttk.Entry(answer_frame,
                textvariable=self.answer_var).pack(fill='x', padx=5, pady=5)
        
        button_frame = ttk.Frame(answer_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame,
                text="ヒントを表示",
                command=lambda: self.show_hint(3)).pack(side='left')
        ttk.Button(button_frame,
                text="解答をチェック",
                command=lambda: self.check_answer(3)).pack(side='right')

        return main_frame
    def create_intro_slide(self, parent):
        """イントロスライドの作成"""
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        # タイトルセクション
        title_frame = ttk.Frame(frame)
        title_frame.pack(fill='x', pady=20)
        
        self.create_decoration_line(title_frame)
        title = ttk.Label(title_frame, 
                        text="発掘調査団特別レポート",
                        style='Title.TLabel')
        title.pack(pady=10)
        
        subtitle = ttk.Label(title_frame,
                        text="プロジェクトコード: ENIGMA-X",
                        style='Subtitle.TLabel')
        subtitle.pack(pady=5)
        self.create_decoration_line(title_frame)
        
        # 情報セクション
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        info_frame = ttk.LabelFrame(content_frame, text="調査情報")
        info_frame.pack(fill='x', pady=10)
        
        info = [
            ("発見場所", "南方遺跡群 地下深層部"),
            ("発見日時", "2024年1月5日"),
            ("調査責任者", "Dr. なおちゃん"),
            ("機密レベル", "LEVEL-S")
        ]
        
        for label, value in info:
            row = ttk.Frame(info_frame)
            row.pack(fill='x', pady=5, padx=20)
            ttk.Label(row,
                    text=f"{label}:",
                    width=15,
                    anchor='e').pack(side='left', padx=10)
            ttk.Label(row,
                    text=value).pack(side='left', padx=10)
        
        # 説明セクション
        desc_frame = ttk.LabelFrame(content_frame, text="調査概要")
        desc_frame.pack(fill='both', expand=True, pady=10)
        
        description = """
        地下深層部で発見された5台の謎の装置について報告いたします。
        これらの装置は、古代文明の暮らしを記録した「生活記録装置」と推測されています。
        各装置は異なる時代に作られたと見られ、技術の進化が確認できます。
        
        解読には特別な知識と技術が必要とされ、現在解析を進めています。
        """
        
        ttk.Label(desc_frame,
                text=description,
                wraplength=600,
                justify='left').pack(fill='both', expand=True, padx=20, pady=10)
        
        return frame
    def draw_circular_mechanism(self):
        center_x = 150
        center_y = 150
        
        self.cipher_canvas.create_oval(20, 20, 280, 280,
                                     outline='#00ff00',
                                     width=2)
        
        self.cipher_canvas.create_oval(60, 60, 240, 240,
                                     outline='#00ff00',
                                     width=2)

        numbers = list(range(1, 7))
        self.place_items_on_circle(numbers, 130, '#00ff00', center_x, center_y)

        letters = ['f', 'o', 'r', 'e', 's', 't']
        self.place_items_on_circle(letters, 90, '#ffff00', center_x, center_y)
    # cipher_app.py内のcreate_puzzle_four関数を修正

    def create_puzzle_four(self, parent):
        """第4問 - 二重の暗号"""
        frame, puzzle_frame, info_frame = self.create_puzzle_base(
            parent,
            "第4問 - 二重の暗号",
            4
        )

        # パズルエリアにDualDialCipherを配置
        dual_dial = DualDialCipher(puzzle_frame)  # puzzle_frameをparentとして渡す

        # 情報エリア
        description = """二重暗号システムが起動しました。
        
        解読のヒント:
        - 赤のダイヤル(A-D)と青のダイヤル(W-Z)は、それぞれ4文字の英単語を表しています
        - 2つのダイヤルを組み合わせると8文字の単語になります
        - 目標：「子供たち」を意味する8文字の英単語を見つけ出せ！
        """

        self.create_puzzle_info(info_frame, 4, description)
        return frame
        # アニメーション効果を適用
        self.animation_manager.fade_in(frame)

    def _create_dial_display(self, parent):
        """二重ダイヤルの表示エリアを作成"""
        display_frame = ttk.Frame(parent, style='Device.TFrame')
        display_frame.pack(pady=10, padx=20, fill='x')

        # 赤のダイヤル
        red_frame = ttk.LabelFrame(display_frame,
                                text="赤のダイヤル",
                                style='Device.TLabelframe')
        red_frame.pack(side='left', expand=True, padx=10)

        self.red_display = ttk.Label(red_frame,
                                    text="未選択",
                                    font=('DS-Digital', 36),
                                    foreground='#FF0000')
        self.red_display.pack(pady=10)

        red_buttons = ttk.Frame(red_frame)
        red_buttons.pack(pady=5)

        for option in ['A', 'B', 'C', 'D']:
            btn = ttk.Button(red_buttons,
                            text=option,
                            style='Control.TButton',
                            command=lambda opt=option: self._select_dial('red', opt))
            btn.pack(side='left', padx=2)

        # 青のダイヤル（同様の構造）
        blue_frame = ttk.LabelFrame(display_frame,
                                text="青のダイヤル",
                                style='Device.TLabelframe')
        blue_frame.pack(side='right', expand=True, padx=10)
        
        self.blue_display = ttk.Label(blue_frame,
                                    text="未選択",
                                    font=('DS-Digital', 36),
                                    foreground='#0000FF')
        self.blue_display.pack(pady=10)

        blue_buttons = ttk.Frame(blue_frame)
        blue_buttons.pack(pady=5)

        for option in ['W', 'X', 'Y', 'Z']:
            btn = ttk.Button(blue_buttons,
                            text=option,
                            style='Control.TButton',
                            command=lambda opt=option: self._select_dial('blue', opt))
            btn.pack(side='left', padx=2)
    def _create_dial_section(self, parent, title, color):
        """個別のダイヤルセクションを作成"""
        dial_frame = ttk.LabelFrame(parent, text=title)
        dial_frame.pack(side='left', expand=True, padx=10)

        # ダイヤル表示
        display = ttk.Label(dial_frame,
                            text="未選択",
                            font=('DS-Digital', 32),
                            foreground='#ff0000' if color == 'red' else '#0000ff')
        display.pack(pady=10)

        # ボタン作成
        button_frame = ttk.Frame(dial_frame)
        button_frame.pack(pady=5)

        options = ['A', 'B', 'C', 'D'] if color == 'red' else ['W', 'X', 'Y', 'Z']
        for option in options:
            ttk.Button(button_frame,
                    text=option,
                    width=3,
                    command=lambda opt=option, col=color: self._update_dial_display(opt, col, display)).pack(side='left', padx=2)

    def _update_dial_display(self, option, color, display):
        """ダイヤルの選択と表示を更新"""
        if color == 'red':
            selected_numbers = self.dual_cipher.select_red_dial(option)
        else:
            selected_numbers = self.dual_cipher.select_blue_dial(option)

        # ダイヤルの数字と現在の組み合わせを更新
        display.configure(text=' '.join(selected_numbers))
        combined_word = self.dual_cipher.get_combined_word()

        # 組み合わせが正しい場合の処理
        if self.dual_cipher.is_correct_combination():
            self.show_success_message()
            self.next_slide()

    def create_puzzle_five(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        title_frame = ttk.Frame(frame)
        title_frame.pack(pady=20, fill='x')
        
        self.create_decoration_line(title_frame)
        title = ttk.Label(title_frame, 
                         text="第5問 - 究極の暗号機",
                         font=('Helvetica', 24, 'bold'))
        title.pack(pady=10)
        self.create_decoration_line(title_frame)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill='both', expand=True, padx=20)

        device_frame = ttk.LabelFrame(content_frame, text="MULTI-MODE CIPHER SYSTEM")
        device_frame.pack(side='left', fill='both', expand=True, padx=10)

        display_frame = ttk.LabelFrame(device_frame, text="MAIN DISPLAY")
        display_frame.pack(pady=10, padx=20, fill='x')

        word_frame1 = ttk.Frame(display_frame)
        word_frame1.pack(fill='x', pady=5)
        ttk.Label(word_frame1,
                 text="WORD-1:",
                 font=('Courier', 12)).pack(side='left', padx=5)
        ttk.Label(word_frame1,
                 text="02 18 09 03 11",
                 font=('DS-Digital', 24),
                 foreground='#00ff00').pack(side='left', padx=5)

        word_frame2 = ttk.Frame(display_frame)
        word_frame2.pack(fill='x', pady=5)
        ttk.Label(word_frame2,
                 text="WORD-2:",
                 font=('Courier', 12)).pack(side='left', padx=5)
        ttk.Label(word_frame2,
                 text="08 15 21 19 05",
                 font=('DS-Digital', 24),
                 foreground='#00ff00').pack(side='left', padx=5)

        mode_frame = ttk.LabelFrame(device_frame, text="MODE SELECT")
        mode_frame.pack(pady=10, padx=20, fill='x')

        modes = [
            ("MODE-α", "STANDARD", "#00ff00"),
            ("MODE-β", "SPECIAL", "#ff0000"),
            ("MODE-γ", "SPACE", "#0000ff")
        ]

        for mode, label, color in modes:
            mode_panel = ttk.Frame(mode_frame)
            mode_panel.pack(side='left', expand=True, padx=5, pady=5)
            ttk.Label(mode_panel,
                     text=mode,
                     font=('Courier', 10)).pack()
            ttk.Label(mode_panel,
                     text="●",
                     foreground=color).pack()
            ttk.Label(mode_panel,
                     text=label,
                     font=('Courier', 8)).pack()

        info_frame = ttk.LabelFrame(content_frame, text="Mission Information")
        info_frame.pack(side='right', fill='both', expand=True, padx=10)

        description = """
        最終暗号装置が起動しました。
        この装置は3つのモードを組み合わせた
        最も高度な暗号化システムです。

        解読のヒント:
        - MODE-α: 通常の文字を処理
        - MODE-β: 特殊文字を処理
        - MODE-γ: スペースを処理
        - 2つの単語を組み合わせたフレーズになります
        """

        ttk.Label(info_frame,
                 text=description,
                 wraplength=300,
                 justify='left',
                 font=('Helvetica', 12)).pack(pady=20, padx=20)

        input_frame = ttk.LabelFrame(info_frame, text="Final Answer")
        input_frame.pack(fill='x', padx=20, pady=20)

        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(input_frame,
                               textvariable=self.answer_var,
                               font=('Courier', 14))
        answer_entry.pack(pady=10, padx=10, fill='x')

        check_button = ttk.Button(input_frame,
                                text="DECODE FINAL CIPHER",
                                command=self.check_final_answer)
        check_button.pack(pady=10)

        answer_entry.bind('<Return>', lambda e: self.check_final_answer())

    def create_birthday(self, parent):
        """お誕生日メッセージスライド"""
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        # メインコンテンツを中央に配置するためのフレーム
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # メッセージ要素のリスト
        messages = []
        
        # タイトル
        title = ttk.Label(content_frame,
                        text="認証完了 - FINAL MESSAGE",
                        font=('Helvetica', 24, 'bold'),
                        foreground='#00ff00')
        messages.append((title, 0))
        
        # デコレーション
        decoration_top = ttk.Label(content_frame,
                                text="* * * * * * * * * *",
                                font=('Courier', 24),
                                foreground='#00ff00')
        messages.append((decoration_top, 500))
        
        # 宛名
        recipient = ttk.Label(content_frame,
                            text="Dear なおちゃんへ",
                            font=('Helvetica', 20),
                            foreground='#ffffff')
        messages.append((recipient, 1000))
        
        # メッセージ本文
        message_texts = [
            "お誕生日おめでとう！",
            "一緒にいると幸せで、時間があっという間に過ぎてしまいます。",
            "これからも、たくさんの素敵な思い出を作っていきたいです。",
            "あなたにとって、すてきな一年になりますように。",
            "Happy Birthday!"
        ]
        
        delay = 1500
        for text in message_texts:
            msg = ttk.Label(content_frame,
                        text=text,
                        font=('Helvetica', 16),
                        foreground='#ffffff',
                        wraplength=500)  # 長いメッセージを折り返し
            messages.append((msg, delay))
            delay += 500
        
        # 署名
        signature = ttk.Label(content_frame,
                            text="From もけ",
                            font=('Helvetica', 18),
                            foreground='#00ff00')
        messages.append((signature, delay))
        
        # 下部デコレーション
        decoration_bottom = ttk.Label(content_frame,
                                    text="* * * * * * * * * *",
                                    font=('Courier', 24),
                                    foreground='#00ff00')
        messages.append((decoration_bottom, delay + 500))
        
        # アニメーション処理
        def show_messages(index=0):
            if index < len(messages):
                label, delay = messages[index]
                label.pack(pady=10)
                self.play_sound('click')
                self.root.after(delay, lambda: show_messages(index + 1))
        
        # アニメーション開始
        show_messages()
        
        return frame
    def start_birthday_animation(self):
        def show_element(index):
            if index < len(self.birthday_elements):
                element, delay = self.birthday_elements[index]
                element.pack(pady=10)
                self.play_sound('click')
                self.root.after(delay, lambda: show_element(index + 1))
                show_element(0)
