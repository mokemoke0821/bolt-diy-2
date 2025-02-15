class FinalCipher:
    """最終暗号システムの実装
    
    このクラスは2つの暗号化された単語を組み合わせて
    最終的なフレーズを生成する機能を提供します。
    """
    
    def __init__(self):
        """最終暗号システムの初期化"""
        # 数字→文字の変換テーブル
        self.conversion_table = {
            '02': 'b', '18': 'r', '09': 'i', '03': 'c', '11': 'k',
            '08': 'h', '15': 'o', '21': 'u', '19': 's', '05': 'e'
        }
        
        # 暗号化された単語の数字列
        self.word1_numbers = "02 18 09 03 11"  # brick
        self.word2_numbers = "08 15 21 19 05"  # house
        
        # 動作モード
        self.modes = {
            'alpha': 'STANDARD',   # 通常の文字変換
            'beta': 'SPECIAL',     # 特殊文字変換
            'gamma': 'SPACE'       # スペース処理
        }

    def decode_word(self, numbers_str: str) -> str:
        """数字列を単語にデコード
        
        Args:
            numbers_str: スペース区切りの数字列
            
        Returns:
            str: デコードされた単語
        """
        result = ''
        numbers = numbers_str.split()
        for num in numbers:
            if num in self.conversion_table:
                result += self.conversion_table[num]
        return result

    def get_complete_phrase(self) -> str:
        """完全なフレーズを取得
        
        Returns:
            str: デコードされた完全なフレーズ
        """
        word1 = self.decode_word(self.word1_numbers)
        word2 = self.decode_word(self.word2_numbers)
        return f"{word1} {word2}"
        
    def get_current_mode_description(self, mode: str) -> str:
        """指定されたモードの説明を取得
        
        Args:
            mode: モード名（'alpha', 'beta', 'gamma'）
            
        Returns:
            str: モードの説明文
        """
        descriptions = {
            'alpha': '通常の文字を処理します',
            'beta': '特殊文字を処理します',
            'gamma': 'スペースを処理します'
        }
        return descriptions.get(mode, '不明なモード')