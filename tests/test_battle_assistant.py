#!/usr/bin/env python3
"""
PerfectDou 实战助手测试脚本

测试各个模块的基本功能。
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from perfectdou.battle_assistant import CardParser, GameState, AIAdvisor, Position


def test_card_parser():
    """测试牌型解析器"""
    print("🧪 测试牌型解析器")
    print("-" * 30)
    
    parser = CardParser()
    
    # 测试用例
    test_cases = [
        "3 4 5 J Q K A",
        "345JQKA",
        "三四五 J Q K A",
        "小王 大王",
        "小 大",
        "3 3 4 4 5 5",
        "K K K K",
        "pass"
    ]
    
    for case in test_cases:
        try:
            if case == "pass":
                print(f"输入: '{case}' -> 过牌")
                continue
                
            cards = parser.parse_cards(case)
            display = parser.cards_to_display(cards)
            card_info = parser.get_card_type_info(cards)
            print(f"输入: '{case}'")
            print(f"  解析: {cards}")
            print(f"  显示: {display}")
            print(f"  类型: {card_info['description']}")
            print()
        except Exception as e:
            print(f"输入: '{case}' -> 错误: {e}")
    
    print("✅ 牌型解析器测试完成\n")


def test_game_state():
    """测试游戏状态管理"""
    print("🧪 测试游戏状态管理")
    print("-" * 30)
    
    # 创建游戏状态
    game_state = GameState(Position.LANDLORD)
    
    # 设置初始手牌
    user_cards = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 3, 4, 5, 6]
    landlord_cards = [20, 30, 17]
    
    success = game_state.set_initial_cards(user_cards, landlord_cards)
    print(f"设置手牌: {'成功' if success else '失败'}")
    
    # 显示当前状态
    situation = game_state.get_current_situation()
    print(f"当前阶段: {situation['phase']}")
    print(f"当前玩家: {situation['current_player']}")
    print(f"用户手牌: {situation['players']['landlord']['hand_cards']}")
    
    # 测试出牌
    success = game_state.make_move(Position.LANDLORD, [3])
    print(f"出牌测试: {'成功' if success else '失败'}")
    
    print("✅ 游戏状态管理测试完成\n")


def test_ai_advisor():
    """测试AI顾问"""
    print("🧪 测试AI顾问")
    print("-" * 30)
    
    # 创建游戏状态
    game_state = GameState(Position.LANDLORD)
    user_cards = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17]
    game_state.set_initial_cards(user_cards)
    
    # 创建AI顾问
    advisor = AIAdvisor()
    
    try:
        # 获取建议
        advice_list = advisor.get_move_advice(game_state, num_suggestions=3)
        
        if advice_list:
            print("AI建议:")
            for i, advice in enumerate(advice_list, 1):
                parser = CardParser()
                cards_display = parser.cards_to_display(advice.cards) if advice.cards else "过牌"
                print(f"  {i}. {cards_display} ({advice.description})")
                print(f"     置信度: {advice.confidence:.0%}")
                print(f"     理由: {advice.reasoning}")
        else:
            print("未获取到AI建议（可能是模型未加载）")
            
    except Exception as e:
        print(f"AI顾问测试出错: {e}")
    
    print("✅ AI顾问测试完成\n")


def main():
    """主测试函数"""
    print("🔬 PerfectDou 实战助手功能测试")
    print("=" * 50)
    print()
    
    try:
        # 运行各项测试
        test_card_parser()
        test_game_state()
        test_ai_advisor()
        
        print("🎉 所有测试完成！")
        print("\n💡 提示：如果AI顾问测试显示模型未加载，这是正常的。")
        print("   实际使用时，程序会尝试加载PerfectDou模型。")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
