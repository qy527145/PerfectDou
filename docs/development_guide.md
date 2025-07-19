# PerfectDou 开发指南

## 📁 项目结构

```
PerfectDou/
├── src/
│   └── perfectdou/              # 主要的 Python 包
│       ├── __init__.py
│       ├── battle_assistant/    # 实战助手模块
│       │   ├── __init__.py
│       │   ├── ai_advisor.py    # AI顾问
│       │   ├── battle_interface.py  # 对战界面
│       │   ├── card_parser.py   # 牌型解析器
│       │   └── game_state.py    # 游戏状态管理
│       ├── cli/                 # 命令行工具
│       │   ├── __init__.py
│       │   ├── battle_assistant.py  # 实战助手入口
│       │   ├── demo_battle_assistant.py  # 演示程序
│       │   ├── evaluate.py      # 评估工具
│       │   └── generate_eval_data.py  # 数据生成工具
│       ├── env/                 # 游戏环境
│       │   ├── __init__.py
│       │   ├── env.py          # 环境接口
│       │   ├── game.py         # 游戏逻辑
│       │   └── ...
│       ├── evaluation/          # 评估模块
│       │   ├── __init__.py
│       │   ├── simulation.py   # 仿真评估
│       │   └── ...
│       └── model/              # 模型文件
│           ├── douzero/        # DouZero模型
│           └── perfectdou/     # PerfectDou模型
├── tests/                      # 测试文件
│   ├── __init__.py
│   └── test_battle_assistant.py
├── docs/                       # 文档
│   ├── battle_assistant_guide.md
│   └── development_guide.md
├── pyproject.toml             # 项目配置
├── poetry.lock               # 依赖锁定文件
├── README.md                 # 项目说明
├── LICENSE                   # 许可证
└── 数据文件 (*.json, *.so)    # 配置和二进制文件
```

## 🛠️ 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/Netease-Games-AI-Lab-Guangzhou/PerfectDou.git
cd PerfectDou
```

### 2. 安装依赖
```bash
# 安装 Poetry（如果尚未安装）
pip install poetry

# 安装项目依赖
poetry install
```

### 3. 激活虚拟环境
```bash
poetry shell
```

## 📦 包管理

### Poetry Scripts
项目配置了以下命令行工具：

```toml
[tool.poetry.scripts]
evaluate = "perfectdou.cli.evaluate:main"
generate-eval = "perfectdou.cli.generate_eval_data:main"
battle = "perfectdou.cli.battle_assistant:main"
demo = "perfectdou.cli.demo_battle_assistant:main"
```

### 使用方法
```bash
# 运行评估
poetry run evaluate --help

# 生成评估数据
poetry run generate-eval --help

# 启动实战助手
poetry run battle

# 运行演示
poetry run demo
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
poetry run python tests/test_battle_assistant.py

# 运行特定测试
poetry run python -m pytest tests/ -v
```

### 测试覆盖
- 牌型解析功能测试
- 游戏状态管理测试
- AI顾问功能测试

## 🔧 开发工具

### 代码格式化
```bash
# 使用 Black 格式化代码
poetry run black src/ tests/

# 使用 flake8 检查代码风格
poetry run flake8 src/ tests/
```

### 类型检查
```bash
# 使用 mypy 进行类型检查
poetry run mypy src/
```

## 📝 添加新功能

### 1. 添加新的CLI命令
1. 在 `src/perfectdou/cli/` 下创建新的模块
2. 实现 `main()` 函数
3. 在 `pyproject.toml` 中添加 script 配置

### 2. 扩展实战助手功能
1. 在 `src/perfectdou/battle_assistant/` 下添加新模块
2. 更新相关的接口和测试
3. 更新文档

### 3. 添加新的评估方法
1. 在 `src/perfectdou/evaluation/` 下添加新模块
2. 实现评估接口
3. 添加相应的测试

## 🚀 发布流程

### 1. 版本管理
```bash
# 更新版本号
poetry version patch  # 或 minor, major

# 查看当前版本
poetry version
```

### 2. 构建包
```bash
# 构建分发包
poetry build
```

### 3. 发布
```bash
# 发布到 PyPI
poetry publish
```

## 📋 代码规范

### Python 代码风格
- 遵循 PEP 8 标准
- 使用 Black 进行代码格式化
- 使用 flake8 进行代码检查
- 使用 mypy 进行类型检查

### 文档规范
- 所有公共函数和类都应有文档字符串
- 使用中文编写用户文档
- 使用英文编写代码注释和文档字符串

### 提交规范
- 使用清晰的提交信息
- 每个提交应该是一个逻辑单元
- 大的功能应该分解为多个小的提交

## 🤝 贡献指南

### 1. Fork 项目
在 GitHub 上 fork 项目到您的账户

### 2. 创建分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发和测试
- 编写代码
- 添加测试
- 运行测试确保通过

### 4. 提交更改
```bash
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request
在 GitHub 上创建 Pull Request

## 📞 获取帮助

如果您在开发过程中遇到问题：
1. 查看现有的 Issues
2. 创建新的 Issue 描述问题
3. 联系维护者获取帮助

---

**Happy Coding!** 🎉
