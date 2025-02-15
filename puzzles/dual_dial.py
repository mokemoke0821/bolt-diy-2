import tkinter as tk
from tkinter import ttk
import logging

class DualDialCipher:
    def __init__(self, parent):
        self.parent = parent
        self.displays = {}
        self.selected_red = None
        self.selected_blue = None
        
        # 選択肢の定義
        self.red_options = {
            'A': 'chil',
            'B': 'kids',
            'C': 'play',
            'D': 'chil'
        }
        self.blue_options = {
            'W': 'dren',
            'X': 'ding',
            'Y': 'time',
            'Z': 'dren'
        }
        
        self._setup_styles()
        self._create_dial_interface(parent)

    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        style.configure('Dial.TButton',
                       padding=5,
                       width=10)
        style.configure('DialDisplay.TLabel',
                       font=('Helvetica', 24),
                       background='#1a1a1a',
                       padding=10)
        style.configure('DialFrame.TLabelframe',
                       background='#1a1a1a',
                       padding=10)

    def _create_dial_interface(self, parent):
        """ダイヤルインターフェースの作成"""
        frame = ttk.Frame(parent)
        frame.pack(pady=20)
        
        # 赤のダイヤル
        self._create_dial_section(frame, "赤のダイヤル",
                                ['A', 'B', 'C', 'D'],
                                'red', True)
        
        # 青のダイヤル
        self._create_dial_section(frame, "青のダイヤル",
                                ['W', 'X', 'Y', 'Z'],
                                'blue', False)

    def _create_dial_section(self, parent, title, options, color, is_left):
        """ダイヤルセクションの作成"""
        frame = ttk.LabelFrame(parent, text=title, style='DialFrame.TLabelframe')
        frame.pack(side='left' if is_left else 'right', padx=20)
        
        self.displays[color] = ttk.Label(frame,
                                       text="未選択",
                                       style='DialDisplay.TLabel',
                                       foreground='#FF0000' if color == 'red' else '#0000FF')
        self.displays[color].pack(pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        for opt in options:
            ttk.Button(button_frame,
                      text=opt,
                      style='Dial.TButton',
                      command=lambda x=opt: self._update_dial(color, x)).pack(pady=2)

    def _update_dial(self, dial_type, option):
        """ダイヤルの更新"""
        try:
            if dial_type == 'red':
                self.selected_red = option
                word = self.red_options.get(option, '')
            else:
                self.selected_blue = option
                word = self.blue_options.get(option, '')
                
            self.displays[dial_type].configure(text=word)
            
            if self.is_correct_combination():
                self._show_success()
                
        except Exception as e:
            logging.error(f"ダイヤル更新エラー: {str(e)}")

    def is_correct_combination(self):
        """正解の組み合わせかチェック"""
        return (self.selected_red == 'D' and 
                self.selected_blue == 'Z')

    def get_combined_word(self):
        """組み合わせた単語を取得"""
        red_word = self.red_options.get(self.selected_red, '')
        blue_word = self.blue_options.get(self.selected_blue, '')
        return red_word + blue_word

    def _show_success(self):
        """正解時の処理"""
        success_label = ttk.Label(self.parent,
                                text="正解！",
                                style='DialDisplay.TLabel',
                                foreground='#00FF00')
        success_label.pack(pady=20)
        self.parent.after(2000, success_label.destroy)