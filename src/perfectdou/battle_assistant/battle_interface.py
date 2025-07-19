"""
斗地主实战界面模块

提供用户友好的命令行交互界面，支持实时输入和AI建议显示。
"""

import os
import sys
from typing import List, Optional, Dict
from .game_state import GameState, Position
from .card_parser import CardParser
from .ai_advisor import AIAdvisor


class BattleInterface:
    """斗地主实战交互界面"""
    
    def __init__(self):
        """初始化界面"""
        self.card_parser = CardParser()
        self.ai_advisor = AIAdvisor()
        self.game_state: Optional[GameState] = None
        
    def start_battle(self):
        """开始实战模式"""
        self._print_welcome()
        
        # 初始化游戏
        if not self._initialize_game():
            return
        
        # 主游戏循环
        self._game_loop()
        
    def _print_welcome(self):
        """打印欢迎信息"""
        print("=" * 60)
        print("🎮 PerfectDou 斗地主实战助手")
        print("=" * 60)
        print("欢迎使用AI斗地主助手！我将为您提供最优出牌建议。")
        print()
        
    def _initialize_game(self) -> bool:
        """初始化游戏设置"""
        print("📋 游戏初始化")
        print("-" * 30)
        
        # 选择身份
        position = self._select_position()
        if not position:
            return False
        
        self.game_state = GameState(position)
        
        # 输入手牌
        if not self._input_initial_cards():
            return False
        
        print("\n✅ 游戏初始化完成！")
        return True
    
    def _select_position(self) -> Optional[Position]:
        """选择玩家身份"""
        print("请选择您的身份：")
        print("1. 地主")
        print("2. 地主上家（农民）")
        print("3. 地主下家（农民）")
        
        while True:
            try:
                choice = input("\n请输入选择 (1-3): ").strip()
                if choice == '1':
                    return Position.LANDLORD
                elif choice == '2':
                    return Position.LANDLORD_UP
                elif choice == '3':
                    return Position.LANDLORD_DOWN
                else:
                    print("❌ 无效选择，请输入 1-3")
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                return None
    
    def _input_initial_cards(self) -> bool:
        """输入初始手牌"""
        print(f"\n您的身份：{self._position_to_chinese(self.game_state.user_position)}")
        print("\n📝 请输入您的手牌")
        print("支持格式：3 4 5 J Q K A 2 小王 大王")
        print("或简化：345JQKA2小大")
        
        while True:
            try:
                cards_input = input("\n手牌: ").strip()
                if not cards_input:
                    print("❌ 请输入手牌")
                    continue
                
                # 解析手牌
                try:
                    user_cards = self.card_parser.parse_cards(cards_input)
                    if not user_cards:
                        print("❌ 未识别到有效牌型")
                        continue
                    
                    # 验证手牌数量
                    expected_count = 17 if self.game_state.user_position != Position.LANDLORD else 17
                    if len(user_cards) < 10 or len(user_cards) > 20:
                        print(f"⚠️  手牌数量异常：{len(user_cards)}张，通常应该是17张（农民）或20张（地主）")
                        confirm = input("是否继续？(y/n): ").strip().lower()
                        if confirm != 'y':
                            continue
                    
                    print(f"✅ 识别手牌：{self.card_parser.cards_to_display(user_cards)}")
                    print(f"   共 {len(user_cards)} 张")
                    
                    # 如果是地主，询问底牌
                    landlord_cards = None
                    if self.game_state.user_position == Position.LANDLORD:
                        landlord_cards = self._input_landlord_cards()
                        if landlord_cards is None:
                            continue
                    
                    # 设置手牌
                    if self.game_state.set_initial_cards(user_cards, landlord_cards):
                        return True
                    else:
                        print("❌ 手牌设置失败，请重新输入")
                        
                except ValueError as e:
                    print(f"❌ 牌型解析错误：{e}")
                    print("请检查输入格式，例如：3 4 5 J Q K A 2 小王 大王")
                    
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                return False
    
    def _input_landlord_cards(self) -> Optional[List[int]]:
        """输入地主底牌"""
        print("\n请输入地主底牌（3张）：")
        
        while True:
            try:
                cards_input = input("底牌: ").strip()
                if not cards_input:
                    print("❌ 请输入底牌")
                    continue
                
                landlord_cards = self.card_parser.parse_cards(cards_input)
                if len(landlord_cards) != 3:
                    print(f"❌ 底牌必须是3张，您输入了{len(landlord_cards)}张")
                    continue
                
                print(f"✅ 底牌：{self.card_parser.cards_to_display(landlord_cards)}")
                return landlord_cards
                
            except ValueError as e:
                print(f"❌ 底牌解析错误：{e}")
            except KeyboardInterrupt:
                return None
    
    def _game_loop(self):
        """主游戏循环"""
        print("\n" + "=" * 60)
        print("🎯 游戏开始！")
        print("=" * 60)
        
        while self.game_state.phase.value == "playing":
            try:
                # 显示当前局面
                self._display_current_situation()
                
                # 处理当前回合
                if self.game_state.current_player == self.game_state.user_position:
                    # 用户回合
                    if not self._handle_user_turn():
                        break
                else:
                    # 对手回合
                    if not self._handle_opponent_turn():
                        break
                        
            except KeyboardInterrupt:
                print("\n\n👋 游戏结束！")
                break
        
        if self.game_state.phase.value == "finished":
            self._display_game_result()
    
    def _display_current_situation(self):
        """显示当前局面"""
        situation = self.game_state.get_current_situation()
        
        print(f"\n📊 当前局面")
        print("-" * 30)
        print(f"当前出牌：{self._position_to_chinese(Position(situation['current_player']))}")
        
        # 显示各玩家剩余牌数
        for pos_str, player_info in situation["players"].items():
            pos = Position(pos_str)
            name = self._position_to_chinese(pos)
            count = player_info["remaining_count"]
            is_user = player_info["is_user"]
            
            if is_user:
                cards = player_info["hand_cards"]
                print(f"{name}：{count}张 - {cards}")
            else:
                print(f"{name}：{count}张")
        
        # 显示上一手牌
        if situation["last_move"] and situation["last_move"]["cards"]:
            last_pos = self._position_to_chinese(Position(situation["last_move"]["position"]))
            last_cards = situation["last_move"]["cards"]
            last_desc = situation["last_move"]["description"]
            print(f"\n上一手：{last_pos} 出了 {last_cards} ({last_desc})")
        elif situation["last_move"]:
            last_pos = self._position_to_chinese(Position(situation["last_move"]["position"]))
            print(f"\n上一手：{last_pos} 过牌")
    
    def _handle_user_turn(self) -> bool:
        """处理用户回合"""
        print(f"\n🎯 轮到您出牌！")
        
        # 获取AI建议
        advice_list = self.ai_advisor.get_move_advice(self.game_state)
        
        if advice_list:
            print("\n🤖 AI建议：")
            for i, advice in enumerate(advice_list, 1):
                cards_display = self.card_parser.cards_to_display(advice.cards) if advice.cards else "过牌"
                confidence_str = f"{advice.confidence:.0%}"
                print(f"  {i}. {cards_display} ({advice.description}) - 置信度:{confidence_str}")
                print(f"     理由：{advice.reasoning}")
        
        # 用户输入
        while True:
            try:
                user_input = input(f"\n请出牌（输入'pass'过牌，'help'查看帮助）: ").strip()
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'pass':
                    # 过牌
                    if self.game_state.make_move(self.game_state.user_position, []):
                        print("✅ 您选择过牌")
                        return True
                    else:
                        print("❌ 无法过牌")
                        continue
                else:
                    # 解析出牌
                    try:
                        cards = self.card_parser.parse_cards(user_input)
                        if self.game_state.make_move(self.game_state.user_position, cards):
                            card_info = self.card_parser.get_card_type_info(cards)
                            print(f"✅ 您出了：{self.card_parser.cards_to_display(cards)} ({card_info['description']})")
                            return True
                        else:
                            print("❌ 无效出牌，请重新输入")
                    except ValueError as e:
                        print(f"❌ 输入错误：{e}")
                        
            except KeyboardInterrupt:
                return False
    
    def _handle_opponent_turn(self) -> bool:
        """处理对手回合"""
        current_pos = self._position_to_chinese(self.game_state.current_player)
        print(f"\n⏳ 等待 {current_pos} 出牌...")
        
        try:
            user_input = input("请输入对手的出牌（'pass'表示过牌）: ").strip()
            
            if user_input.lower() == 'pass':
                # 对手过牌
                if self.game_state.make_move(self.game_state.current_player, []):
                    print(f"✅ {current_pos} 过牌")
                    return True
            else:
                # 解析对手出牌
                try:
                    cards = self.card_parser.parse_cards(user_input)
                    if self.game_state.make_move(self.game_state.current_player, cards):
                        card_info = self.card_parser.get_card_type_info(cards)
                        print(f"✅ {current_pos} 出了：{self.card_parser.cards_to_display(cards)} ({card_info['description']})")
                        return True
                    else:
                        print("❌ 无效出牌，请重新输入")
                except ValueError as e:
                    print(f"❌ 输入错误：{e}")
                    
        except KeyboardInterrupt:
            return False
        
        return True
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n📖 帮助信息")
        print("-" * 30)
        print("输入格式示例：")
        print("  单牌：3, K, A, 2, 小王, 大王")
        print("  对子：3 3, K K, A A")
        print("  三张：3 3 3, K K K")
        print("  炸弹：3 3 3 3, K K K K")
        print("  王炸：小王 大王 或 小 大")
        print("  顺子：3 4 5 6 7")
        print("  连对：3 3 4 4 5 5")
        print("\n特殊命令：")
        print("  pass - 过牌")
        print("  help - 显示此帮助")
        print("  quit - 退出游戏")
    
    def _position_to_chinese(self, position: Position) -> str:
        """位置转中文"""
        mapping = {
            Position.LANDLORD: "地主",
            Position.LANDLORD_UP: "地主上家",
            Position.LANDLORD_DOWN: "地主下家"
        }
        return mapping.get(position, str(position))
    
    def _display_game_result(self):
        """显示游戏结果"""
        print("\n" + "=" * 60)
        print("🎉 游戏结束！")
        print("=" * 60)
        # 这里可以添加胜负判断和统计信息
