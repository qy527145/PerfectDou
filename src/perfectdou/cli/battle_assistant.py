#!/usr/bin/env python3
"""
PerfectDou 斗地主实战助手

使用AI技术为您的斗地主实战提供最优决策建议。

使用方法：
    python battle_assistant.py

功能特点：
- 基于PerfectDou AI模型的智能决策
- 支持多种牌型输入格式
- 实时游戏状态跟踪
- 多样化出牌建议
- 用户友好的交互界面
"""

from perfectdou.battle_assistant import BattleInterface


def main():
    """主函数"""
    try:
        # 创建并启动实战界面
        interface = BattleInterface()
        interface.start_battle()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用PerfectDou实战助手！")
    except Exception as e:
        print(f"\n❌ 程序出现错误：{e}")
        print("请检查依赖是否正确安装，或联系开发者获取帮助。")


if __name__ == "__main__":
    main()
