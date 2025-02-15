import tkinter as tk
from tkinter import ttk
import logging

class AnimationManager:
    def __init__(self, root):
        self.root = root
        self.animation_speed = 'normal'
        self.animation_durations = {
            'fast': 200,
            'normal': 400,
            'slow': 800
        }

    def fade_in(self, widget, duration=None):
        """フェードインアニメーション（Canvas対応版）"""
        duration = duration or self.animation_durations[self.animation_speed]
        steps = 20
        step_time = duration // steps

        # キャンバスにオーバーレイ
        overlay = tk.Canvas(widget, bg="black", highlightthickness=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        widget.update_idletasks()

        for step in range(steps):
            opacity = 1 - (step + 1) / steps
            overlay.configure(bg=f"#{int(255 * opacity):02x}{int(255 * opacity):02x}{int(255 * opacity):02x}")
            self.root.update_idletasks()
            self.root.after(step_time)

        overlay.destroy()

    def fade_out(self, widget, duration=None):
        """フェードアウトアニメーション（Canvas対応版）"""
        duration = duration or self.animation_durations[self.animation_speed]
        steps = 20
        step_time = duration // steps

        # キャンバスにオーバーレイ
        overlay = tk.Canvas(widget, bg="black", highlightthickness=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        widget.update_idletasks()

        for step in range(steps):
            opacity = (step + 1) / steps
            overlay.configure(bg=f"#{int(255 * opacity):02x}{int(255 * opacity):02x}{int(255 * opacity):02x}")
            self.root.update_idletasks()
            self.root.after(step_time)

        overlay.destroy()


    def slide_transition(self, old_frame, new_frame, direction='right', duration=None):
        """スライド遷移アニメーション"""
        duration = duration or self.animation_durations[self.animation_speed]
        steps = 20
        step_time = duration // steps
        window_width = self.root.winfo_width()
        start_x = window_width if direction == 'right' else -window_width

        new_frame.pack(fill='both', expand=True)
        for step in range(steps):
            progress = step / steps
            old_x = int(-start_x * progress)
            new_x = int(start_x * (1 - progress))
            old_frame.place(x=old_x, y=0, relwidth=1, relheight=1)
            new_frame.place(x=new_x, y=0, relwidth=1, relheight=1)
            self.root.update_idletasks()
            self.root.after(step_time)

        old_frame.destroy()

    def set_animation_speed(self, speed: str):
        """アニメーション速度の設定"""
        if speed in self.animation_durations:
            self.animation_speed = speed
            logging.info(f"アニメーション速度を{speed}に設定しました")

    def disable_animations(self):
        """アニメーションの無効化"""
        self.animation_speed = 'fast'
        self.animation_durations['fast'] = 1
        logging.info("アニメーションを無効化しました")

    def enable_animations(self):
        """アニメーションの有効化"""
        self.animation_speed = 'normal'
        self.animation_durations = {
            'fast': 200,
            'normal': 400,
            'slow': 800
        }
        logging.info("アニメーションを有効化しました")

    def cleanup(self):
        """アニメーションマネージャーのクリーンアップ"""
        try:
            self.running_animations.clear()
            for after_id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(after_id)
            logging.info("アニメーションマネージャーのクリーンアップが完了しました")
        except Exception as e:
            logging.error(f"アニメーションマネージャーのクリーンアップに失敗: {str(e)}")
