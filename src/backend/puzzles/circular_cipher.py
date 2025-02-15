import math
import logging
import tkinter as tk
from tkinter import ttk

class CircularCipherPuzzle:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.current_angle = 0
        self.is_rotating = False
        self.numbers = list(range(1, 7))
        self.letters = ['f', 'o', 'r', 'e', 's', 't']
        
        # キャンバスの初期設定
        self.canvas.configure(bg='#1a1a1a')
        
        # 回転ボタンの追加
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(pady=10)
        
        ttk.Button(self.control_frame, 
                  text="時計回りに回転",
                  command=lambda: self.rotate(60)).pack(side='left', padx=5)
        
        ttk.Button(self.control_frame,
                  text="反時計回りに回転",
                  command=lambda: self.rotate(-60)).pack(side='left', padx=5)
        
        # 角度表示
        self.angle_label = ttk.Label(self.control_frame, text="0°")
        self.angle_label.pack(side='left', padx=20)
        
        # 初期描画
        self.canvas.bind('<Configure>', self._on_resize)
        self.draw_mechanism()

    def _on_resize(self, event):
        """キャンバスのリサイズ時の処理"""
        self.draw_mechanism()

    def draw_mechanism(self):
        """円環メカニズムの描画"""
        try:
            self.canvas.delete('all')
            
            # キャンバスサイズ取得と設定
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.configure(width=width, height=height, bg='#1a1a1a')
            
            center_x = width // 2
            center_y = height // 2
            
            # 円のサイズ計算
            size = min(width, height) - 60
            outer_radius = size // 2
            inner_radius = outer_radius - 50
            
            # 描画
            self._draw_circles(center_x, center_y, outer_radius, inner_radius)
            self._place_items(self.numbers, outer_radius - 25, '#00FFFF', center_x, center_y, 0)
            self._place_items(self.letters, inner_radius - 25, '#00FF00', center_x, center_y, self.current_angle)
            
        except Exception as e:
            logging.error(f"円環メカニズムの描画エラー: {str(e)}")

    def _draw_circles(self, cx, cy, outer_r, inner_r):
        """円を描画"""
        self.canvas.create_oval(
            cx - outer_r, cy - outer_r,
            cx + outer_r, cy + outer_r,
            outline='#00FFFF', width=2
        )
        self.canvas.create_oval(
            cx - inner_r, cy - inner_r,
            cx + inner_r, cy + inner_r,
            outline='#00FF00', width=2
        )
    def _place_items(self, items, radius, color, center_x, center_y, angle_offset):
        """アイテムを円周上に配置"""
        for i, item in enumerate(items):
            angle = math.radians(i * 60 + angle_offset)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.canvas.create_text(
                x, y, text=str(item),
                font=('Helvetica', 18, 'bold'),
                fill=color
            )

    def rotate(self, degrees):
        """指定角度の回転処理"""
        if not self.is_rotating:
            self.is_rotating = True
            self._animate_rotation(degrees, 0)

    def _animate_rotation(self, target_degrees, current_step):
        """回転アニメーション"""
        steps = 10
        if current_step < steps:
            step_angle = target_degrees / steps
            self.current_angle = (self.current_angle + step_angle) % 360
            self.angle_label.configure(text=f"{int(self.current_angle)}°")
            self.draw_mechanism()
            self.root.after(50, lambda: self._animate_rotation(target_degrees, current_step + 1))
        else:
            self.is_rotating = False

    def get_current_mapping(self):
        """現在の文字と数字の対応を取得"""
        offset = int(self.current_angle / 60)
        mapping = {}
        for i in range(len(self.numbers)):
            letter_idx = (i - offset) % len(self.letters)
            mapping[self.numbers[i]] = self.letters[letter_idx]
        return mapping

    def get_current_word(self):
        """現在の配置から単語を取得"""
        mapping = self.get_current_mapping()
        number_sequence = [4, 3, 5, 1, 1, 4]
        return ''.join(mapping[num] for num in number_sequence)