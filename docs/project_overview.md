# PerfectDou 项目概览

## 🎯 项目简介

PerfectDou 是基于 NeurIPS 2022 论文的先进斗地主 AI 系统，采用完美信息蒸馏技术，在斗地主游戏中达到了最先进的性能。

## 📁 项目结构

### 核心包结构
```
src/perfectdou/
├── battle_assistant/    # 🎮 实战助手模块
├── cli/                # 🖥️ 命令行工具
├── env/                # 🎲 游戏环境
├── evaluation/         # 📊 评估模块
└── model/             # 🤖 AI模型
```

### 主要功能模块

#### 1. 实战助手 (`battle_assistant/`)
- **AI顾问** (`ai_advisor.py`): 提供智能出牌建议
- **对战界面** (`battle_interface.py`): 用户交互界面
- **牌型解析** (`card_parser.py`): 多格式牌型输入解析
- **状态管理** (`game_state.py`): 游戏状态跟踪

#### 2. 命令行工具 (`cli/`)
- **实战助手** (`battle_assistant.py`): 主要的对战程序
- **演示程序** (`demo_battle_assistant.py`): 功能演示
- **评估工具** (`evaluate.py`): 模型性能评估
- **数据生成** (`generate_eval_data.py`): 评估数据生成

#### 3. 游戏环境 (`env/`)
- 斗地主游戏逻辑实现
- 动作生成和检测
- 游戏状态编码

#### 4. 评估模块 (`evaluation/`)
- 多种AI智能体实现
- 仿真对战评估
- 性能指标计算

## 🚀 快速开始

### 安装依赖
```bash
poetry install
```

### 主要命令

#### 实战助手
```bash
# 启动实战助手
poetry run battle

# 运行演示
poetry run demo
```

#### 模型评估
```bash
# 生成评估数据
poetry run generate-eval

# 运行评估
poetry run evaluate --landlord perfectdou --landlord_up douzero --landlord_down douzero
```

#### 测试
```bash
# 运行功能测试
poetry run python tests/test_battle_assistant.py
```

## 🎮 实战助手特性

### 核心功能
- **🤖 AI智能决策**: 基于PerfectDou模型的最优策略
- **📊 实时状态跟踪**: 完整的游戏状态管理
- **🎯 多格式输入**: 支持中英文、简化等多种输入方式
- **💡 策略分析**: 提供出牌理由和置信度评估

### 支持的输入格式
| 格式 | 示例 | 说明 |
|------|------|------|
| 标准格式 | `3 4 5 J Q K A 2 小王 大王` | 空格分隔 |
| 简化格式 | `345JQKA2小大` | 紧凑输入 |
| 中文格式 | `三四五 J Q K A 二 小王 大王` | 中文数字 |

## 📊 模型性能

PerfectDou 在与现有AI系统的对比中表现优异：
- 击败所有现有的斗地主AI程序
- 在大规模评估中达到最先进性能
- 基于完美信息蒸馏的创新训练方法

## 🛠️ 开发指南

### 项目配置
- **包管理**: Poetry
- **Python版本**: >=3.7,<3.8
- **主要依赖**: torch, onnxruntime, rlcard

### 代码规范
- 遵循 PEP 8 标准
- 使用 Black 进行代码格式化
- 使用 mypy 进行类型检查

### 测试覆盖
- 牌型解析功能测试
- 游戏状态管理测试
- AI顾问功能测试

## 📚 文档资源

- **[实战助手使用指南](battle_assistant_guide.md)**: 详细的使用说明
- **[开发指南](development_guide.md)**: 开发环境设置和贡献指南
- **[项目README](../README.md)**: 项目基本信息和安装说明

## 🔗 相关链接

- **论文**: [PerfectDou: Dominating DouDizhu with Perfect Information Distillation](https://arxiv.org/abs/2203.16406)
- **在线演示**: [https://outer-perfectdou-demo-gzailab.nie.netease.com](https://outer-perfectdou-demo-gzailab.nie.netease.com)
- **GitHub**: [项目仓库](https://github.com/Netease-Games-AI-Lab-Guangzhou/PerfectDou)

## 📞 联系我们

如有问题或建议，欢迎联系：
- yangguan@corp.netease.com
- minghuanliu@sjtu.edu.cn
- hongweijun@corp.netease.com
- gzzengguangjun@corp.netease.com

---

**让AI助您成为斗地主高手！** 🎉
