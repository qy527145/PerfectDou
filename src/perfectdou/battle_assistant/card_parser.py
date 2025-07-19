"""
牌型解析模块

支持多种输入格式的牌型解析和标准化转换。
"""

import re
from typing import List, Dict, Union, Optional


class CardParser:
    """牌型解析器，支持多种输入格式"""
    
    # 牌面映射表
    CARD_MAPPINGS = {
        # 标准英文表示
        '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 17,
        
        # 中文数字
        '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        
        # 王牌的多种表示
        'joker': 20, '小王': 20, '小': 20, 'B': 20, 'b': 20,
        'JOKER': 30, '大王': 30, '大': 30, 'R': 30, 'r': 30,
        
        # 其他常见表示
        'j': 11, 'q': 12, 'k': 13, 'a': 14,
        'T': 10, 't': 10,  # 10的另一种表示
    }
    
    # 反向映射：从数值到标准表示
    VALUE_TO_DISPLAY = {
        3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: 'J', 12: 'Q', 13: 'K', 14: 'A', 17: '2', 20: '小王', 30: '大王'
    }
    
    # 用于PerfectDou环境的映射
    ENV_CARD_MAPPING = {
        3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
        11: 11, 12: 12, 13: 13, 14: 14, 17: 17, 20: 20, 30: 30
    }
    
    def __init__(self):
        """初始化牌型解析器"""
        pass
    
    def parse_cards(self, card_input: str) -> List[int]:
        """
        解析牌型字符串，返回标准化的牌值列表
        
        Args:
            card_input: 输入的牌型字符串
            
        Returns:
            标准化的牌值列表，按从小到大排序
            
        Examples:
            >>> parser = CardParser()
            >>> parser.parse_cards("3 4 5 J Q K A")
            [3, 4, 5, 11, 12, 13, 14]
            >>> parser.parse_cards("三四五 J Q K A 小王 大王")
            [3, 4, 5, 11, 12, 13, 14, 20, 30]
        """
        if not card_input or not card_input.strip():
            return []
        
        # 预处理：统一空格分隔
        card_input = self._preprocess_input(card_input)
        
        # 分割并解析每张牌
        cards = []
        tokens = card_input.split()
        
        for token in tokens:
            if not token:
                continue
                
            card_value = self._parse_single_card(token)
            if card_value is not None:
                cards.append(card_value)
            else:
                raise ValueError(f"无法识别的牌型: {token}")
        
        # 排序并返回
        return sorted(cards)
    
    def _preprocess_input(self, card_input: str) -> str:
        """预处理输入字符串"""
        # 移除多余的空白字符
        card_input = re.sub(r'\s+', ' ', card_input.strip())

        # 处理王牌的特殊情况（优先处理）
        card_input = re.sub(r'(小王|大王)', r' \1 ', card_input)
        card_input = re.sub(r'(?<!\S)(小|大)(?!\S)', r' \1 ', card_input)

        # 处理连续的数字和字母（如：345JQK -> 3 4 5 J Q K）
        # 使用更精确的正则表达式来分隔字符
        # 在每个字符之间插入空格
        result = ""
        i = 0
        while i < len(card_input):
            if i > 0 and card_input[i-1] != ' ' and card_input[i] != ' ':
                # 检查是否需要在字符间插入空格
                prev_char = card_input[i-1]
                curr_char = card_input[i]

                # 如果前一个字符是数字，当前字符也是数字或字母，则插入空格
                if (prev_char.isdigit() and (curr_char.isdigit() or curr_char.isalpha())) or \
                   (prev_char.isalpha() and (curr_char.isdigit() or curr_char.isalpha())):
                    result += ' '

            result += card_input[i]
            i += 1

        card_input = result

        # 处理中文字符之间的分隔
        card_input = re.sub(r'([三四五六七八九十])([三四五六七八九十])', r'\1 \2', card_input)

        # 清理多余空格
        card_input = re.sub(r'\s+', ' ', card_input.strip())

        return card_input
    
    def _parse_single_card(self, token: str) -> Optional[int]:
        """解析单张牌"""
        token = token.strip()
        
        # 直接查找映射表
        if token in self.CARD_MAPPINGS:
            return self.CARD_MAPPINGS[token]
        
        # 处理数字
        if token.isdigit():
            num = int(token)
            if 3 <= num <= 10:
                return num
            elif num == 2:
                return 17
        
        return None
    
    def cards_to_display(self, cards: List[int]) -> str:
        """将牌值列表转换为显示字符串"""
        if not cards:
            return "无牌"
        
        display_cards = []
        for card in sorted(cards):
            if card in self.VALUE_TO_DISPLAY:
                display_cards.append(self.VALUE_TO_DISPLAY[card])
            else:
                display_cards.append(str(card))
        
        return " ".join(display_cards)
    
    def cards_to_env_format(self, cards: List[int]) -> List[int]:
        """将牌值列表转换为环境格式"""
        return [self.ENV_CARD_MAPPING.get(card, card) for card in cards]
    
    def validate_cards(self, cards: List[int]) -> bool:
        """验证牌型是否合法（不超过标准牌数）"""
        # 统计每种牌的数量
        card_count = {}
        for card in cards:
            card_count[card] = card_count.get(card, 0) + 1
        
        # 检查数量限制
        for card, count in card_count.items():
            if card in [20, 30]:  # 王牌只能有1张
                if count > 1:
                    return False
            else:  # 其他牌最多4张
                if count > 4:
                    return False
        
        return True
    
    def get_card_type_info(self, cards: List[int]) -> Dict[str, Union[str, int]]:
        """获取牌型信息"""
        if not cards:
            return {"type": "空", "count": 0, "description": "没有出牌"}
        
        sorted_cards = sorted(cards)
        count = len(cards)
        
        # 基本牌型判断
        if count == 1:
            return {"type": "单牌", "count": 1, "description": f"单张 {self.cards_to_display(cards)}"}
        elif count == 2:
            if sorted_cards[0] == sorted_cards[1]:
                return {"type": "对子", "count": 2, "description": f"一对 {self.cards_to_display([sorted_cards[0]])}"}
            elif sorted_cards == [20, 30]:
                return {"type": "王炸", "count": 2, "description": "火箭（双王）"}
            else:
                return {"type": "无效", "count": 2, "description": "无效的两张牌"}
        elif count == 3:
            if sorted_cards[0] == sorted_cards[1] == sorted_cards[2]:
                return {"type": "三张", "count": 3, "description": f"三张 {self.cards_to_display([sorted_cards[0]])}"}
        elif count == 4:
            if sorted_cards[0] == sorted_cards[1] == sorted_cards[2] == sorted_cards[3]:
                return {"type": "炸弹", "count": 4, "description": f"炸弹 {self.cards_to_display([sorted_cards[0]])}"}
        
        # 更复杂的牌型需要进一步分析
        return {"type": "复合", "count": count, "description": f"{count}张牌的组合"}
