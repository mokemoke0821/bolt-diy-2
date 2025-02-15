# puzzle_manager.py
import logging
from typing import Dict, Set, Optional

class PuzzleManager:
    def __init__(self, game_state, resource_manager):
        """パズルマネージャーの初期化"""
        self.game_state = game_state
        self.resource_manager = resource_manager
        self.answers = {
            1: "river",    # 最古の暗号装置の解答
            2: "bread",    # パターン解析装置の解答
            3: "forest",   # 円環暗号装置の解答
            4: "children", # 二重暗号装置の解答
            5: "brick house" # 最終暗号装置の解答
        }
        
        # 各パズルの説明文
        self.puzzle_descriptions = {
            1: """最古の暗号装置が起動しました。
            この装置は、文字を2桁の数字に変換する
            シンプルな機構を持っています。
            
            解読のヒント:
            - 2桁の数字は1つのアルファベットに対応
            - 変換表を参考に規則性を見つけ出せ
            - 意味のある英単語になるはず""",
            
            2: """パターン解析装置が起動しました。
            入力された数値が特定のパターンで変換されています。
            
            解読のヒント:
            - 変換パターンを解析せよ
            - 各数字は文字に対応
            - 日常生活で見かけるものを表す単語""",
            
            3: """円環暗号装置が起動しました。
            この装置は文字を円環状に配置し、
            回転させることで暗号化を行います。
            
            解読のヒント:
            - 外側の環は数字を表示
            - 内側の環は文字を表示
            - 環を回転させることで対応が変化""",
            
            4: """二重暗号システムが起動しました。
            この装置は2つのダイヤルで異なる文字グループを
            暗号化しています。
            
            解読のヒント:
            - 赤のダイヤル: 前半4文字を担当
            - 青のダイヤル: 後半4文字を担当
            - 各ダイヤルは特定の文字グループのみ使用""",
            
            5: """最終暗号装置が起動しました。
            この装置は3つのモードを組み合わせた
            最も高度な暗号化システムです。
            
            解読のヒント:
            - 2つの単語で構成される
            - 建物に関する表現
            - モードの組み合わせを考えよ"""
        }

    def check_answer(self, puzzle_number: int, answer: str) -> bool:
        """解答をチェックし、正誤を判定する"""
        try:
            if puzzle_number not in self.answers:
                logging.warning(f"未定義のパズル番号: {puzzle_number}")
                return False
                
            is_correct = answer.lower().strip() == self.answers[puzzle_number]
            
            if is_correct:
                self.resource_manager.play_sound('success')
                self.game_state.update_score(100)  # 基本点
                # ヒントを使っていない場合のボーナス
                if self.game_state.hint_levels[puzzle_number] == 0:
                    self.game_state.update_score(50)  # ボーナス点
            else:
                self.resource_manager.play_sound('error')
                self.game_state.update_score(-10)  # ペナルティ
                
            return is_correct
            
        except Exception as e:
            logging.error(f"解答チェック時にエラーが発生: {str(e)}")
            return False

    def get_puzzle_description(self, puzzle_number: int) -> str:
        """パズルの説明文を取得"""
        return self.puzzle_descriptions.get(puzzle_number, "")

    def calculate_progress(self) -> float:
        """全体の進捗率を計算（0.0 ~ 1.0）"""
        total_puzzles = len(self.answers)
        solved_count = sum(1 for puzzle_num in self.answers 
                         if puzzle_num in self.game_state.solved_puzzles)
        return solved_count / total_puzzles

    def is_all_completed(self) -> bool:
        """全てのパズルが解かれているかチェック"""
        return len(self.game_state.solved_puzzles) == len(self.answers)

    def get_remaining_puzzles(self) -> Set[int]:
        """未解決のパズル番号を取得"""
        return set(self.answers.keys()) - self.game_state.solved_puzzles
