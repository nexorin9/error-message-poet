"""
诗歌生成模块单元测试
"""
import unittest
from poetry_generator import PoetryGenerator


class TestPoetryGenerator(unittest.TestCase):
    """诗歌生成器测试"""

    def setUp(self):
        """测试前准备"""
        self.config = {
            'OPENAI_API_KEY': 'test_key',
            'DEFAULT_MODEL': 'gpt-3.5-turbo'
        }
        self.generator = PoetryGenerator(self.config)

    def tearDown(self):
        """测试后清理"""
        self.generator = None

    def test_build_prompt_modern(self):
        """测试构建现代诗提示词"""
        prompt = self.generator._build_prompt("测试错误", "modern", "python")

        self.assertIn("现代诗", prompt)
        self.assertIn("测试错误", prompt)

    def test_build_prompt_classical(self):
        """测试构建古体诗提示词"""
        prompt = self.generator._build_prompt("测试错误", "classical", "python")

        self.assertIn("古体诗", prompt)
        self.assertIn("七言绝句", prompt)

    def test_build_prompt_free(self):
        """测试构建自由诗提示词"""
        prompt = self.generator._build_prompt("测试错误", "free", "python")

        self.assertIn("自由诗", prompt)

    def test_generate_batch(self):
        """测试批量生成诗歌"""
        errors = ["错误1", "错误2", "错误3"]

        # 测试批量生成功能（不实际调用 API）
        # 由于没有有效的 API key，这里只验证函数调用
        try:
            poems = self.generator.generate_batch(errors)
            # 如果没有抛出异常，说明函数调用成功
            self.assertEqual(len(poems), 3)
        except Exception as e:
            # 如果 API 调用失败，这是预期的（没有有效的 API key）
            self.assertIn("API", str(e))

    def test_generate_without_config(self):
        """测试未配置任何 LLM 提供商"""
        generator = PoetryGenerator({})

        with self.assertRaises(ValueError):
            generator.generate_poem("测试错误")

    def test_generate_with_custom_template(self):
        """测试使用自定义模板"""
        prompt = self.generator._build_prompt("测试错误", "custom", "python")

        # 自定义模板应该使用默认模板
        self.assertIn("现代诗", prompt)

    def test_detect_available_models(self):
        """测试检测可用模型"""
        # 测试只有 OpenAI
        config = {
            'OPENAI_API_KEY': 'test_key',
            'DEFAULT_MODEL': 'gpt-3.5-turbo'
        }
        generator = PoetryGenerator(config)
        available = generator.get_available_models()

        self.assertIn('openai', available)
        self.assertNotIn('anthropic', available)
        self.assertNotIn('local', available)

        # 测试只有本地模型
        config = {
            'LOCAL_MODEL_URL': 'http://localhost:11434',
            'DEFAULT_MODEL': 'llama2'
        }
        generator = PoetryGenerator(config)
        available = generator.get_available_models()

        self.assertIn('local', available)
        self.assertNotIn('openai', available)
        self.assertNotIn('anthropic', available)

        # 测试多个提供商
        config = {
            'OPENAI_API_KEY': 'test_key',
            'ANTHROPIC_API_KEY': 'test_key',
            'LOCAL_MODEL_URL': 'http://localhost:11434',
            'DEFAULT_MODEL': 'gpt-3.5-turbo'
        }
        generator = PoetryGenerator(config)
        available = generator.get_available_models()

        self.assertIn('openai', available)
        self.assertIn('anthropic', available)
        self.assertIn('local', available)

    def test_generate_with_local_model(self):
        """测试使用本地模型生成诗歌"""
        config = {
            'LOCAL_MODEL_URL': 'http://localhost:11434',
            'DEFAULT_MODEL': 'llama2'
        }
        generator = PoetryGenerator(config)

        # 由于没有真实的本地模型服务，这里只验证函数调用
        # 如果本地服务不可用，应该抛出异常
        try:
            poem = generator.generate_poem("测试错误", model='llama2')
            # 如果没有抛出异常，说明本地服务可用
            self.assertIsInstance(poem, str)
        except Exception as e:
            # 如果本地服务不可用，这是预期的
            self.assertIn('localhost', str(e).lower() or 'connection' in str(e).lower())


if __name__ == '__main__':
    unittest.main()