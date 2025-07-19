"""
游戏状态管理模块

管理斗地主游戏的当前状态，包括手牌、出牌历史、当前轮次等信息。
"""

from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from .card_parser import CardParser


class Position(Enum):
    """玩家位置枚举"""
    LANDLORD = "landlord"           # 地主
    LANDLORD_UP = "landlord_up"     # 地主上家（农民）
    LANDLORD_DOWN = "landlord_down" # 地主下家（农民）


class GamePhase(Enum):
    """游戏阶段枚举"""
    INIT = "init"           # 初始化
    PLAYING = "playing"     # 游戏中
    FINISHED = "finished"   # 游戏结束


@dataclass
class MoveRecord:
    """出牌记录"""
    position: Position
    cards: List[int]
    move_type: str
    description: str
    timestamp: Optional[str] = None


@dataclass
class PlayerInfo:
    """玩家信息"""
    position: Position
    hand_cards: List[int] = field(default_factory=list)
    played_cards: List[int] = field(default_factory=list)
    remaining_count: int = 0
    is_user: bool = False


class GameState:
    """游戏状态管理器"""
    
    def __init__(self, user_position: Position):
        """
        初始化游戏状态
        
        Args:
            user_position: 用户的位置（地主/地主上家/地主下家）
        """
        self.card_parser = CardParser()
        self.user_position = user_position
        self.phase = GamePhase.INIT
        
        # 玩家信息
        self.players = {
            Position.LANDLORD: PlayerInfo(Position.LANDLORD),
            Position.LANDLORD_UP: PlayerInfo(Position.LANDLORD_UP),
            Position.LANDLORD_DOWN: PlayerInfo(Position.LANDLORD_DOWN)
        }
        self.players[user_position].is_user = True
        
        # 游戏状态
        self.current_player = Position.LANDLORD  # 当前出牌玩家
        self.last_move: Optional[MoveRecord] = None
        self.move_history: List[MoveRecord] = []
        self.three_landlord_cards: List[int] = []
        
        # 出牌控制
        self.need_follow = False  # 是否需要跟牌
        self.last_valid_move: Optional[MoveRecord] = None  # 上一个有效出牌
        
    def set_initial_cards(self, user_cards: List[int], 
                         landlord_cards: Optional[List[int]] = None) -> bool:
        """
        设置初始手牌
        
        Args:
            user_cards: 用户的手牌
            landlord_cards: 地主的三张底牌（如果用户是地主）
            
        Returns:
            是否设置成功
        """
        try:
            # 验证牌型合法性
            if not self.card_parser.validate_cards(user_cards):
                return False
            
            # 设置用户手牌
            self.players[self.user_position].hand_cards = sorted(user_cards)
            self.players[self.user_position].remaining_count = len(user_cards)
            
            # 如果用户是地主，设置底牌
            if self.user_position == Position.LANDLORD and landlord_cards:
                if not self.card_parser.validate_cards(landlord_cards):
                    return False
                self.three_landlord_cards = sorted(landlord_cards)
                # 地主手牌包含底牌
                all_landlord_cards = user_cards + landlord_cards
                self.players[Position.LANDLORD].hand_cards = sorted(all_landlord_cards)
                self.players[Position.LANDLORD].remaining_count = len(all_landlord_cards)
            
            # 估算其他玩家的手牌数量
            if self.user_position == Position.LANDLORD:
                # 地主20张，农民各17张
                self.players[Position.LANDLORD_UP].remaining_count = 17
                self.players[Position.LANDLORD_DOWN].remaining_count = 17
            else:
                # 地主20张，农民17张
                self.players[Position.LANDLORD].remaining_count = 20
                other_farmer = (Position.LANDLORD_UP if self.user_position == Position.LANDLORD_DOWN 
                              else Position.LANDLORD_DOWN)
                self.players[other_farmer].remaining_count = 17
            
            self.phase = GamePhase.PLAYING
            return True
            
        except Exception as e:
            print(f"设置初始手牌失败: {e}")
            return False
    
    def make_move(self, position: Position, cards: List[int]) -> bool:
        """
        执行出牌动作
        
        Args:
            position: 出牌玩家位置
            cards: 出的牌
            
        Returns:
            是否出牌成功
        """
        try:
            # 验证是否轮到该玩家
            if position != self.current_player:
                return False
            
            # 创建出牌记录
            if not cards:  # 过牌
                move_record = MoveRecord(
                    position=position,
                    cards=[],
                    move_type="pass",
                    description="过牌"
                )
            else:
                # 验证牌型
                card_info = self.card_parser.get_card_type_info(cards)
                move_record = MoveRecord(
                    position=position,
                    cards=sorted(cards),
                    move_type=card_info["type"],
                    description=card_info["description"]
                )
                
                # 更新玩家手牌（如果是用户）
                if position == self.user_position:
                    for card in cards:
                        if card in self.players[position].hand_cards:
                            self.players[position].hand_cards.remove(card)
                        else:
                            return False  # 用户没有这张牌
                
                # 更新已出牌记录
                self.players[position].played_cards.extend(cards)
                self.players[position].remaining_count -= len(cards)
                
                # 更新最后有效出牌
                self.last_valid_move = move_record
                self.need_follow = True
            
            # 记录出牌
            self.move_history.append(move_record)
            self.last_move = move_record
            
            # 切换到下一个玩家
            self._next_player()
            
            # 检查游戏是否结束
            if self.players[position].remaining_count == 0:
                self.phase = GamePhase.FINISHED
            
            return True
            
        except Exception as e:
            print(f"出牌失败: {e}")
            return False
    
    def _next_player(self):
        """切换到下一个玩家"""
        if self.current_player == Position.LANDLORD:
            self.current_player = Position.LANDLORD_UP
        elif self.current_player == Position.LANDLORD_UP:
            self.current_player = Position.LANDLORD_DOWN
        else:
            self.current_player = Position.LANDLORD
    
    def get_current_situation(self) -> Dict:
        """获取当前局面信息"""
        return {
            "phase": self.phase.value,
            "current_player": self.current_player.value,
            "user_position": self.user_position.value,
            "is_user_turn": self.current_player == self.user_position,
            "need_follow": self.need_follow,
            "last_move": {
                "position": self.last_move.position.value if self.last_move else None,
                "cards": self.card_parser.cards_to_display(self.last_move.cards) if self.last_move else None,
                "description": self.last_move.description if self.last_move else None
            } if self.last_move else None,
            "players": {
                pos.value: {
                    "remaining_count": player.remaining_count,
                    "is_user": player.is_user,
                    "hand_cards": self.card_parser.cards_to_display(player.hand_cards) if player.is_user else None
                }
                for pos, player in self.players.items()
            }
        }
    
    def get_user_hand_cards(self) -> List[int]:
        """获取用户当前手牌"""
        return self.players[self.user_position].hand_cards.copy()
    
    def get_legal_moves_context(self) -> Dict:
        """获取合法出牌的上下文信息"""
        context = {
            "need_follow": self.need_follow,
            "last_valid_move": None,
            "user_cards": self.get_user_hand_cards(),
            "can_pass": self.need_follow
        }
        
        if self.last_valid_move:
            context["last_valid_move"] = {
                "position": self.last_valid_move.position.value,
                "cards": self.last_valid_move.cards,
                "type": self.last_valid_move.move_type,
                "description": self.last_valid_move.description
            }
        
        return context
    
    def reset_game(self):
        """重置游戏状态"""
        self.phase = GamePhase.INIT
        self.current_player = Position.LANDLORD
        self.last_move = None
        self.move_history = []
        self.three_landlord_cards = []
        self.need_follow = False
        self.last_valid_move = None
        
        for player in self.players.values():
            player.hand_cards = []
            player.played_cards = []
            player.remaining_count = 0
