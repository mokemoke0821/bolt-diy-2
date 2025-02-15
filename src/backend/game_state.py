import logging
import json
import time
from typing import Dict, Set, Optional

class GameState:
    def __init__(self, root, animation_manager):
    #既存の初期化コード
        self.hint_levels = {num: 0 for num in range(1, 6)}  # 各問題のヒントレベル
        self.root = root
        self.animation_manager = animation_manager
        self.score = 0
        self.hints_remaining = 3
        self.start_time = time.time()
        self.solved_puzzles = set()
        
        # パズルの依存関係を定義
        self.puzzle_dependencies = {
            1: set(),  # 第1問は依存なし
            2: {1},    # 第2問は第1問クリアが必要
            3: {1, 2}, # 第3問は第1,2問クリアが必要
            4: {3},    # 第4問は第3問クリアが必要
            5: {4}     # 第5問は第4問クリアが必要
        }
        
        self.load_state()
    
    def can_access_puzzle(self, puzzle_number: int) -> bool:
        """パズルにアクセス可能か確認"""
        if puzzle_number not in self.puzzle_dependencies:
            return False
        return self.puzzle_dependencies[puzzle_number].issubset(self.solved_puzzles)
    
    def mark_puzzle_solved(self, puzzle_number: int) -> None:
        """パズルを解決済みとしてマーク"""
        self.solved_puzzles.add(puzzle_number)
        self.save_state()
    
    def use_hint(self, puzzle_number: int) -> Optional[str]:
        """ヒントを使用"""
        if not self.can_access_puzzle(puzzle_number):
            return None
            
        if self.hints_remaining > 0:
            self.hints_remaining -= 1
            self.save_state()
            return self.get_hint_text(puzzle_number)
        return None
    
    def get_hint_text(self, puzzle_number: int) -> str:
        """ヒントテキストを取得"""
        hints = {
            1: ["数字は1つのアルファベットに対応しています",
                "流れるものを考えてみましょう"],
            2: ["パターンには規則性があります",
                "生活に欠かせないものです"],
            3: ["円環の外側と内側は関連があります",
                "緑が多い場所です"],
            4: ["2つのダイヤルの組み合わせを考えてください",
                "若い存在です"],
            5: ["2つの単語で構成されています",
                "建物に関係します"]
        }
        
        puzzle_hints = hints.get(puzzle_number, [])
        used_hints = len(puzzle_hints) - self.hints_remaining
        return puzzle_hints[min(used_hints, len(puzzle_hints) - 1)]
    # game_state.py に追加
    def get_hints_remaining(self) -> int:
        """残りのヒント回数を取得"""
        return self.hints_remaining
    def save_state(self) -> None:
        """状態を保存"""
        state = {
            'score': self.score,
            'hints_remaining': self.hints_remaining,
            'solved_puzzles': list(self.solved_puzzles),
            'start_time': self.start_time
        }
        
        try:
            with open('game_state.json', 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logging.error(f"状態の保存に失敗: {str(e)}")
    
    def load_state(self) -> None:
        """状態を読み込み"""
        try:
            with open('game_state.json', 'r') as f:
                state = json.load(f)
                self.score = state.get('score', 0)
                self.hints_remaining = state.get('hints_remaining', 3)
                self.solved_puzzles = set(state.get('solved_puzzles', []))
                self.start_time = state.get('start_time', time.time())
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"状態の読み込みに失敗: {str(e)}")
            
    def setup_score_display(self, score_label) -> None:
        """スコア表示の設定"""
        self.score_label = score_label
        self.update_score_display()

    # game_state.py のメソッドを追加

    def get_score(self) -> int:
        """現在のスコアを取得"""
        return self.score

    def get_high_score(self) -> int:
        """ハイスコアを取得"""
        try:
            with open('game_state.json', 'r') as f:
                state = json.load(f)
                return state.get('high_score', 0)
        except:
            return 0
        
    def update_score_display(self) -> None:
        """スコア表示の更新"""
        if hasattr(self, 'score_label') and self.score_label:
            self.score_label.configure(text=f"スコア: {self.score}")
            
    def update_score(self, points: int) -> None:
        """スコアの更新"""
        self.score += points
        self.update_score_display()