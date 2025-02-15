# theme_manager.py
import tkinter.ttk as ttk

class ThemeManager:
    def __init__(self):
        self.themes = {
            'dark': {
                'background': '#1a1a1a',
                'foreground': '#00ff00',
                'accent': '#4a4a4a',
                'text': '#ffffff',
                'error': '#ff0000',
                'success': '#00ff00',
                'button': '#2a2a2a',
                'button_hover': '#3a3a3a',
                'border': '#333333'
            },
            'cyber': {
                'background': '#001122',
                'foreground': '#00ffff',
                'text': '#00ffff',
                'error': '#ff3366',
                'success': '#33ff99',
                'accent': '#003366',
                'button': '#002244',
                'button_hover': '#003366',
                'border': '#004488'
            }
        }
        self.current_theme = 'dark'
        self.style = ttk.Style()

    def apply_theme(self, theme_name):
        """テーマを適用"""
        if theme_name not in self.themes:
            return False
            
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        style = ttk.Style()
        
        # フレームスタイル
        style.configure('Device.TFrame',
                    background=theme['background'],
                    borderwidth=2,
                    relief='solid')
        
        # ラベルスタイル                
        style.configure('Title.TLabel',
                    font=('Helvetica', 28, 'bold'),
                    foreground=theme['foreground'],
                    background=theme['background'])
        
        style.configure('Device.TLabel',
                    font=('Courier', 40),
                    foreground=theme['foreground'],
                    background=theme['background'])
        
        style.configure('Hint.TLabel',
                    font=('Helvetica', 12),
                    foreground=theme['text'],
                    background=theme['background'])
        
        # ボタンスタイル
        style.configure('Control.TButton',
                    font=('Helvetica', 12),
                    background=theme['button'],
                    padding=10)
                    
        style.map('Control.TButton',
                background=[('active', theme['button_hover'])])
        
        return True
    def get_current_theme_colors(self):
        """現在のテーマの色を取得"""
        return self.themes[self.current_theme]