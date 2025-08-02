# [NeurIPS 2022] PerfectDou: 通过完美信息蒸馏主导斗地主
NeurIPS 2022 论文《PerfectDou: Dominating DouDizhu with Perfect Information Distillation》的官方代码库。

**注意：我们仅发布了预训练模型和评估代码。由于使用了分布式系统，训练代码目前不可用。计算剩余手牌和特征工程的代码以共享库（即 *.so 文件）的形式提供，这两个模块的详细信息可以在论文中找到。一旦我们决定开源这些代码，我们会第一时间通知您。**

## 在线演示，快来体验吧！
* 在线演示：[https://outer-perfectdou-demo-gzailab.nie.netease.com](https://outer-perfectdou-demo-gzailab.nie.netease.com)

## 关于 PerfectDou

PerfectDou 是目前最先进的[斗地主](https://baike.baidu.com/item/%E6%96%97%E5%9C%B0%E4%B8%BB/177997) ([DouDizhu](https://en.wikipedia.org/wiki/Dou_dizhu)) AI系统，由**网易游戏AI实验室**与**上海交通大学**和**卡内基梅隆大学**共同开发。

所提出的完美信息蒸馏技术（一个完美训练-不完美执行框架）允许智能体利用全局信息来指导策略训练，就像在完美信息游戏中一样，而训练好的策略可以在实际游戏过程中用于不完美信息游戏。

<img width="500" src="images/result.jpg" alt="result" />

更多详细信息，请查看我们的[论文](https://arxiv.org/abs/2203.16406)，其中展示了PerfectDou如何以及为什么能够击败所有现有的AI程序，并达到最先进的性能。

*   论文链接：[https://arxiv.org/abs/2203.16406](https://arxiv.org/abs/2203.16406)


## 引用本工作

```bibtex
@inproceedings{yang2022perfectdou,
  title={PerfectDou: Dominating DouDizhu with Perfect Information Distillation},
  author={Yang, Guan and Liu, Minghuan and Hong, Weijun and Zhang, Weinan and Fang, Fei and Zeng, Guangjun and Lin, Yue},
  booktitle={NeurIPS},
  year={2022}
}
```

## 评估流程
预训练模型在 `perfectdou/model/` 中提供。为了便于比较，游戏环境和评估方法与 [DouZero](https://github.com/kwai/DouZero/tree/main/douzero/evaluation) 中的相同。

还提供了一些预训练模型和启发式方法作为基线：
*   [random](douzero/evaluation/random_agent.py)：随机（均匀）游戏的智能体
*   [rlcard](douzero/evaluation/rlcard_agent.py)：[RLCard](https://github.com/datamllab/rlcard) 中基于规则的智能体
*   [DouZero](https://github.com/kwai/DouZero)：ADP（平均差分点数）版本
*  PerfectDou：论文中的 2.5e9 帧版本

### 步骤 0：准备环境

首先，克隆代码库：
```
git clone https://github.com/Netease-Games-AI-Lab-Guangzhou/PerfectDou.git
```
确保您已安装 Python 3.7，然后使用 uv 安装依赖：
```
cd PerfectDou
uv sync
```

或者，如果您没有安装 uv，可以先安装 uv：
```
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

cd PerfectDou
uv sync
```

如果您需要开发依赖（用于测试和代码格式化），请运行：
```
uv sync --extra dev
```

### 步骤 1：生成评估数据
```
uv run generate-eval
```
一些重要的超参数如下：
*   `--output`：保存序列化数据的位置
*   `--num_games`：将生成多少个随机游戏，默认为 10000

### 步骤 2：自我对弈
```
uv run evaluate
```
一些重要的超参数如下：
*   `--landlord`：哪个智能体将扮演地主，可以是 random、rlcard、douzero、perfectdou 或预训练模型的路径
*   `--landlord_up`：哪个智能体将扮演地主上家（地主前面的玩家），可以是 random、rlcard、douzero、perfectdou 或预训练模型的路径
*   `--landlord_down`：哪个智能体将扮演地主下家（地主后面的玩家），可以是 random、rlcard、douzero、perfectdou 或预训练模型的路径
*   `--eval_data`：包含评估数据的 pickle 文件
*   `--num_workers`：将使用多少个子进程

例如，以下命令评估 PerfectDou 在地主位置对抗 DouZero 智能体：
```
uv run evaluate --landlord perfectdou --landlord_up douzero --landlord_down douzero
```

## 🎮 实战助手功能

我们新增了**斗地主实战助手**功能，为您的实际对战提供AI决策支持！

### 快速开始
```bash
# 启动实战助手
uv run battle

# 或运行演示
uv run demo
```

### 主要特性
- **🤖 AI智能决策**：基于PerfectDou模型提供最优出牌建议
- **📊 实时状态跟踪**：管理游戏进程、手牌变化、出牌历史
- **🎯 多格式输入**：支持中文、英文、简化等多种牌型输入
- **💡 策略分析**：提供出牌理由和置信度评估
- **🎨 友好界面**：直观的命令行交互体验

### 使用示例
```bash
# 1. 选择身份（地主/地主上家/地主下家）
请选择您的身份：
1. 地主
2. 地主上家（农民）
3. 地主下家（农民）

# 2. 输入手牌（支持多种格式）
手牌: 3 4 5 6 7 8 9 10 J Q K A 2 小王 大王
# 或简化输入: 3456789TJQKA2小大

# 3. 获取AI建议
🤖 AI建议：
  1. K (单张K) - 置信度:90%
     理由：AI智能体推荐
  2. pass (过牌) - 置信度:60%
     理由：过牌等待时机

# 4. 输入您的选择
请出牌（输入'pass'过牌，'help'查看帮助）: K
```

### 功能测试
```bash
# 运行功能测试
uv run python tests/test_battle_assistant.py

# 或运行所有测试
uv run python -m pytest tests/ -v
```

### 📚 相关文档
- **[实战助手使用指南](docs/battle_assistant_guide.md)**: 详细的使用说明和技巧
- **[开发指南](docs/development_guide.md)**: 开发环境设置和贡献指南
- **[项目概览](docs/project_overview.md)**: 项目结构和功能概述

## 致谢
*   演示主要基于 [RLCard-Showdown](https://github.com/datamllab/rlcard-showdown)
*   评估代码和游戏环境实现主要基于 [DouZero](https://github.com/kwai/DouZero)

## 联系我们
如果您有任何问题，请联系我们。

yangguan@corp.netease.com

minghuanliu@sjtu.edu.cn

hongweijun@corp.netease.com

gzzengguangjun@corp.netease.com














