# Error Message Poet

Transform system error messages into poetry, exploring the poetic expression of technical text.

## Features

- 📥 Collect Python and JavaScript error messages
- 🎨 Use LLM to transform errors into poetry
- 🖥️ Command-line interface
- 📦 Batch processing support
- 💾 Result caching
- 🌐 Support for local and remote LLMs
- 📊 Error message analysis
- ✨ Poetry quality evaluation
- 📝 Multiple poetry templates (modern, classical, free verse)

## Installation

```bash
cd error-poet
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit the `.env` file to configure API keys:

```env
# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Local model URL (optional)
LOCAL_MODEL_URL=http://localhost:11434

# Cache directory
CACHE_DIR=./cache

# Output format
OUTPUT_FORMAT=text

# Poetry template
TEMPLATE=modern
```

## Usage

### Command Line Tool

#### Convert a single error

```bash
python main.py convert --input "Error: connection timeout"
```

#### Batch conversion

```bash
python main.py batch --input errors.txt --output poems.txt
```

#### Analyze errors

```bash
python main.py analyze --input errors.txt
```

#### View configuration

```bash
python main.py config
```

### Python API

```python
from error_collector import collect_errors_from_traceback
from poetry_generator import PoetryGenerator
from poetry_quality import evaluate_poetry

# Collect error
try:
    result = 1 / 0
except ZeroDivisionError as e:
    error = collect_errors_from_traceback(e)

# Generate poem
generator = PoetryGenerator()
poem = generator.generate(error)

# Evaluate poem quality
quality = evaluate_poetry(poem, error['message'])
print(f"Overall score: {quality['score']}/100")
```

### JavaScript API

```javascript
const { collectErrorsFromError } = require('./error_collector.js');
const { PoetryGenerator } = require('./poetry_generator.js');
const { evaluatePoetry } = require('./poetry_quality.js');

// Collect error
try {
    const result = 1 / 0;
} catch (error) {
    const errorObj = collectErrorsFromError(error);

    // Generate poem
    const generator = new PoetryGenerator();
    const poem = generator.generate(errorObj);

    // Evaluate poem quality
    const quality = evaluatePoetry(poem, errorObj.message);
    console.log(`Overall score: ${quality.score}/100`);
}
```

## Examples

### Python Examples

```bash
# Run all examples
python examples/example_python.py

# Run specific example
python examples/example_python.py 1  # Single error conversion
python examples/example_python.py 2  # Batch conversion
python examples/example_python.py 3  # Using templates
python examples/example_python.py 4  # Quality report
python examples/example_python.py 5  # Error analysis
```

### JavaScript Examples

```bash
# Run all examples
node examples/example_javascript.js

# Run specific example
node examples/example_javascript.js 1  # Single error conversion
node examples/example_javascript.js 2  # Batch conversion
node examples/example_javascript.js 3  # Using templates
node examples/example_javascript.js 4  # Quality report
node examples/example_javascript.js 5  # Error analysis
```

## Poetry Quality Evaluation

Error Message Poet provides multi-dimensional poetry quality evaluation:

- **Fluency**: Based on sentence length variance, stop word ratio, repetition analysis
- **Poeticness**: Based on imagery words, rhetorical devices, rhyme checking
- **Accuracy**: Based on error keyword matching
- **Coherence**: Based on repetition ratio, paragraph structure

Evaluation results include overall score and detailed feedback.

## Project Structure

```
error-poet/
├── main.py              # CLI entry point
├── config.py            # Configuration management
├── poetry_generator.py  # Poetry generation
├── error_collector.py   # Error collection
├── error_analyzer.py    # Error analysis
├── poetry_quality.py    # Poetry quality evaluation
├── template_loader.py   # Template loading
├── cache_manager.py     # Cache management
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
├── README.md            # Project documentation
├── README_EN.md         # Project documentation (English)
├── templates/           # Template directory
│   ├── modern.yaml
│   ├── classical.yaml
│   └── free.yaml
├── examples/            # Example code
│   ├── example_python.py
│   └── example_javascript.js
└── tests/               # Test directory
    ├── test_error_collector.py
    ├── test_poetry_generator.py
    ├── test_error_analyzer.py
    └── test_poetry_quality.py
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_poetry_generator.py -v
```

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!

---

## Support the Author

If you find this project helpful, feel free to buy me a coffee! ☕

![Buy Me a Coffee](buymeacoffee.png)

**Buy me a coffee (crypto)**

| Chain | Address |
|-------|---------|
| BTC | `bc1qc0f5tv577z7yt59tw8sqaq3tey98xehy32frzd` |
| ETH / USDT | `0x3b7b6c47491e4778157f0756102f134d05070704` |
| SOL | `6Xuk373zc6x6XWcAAuqvbWW92zabJdCmN3CSwpsVM6sd` |
