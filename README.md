# Error Message Poet

将系统错误消息转化为诗歌，探索技术文本的诗意表达。

## 功能特性

- 📥 收集 Python 和 JavaScript 错误消息
- 🎨 使用 LLM 将错误转化为诗歌
- 🖥️ 命令行界面
- 📦 支持批量处理
- 💾 结果缓存
- 🌐 支持本地和远程 LLM
- 📊 错误消息分析
- ✨ 诗歌质量评估
- 📝 多种诗歌模板（现代诗、古体诗、自由诗）

## 安装

```bash
cd error-poet
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置 API 密钥：

```env
# OpenAI API Key（可选）
OPENAI_API_KEY=your_openai_api_key

# Anthropic API Key（可选）
ANTHROPIC_API_KEY=your_anthropic_api_key

# 本地模型 URL（可选）
LOCAL_MODEL_URL=http://localhost:11434

# 缓存目录
CACHE_DIR=./cache

# 输出格式
OUTPUT_FORMAT=text

# 诗歌模板
TEMPLATE=modern
```

## 使用方法

### 命令行工具

#### 转换单个错误

```bash
python main.py convert --input "Error: connection timeout"
```

#### 批量转换

```bash
python main.py batch --input errors.txt --output poems.txt
```

#### 分析错误

```bash
python main.py analyze --input errors.txt
```

#### 查看配置

```bash
python main.py config
```

### Python API

```python
from error_collector import collect_errors_from_traceback
from poetry_generator import PoetryGenerator
from poetry_quality import evaluate_poetry

# 收集错误
try:
    result = 1 / 0
except ZeroDivisionError as e:
    error = collect_errors_from_traceback(e)

# 生成诗歌
generator = PoetryGenerator()
poem = generator.generate(error)

# 评估诗歌质量
quality = evaluate_poetry(poem, error['message'])
print(f"综合得分: {quality['score']}/100")
```

### JavaScript API

```javascript
const { collectErrorsFromError } = require('./error_collector.js');
const { PoetryGenerator } = require('./poetry_generator.js');
const { evaluatePoetry } = require('./poetry_quality.js');

// 收集错误
try {
    const result = 1 / 0;
} catch (error) {
    const errorObj = collectErrorsFromError(error);

    // 生成诗歌
    const generator = new PoetryGenerator();
    const poem = generator.generate(errorObj);

    // 评估诗歌质量
    const quality = evaluatePoetry(poem, errorObj.message);
    console.log(`综合得分: ${quality.score}/100`);
}
```

## 示例

### Python 示例

```bash
# 运行所有示例
python examples/example_python.py

# 运行特定示例
python examples/example_python.py 1  # 单个错误转换
python examples/example_python.py 2  # 批量转换
python examples/example_python.py 3  # 使用模板
python examples/example_python.py 4  # 质量报告
python examples/example_python.py 5  # 错误分析
```

### JavaScript 示例

```bash
# 运行所有示例
node examples/example_javascript.js

# 运行特定示例
node examples/example_javascript.js 1  # 单个错误转换
node examples/example_javascript.js 2  # 批量转换
node examples/example_javascript.js 3  # 使用模板
node examples/example_javascript.js 4  # 质量报告
node examples/example_javascript.js 5  # 错误分析
```

## 诗歌质量评估

Error Message Poet 提供多维度诗歌质量评估：

- **流畅度**: 基于句子长度方差、停用词比例、重复词分析
- **诗意**: 基于意象词、修辞手法、押韵检查
- **准确性**: 基于错误关键词匹配
- **连贯性**: 基于重复词比例、段落结构

评估结果包含综合得分和详细反馈。

## 项目结构

```
error-poet/
├── main.py              # CLI 入口
├── config.py            # 配置管理
├── poetry_generator.py  # 诗歌生成
├── error_collector.py   # 错误收集
├── error_analyzer.py    # 错误分析
├── poetry_quality.py    # 诗歌质量评估
├── template_loader.py   # 模板加载
├── cache_manager.py     # 缓存管理
├── requirements.txt     # 依赖
├── .env.example         # 环境变量示例
├── README.md            # 项目文档
├── templates/           # 模板目录
│   ├── modern.yaml
│   ├── classical.yaml
│   └── free.yaml
├── examples/            # 示例代码
│   ├── example_python.py
│   └── example_javascript.js
└── tests/               # 测试目录
    ├── test_error_collector.py
    ├── test_poetry_generator.py
    ├── test_error_analyzer.py
    └── test_poetry_quality.py
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_poetry_generator.py -v
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 支持作者

如果您觉得这个项目对您有帮助，欢迎打赏支持！

![Buy Me a Coffee](buymeacoffee.png)

**Buy me a coffee (crypto)**

| 币种 | 地址 |
|------|------|
| BTC | `bc1qc0f5tv577z7yt59tw8sqaq3tey98xehy32frzd` |
| ETH / USDT | `0x3b7b6c47491e4778157f0756102f134d05070704` |
| SOL | `6Xuk373zc6x6XWcAAuqvbWW92zabJdCmN3CSwpsVM6sd` |
