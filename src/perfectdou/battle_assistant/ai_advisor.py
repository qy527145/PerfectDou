"""
AI决策顾问模块

集成PerfectDou智能体，为用户提供出牌建议和策略分析。
"""

import os
import sys
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .game_state import GameState, Position, MoveRecord
from .card_parser import CardParser


@dataclass
class MoveAdvice:
    """出牌建议"""
    cards: List[int]
    description: str
    confidence: float  # 置信度 0-1
    move_type: str
    reasoning: str     # 推理说明


class MockInfoSet:
    """模拟信息集，用于适配PerfectDou智能体接口"""
    
    def __init__(self, position: str, hand_cards: List[int], 
                 last_move: List[int], last_two_moves: List[List[int]],
                 legal_actions: List[List[int]], last_pid: str = ""):
        self.player_position = position
        self.player_hand_cards = hand_cards
        self.last_move = last_move
        self.last_two_moves = last_two_moves
        self.legal_actions = legal_actions
        self.last_pid = last_pid


class AIAdvisor:
    """AI决策顾问"""
    
    def __init__(self):
        """初始化AI顾问"""
        self.card_parser = CardParser()
        self._perfectdou_agent = None
        self._rlcard_agent = None
        self._agents_loaded = False
    
    def _load_agents(self):
        """延迟加载AI智能体"""
        if self._agents_loaded:
            return
        
        try:
            # 尝试加载PerfectDou智能体
            from perfectdou.evaluation.perfectdou_agent import PerfectDouAgent
            self._perfectdou_agent = {
                'landlord': PerfectDouAgent('landlord'),
                'landlord_up': PerfectDouAgent('landlord_up'),
                'landlord_down': PerfectDouAgent('landlord_down')
            }
        except Exception as e:
            print(f"警告：无法加载PerfectDou智能体: {e}")
            self._perfectdou_agent = None
        
        try:
            # 加载RLCard智能体作为备选
            from perfectdou.evaluation.rlcard_agent import RLCardAgent
            self._rlcard_agent = {
                'landlord': RLCardAgent('landlord'),
                'landlord_up': RLCardAgent('landlord_up'),
                'landlord_down': RLCardAgent('landlord_down')
            }
        except Exception as e:
            print(f"警告：无法加载RLCard智能体: {e}")
            self._rlcard_agent = None
        
        self._agents_loaded = True
    
    def get_move_advice(self, game_state: GameState, 
                       num_suggestions: int = 3) -> List[MoveAdvice]:
        """
        获取出牌建议
        
        Args:
            game_state: 当前游戏状态
            num_suggestions: 建议数量
            
        Returns:
            出牌建议列表
        """
        self._load_agents()
        
        if not game_state.players[game_state.user_position].is_user:
            return []
        
        # 获取合法出牌上下文
        context = game_state.get_legal_moves_context()
        user_cards = context["user_cards"]
        
        if not user_cards:
            return []
        
        # 生成合法出牌选项
        legal_moves = self._generate_legal_moves(context)
        
        # 获取AI建议
        ai_suggestions = self._get_ai_suggestions(game_state, legal_moves)
        
        # 生成多样化建议
        advice_list = self._generate_diverse_advice(
            legal_moves, ai_suggestions, num_suggestions
        )
        
        return advice_list
    
    def _generate_legal_moves(self, context: Dict) -> List[List[int]]:
        """生成合法出牌选项"""
        user_cards = context["user_cards"]
        legal_moves = []
        
        # 总是可以过牌（如果需要跟牌）
        if context["can_pass"]:
            legal_moves.append([])  # 空列表表示过牌
        
        # 如果不需要跟牌，可以出任意合法牌型
        if not context["need_follow"]:
            legal_moves.extend(self._generate_all_possible_moves(user_cards))
        else:
            # 需要跟牌，生成能够压过上家的牌型
            last_move = context.get("last_valid_move")
            if last_move:
                legal_moves.extend(
                    self._generate_following_moves(user_cards, last_move["cards"])
                )
        
        return legal_moves
    
    def _generate_all_possible_moves(self, cards: List[int]) -> List[List[int]]:
        """生成所有可能的出牌组合"""
        moves = []
        
        # 单牌
        for card in set(cards):
            moves.append([card])
        
        # 对子
        card_counts = {}
        for card in cards:
            card_counts[card] = card_counts.get(card, 0) + 1
        
        for card, count in card_counts.items():
            if count >= 2:
                moves.append([card, card])
            if count >= 3:
                moves.append([card, card, card])
            if count >= 4:
                moves.append([card, card, card, card])
        
        # 王炸
        if 20 in cards and 30 in cards:
            moves.append([20, 30])
        
        # 简化版：只返回基本牌型
        return moves[:20]  # 限制数量避免过多选项
    
    def _generate_following_moves(self, cards: List[int], 
                                last_cards: List[int]) -> List[List[int]]:
        """生成跟牌选项"""
        moves = []
        last_count = len(last_cards)
        
        if last_count == 1:  # 跟单牌
            last_value = last_cards[0]
            for card in cards:
                if card > last_value:
                    moves.append([card])
        elif last_count == 2:  # 跟对子或王炸
            if last_cards == [20, 30]:  # 王炸无法跟
                return moves
            elif last_cards[0] == last_cards[1]:  # 跟对子
                last_value = last_cards[0]
                card_counts = {}
                for card in cards:
                    card_counts[card] = card_counts.get(card, 0) + 1
                for card, count in card_counts.items():
                    if count >= 2 and card > last_value:
                        moves.append([card, card])
        
        # 炸弹可以压任何牌型（除了更大的炸弹）
        card_counts = {}
        for card in cards:
            card_counts[card] = card_counts.get(card, 0) + 1
        
        for card, count in card_counts.items():
            if count >= 4:
                if last_count != 4 or card > last_cards[0]:
                    moves.append([card, card, card, card])
        
        # 王炸可以压任何牌型
        if 20 in cards and 30 in cards and last_cards != [20, 30]:
            moves.append([20, 30])
        
        return moves
    
    def _get_ai_suggestions(self, game_state: GameState, 
                          legal_moves: List[List[int]]) -> List[List[int]]:
        """获取AI智能体的建议"""
        if not legal_moves:
            return []
        
        # 构造信息集
        user_position = game_state.user_position.value
        user_cards = game_state.get_user_hand_cards()
        
        # 获取最近的出牌历史
        last_move = []
        last_two_moves = [[], []]
        last_pid = ""
        
        if game_state.last_move:
            last_move = game_state.last_move.cards
            last_pid = game_state.last_move.position.value
        
        if len(game_state.move_history) >= 2:
            last_two_moves = [
                game_state.move_history[-2].cards,
                game_state.move_history[-1].cards
            ]
        
        # 创建模拟信息集
        info_set = MockInfoSet(
            position=user_position,
            hand_cards=user_cards,
            last_move=last_move,
            last_two_moves=last_two_moves,
            legal_actions=legal_moves,
            last_pid=last_pid
        )
        
        suggestions = []
        
        # 尝试使用PerfectDou智能体
        if self._perfectdou_agent and user_position in self._perfectdou_agent:
            try:
                agent = self._perfectdou_agent[user_position]
                suggestion = agent.act(info_set)
                if suggestion in legal_moves:
                    suggestions.append(suggestion)
            except Exception as e:
                print(f"PerfectDou智能体出错: {e}")
        
        # 尝试使用RLCard智能体
        if self._rlcard_agent and user_position in self._rlcard_agent:
            try:
                agent = self._rlcard_agent[user_position]
                suggestion = agent.act(info_set)
                if suggestion in legal_moves and suggestion not in suggestions:
                    suggestions.append(suggestion)
            except Exception as e:
                print(f"RLCard智能体出错: {e}")
        
        return suggestions
    
    def _generate_diverse_advice(self, legal_moves: List[List[int]], 
                               ai_suggestions: List[List[int]], 
                               num_suggestions: int) -> List[MoveAdvice]:
        """生成多样化的建议"""
        advice_list = []
        
        # AI建议（高置信度）
        for i, suggestion in enumerate(ai_suggestions[:num_suggestions]):
            card_info = self.card_parser.get_card_type_info(suggestion)
            advice = MoveAdvice(
                cards=suggestion,
                description=card_info["description"],
                confidence=0.9 - i * 0.1,
                move_type=card_info["type"],
                reasoning="AI智能体推荐"
            )
            advice_list.append(advice)
        
        # 补充其他选项
        remaining_slots = num_suggestions - len(advice_list)
        if remaining_slots > 0:
            other_moves = [move for move in legal_moves if move not in ai_suggestions]
            
            for move in other_moves[:remaining_slots]:
                card_info = self.card_parser.get_card_type_info(move)
                confidence = 0.6 if move == [] else 0.5  # 过牌有一定合理性
                reasoning = "过牌等待时机" if move == [] else "备选方案"
                
                advice = MoveAdvice(
                    cards=move,
                    description=card_info["description"],
                    confidence=confidence,
                    move_type=card_info["type"],
                    reasoning=reasoning
                )
                advice_list.append(advice)
        
        return advice_list[:num_suggestions]
