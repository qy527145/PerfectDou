#!/usr/bin/env python3
"""
PerfectDou 实战助手演示脚本

展示实战助手的核心功能，无需完整的交互流程。
"""

from perfectdou.battle_assistant import CardParser, GameState, AIAdvisor, Position


def demo_card_parsing():
    """演示牌型解析功能"""
    print("🎴 牌型解析演示")
    print("=" * 40)
    
    parser = CardParser()
    
    test_inputs = [
        "3 4 5 J Q K A",      # 标准格式
        "345JQKA",            # 简化格式
        "小王 大王",           # 王炸
        "小 大",              # 王炸简化
        "KKKK",               # 炸弹
        "3 3 4 4 5 5",        # 连对
        "三四五六七",          # 中文数字
    ]
    
    for card_input in test_inputs:
        try:
            cards = parser.parse_cards(card_input)
            display = parser.cards_to_display(cards)
            card_info = parser.get_card_type_info(cards)
            
            print(f"输入: '{card_input}'")
            print(f"  → 解析: {display}")
            print(f"  → 类型: {card_info['description']}")
            print()
        except Exception as e:
            print(f"输入: '{card_input}' → 错误: {e}")
            print()


def demo_game_state():
    """演示游戏状态管理"""
    print("🎮 游戏状态管理演示")
    print("=" * 40)
    
    # 创建游戏状态（用户是地主）
    game_state = GameState(Position.LANDLORD)
    
    # 设置手牌
    user_cards = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 3, 4, 5, 6]
    landlord_cards = [20, 30, 17]  # 底牌：大王、小王、2
    
    success = game_state.set_initial_cards(user_cards, landlord_cards)
    print(f"✅ 初始化游戏: {'成功' if success else '失败'}")
    
    # 显示当前状态
    situation = game_state.get_current_situation()
    print(f"📊 当前状态:")
    print(f"  - 游戏阶段: {situation['phase']}")
    print(f"  - 当前玩家: {situation['current_player']}")
    print(f"  - 用户身份: {situation['user_position']}")
    print(f"  - 是否用户回合: {situation['is_user_turn']}")
    
    # 显示手牌
    parser = CardParser()
    user_hand = game_state.get_user_hand_cards()
    print(f"  - 用户手牌: {parser.cards_to_display(user_hand)}")
    print(f"  - 手牌数量: {len(user_hand)}张")
    
    # 模拟出牌
    print(f"\n🎯 模拟出牌:")
    success = game_state.make_move(Position.LANDLORD, [3])
    if success:
        print(f"  ✅ 地主出了: 3")
        updated_hand = game_state.get_user_hand_cards()
        print(f"  📝 剩余手牌: {parser.cards_to_display(updated_hand)}")
    
    print()


def demo_ai_advisor():
    """演示AI决策顾问"""
    print("🤖 AI决策顾问演示")
    print("=" * 40)
    
    # 创建游戏状态
    game_state = GameState(Position.LANDLORD)
    user_cards = [3, 4, 5, 11, 12, 13, 14, 17, 20, 30]  # 简化手牌
    game_state.set_initial_cards(user_cards)
    
    # 创建AI顾问
    advisor = AIAdvisor()
    
    print("📋 当前手牌: 3 4 5 J Q K A 2 小王 大王")
    print("🎯 获取AI建议...")
    
    try:
        advice_list = advisor.get_move_advice(game_state, num_suggestions=3)
        
        if advice_list:
            print("\n💡 AI建议:")
            for i, advice in enumerate(advice_list, 1):
                parser = CardParser()
                cards_display = parser.cards_to_display(advice.cards) if advice.cards else "过牌"
                confidence_str = f"{advice.confidence:.0%}"
                print(f"  {i}. {cards_display}")
                print(f"     类型: {advice.description}")
                print(f"     置信度: {confidence_str}")
                print(f"     理由: {advice.reasoning}")
                print()
        else:
            print("⚠️  未获取到AI建议（可能是模型未加载）")
            print("   在实际使用中，程序会尝试加载PerfectDou模型")
            
    except Exception as e:
        print(f"❌ AI顾问出错: {e}")
    
    print()


def demo_battle_scenario():
    """演示实战场景"""
    print("⚔️  实战场景演示")
    print("=" * 40)
    
    # 创建游戏状态（用户是农民）
    game_state = GameState(Position.LANDLORD_UP)
    user_cards = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17]
    game_state.set_initial_cards(user_cards)
    
    parser = CardParser()
    
    print("🎭 场景: 您是地主上家（农民）")
    print(f"📋 您的手牌: {parser.cards_to_display(user_cards)}")
    print()
    
    # 模拟地主出牌
    print("🎯 地主出了: 3")
    game_state.make_move(Position.LANDLORD, [3])
    
    # 轮到用户
    print("⏰ 轮到您出牌...")
    
    # 获取AI建议
    advisor = AIAdvisor()
    advice_list = advisor.get_move_advice(game_state, num_suggestions=2)
    
    if advice_list:
        print("🤖 AI建议:")
        for i, advice in enumerate(advice_list, 1):
            cards_display = parser.cards_to_display(advice.cards) if advice.cards else "过牌"
            print(f"  {i}. {cards_display} - {advice.reasoning}")
    
    # 模拟用户选择
    print("\n✅ 您选择出: 4")
    game_state.make_move(Position.LANDLORD_UP, [4])
    
    # 显示更新后的状态
    situation = game_state.get_current_situation()
    print(f"📊 当前状态: 轮到{situation['current_player']}出牌")
    
    remaining_cards = game_state.get_user_hand_cards()
    print(f"📝 您的剩余手牌: {parser.cards_to_display(remaining_cards)}")
    print(f"   剩余数量: {len(remaining_cards)}张")
    
    print()


def main():
    """主演示函数"""
    print("🎉 PerfectDou 实战助手功能演示")
    print("=" * 60)
    print("这个演示将展示实战助手的核心功能")
    print()
    
    try:
        demo_card_parsing()
        demo_game_state()
        demo_ai_advisor()
        demo_battle_scenario()
        
        print("🎊 演示完成！")
        print()
        print("💡 使用提示:")
        print("  - 运行 'poetry run battle' 开始实战模式")
        print("  - 运行 'poetry run python tests/test_battle_assistant.py' 进行功能测试")
        print("  - 查看 'docs/battle_assistant_guide.md' 获取详细使用说明")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
