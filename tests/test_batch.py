"""
批量处理功能单元测试
"""
import unittest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from main import cli
from dotenv import load_dotenv

# 在导入 main 之前设置环境变量
load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = 'test_key'


class TestBatchCommand(unittest.TestCase):
    """批量处理命令测试"""

    @classmethod
    def setUpClass(cls):
        """类级别设置：设置环境变量"""
        os.environ['OPENAI_API_KEY'] = 'test_key'

    @classmethod
    def tearDownClass(cls):
        """类级别清理：清理环境变量"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']

    def setUp(self):
        """测试前准备"""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_batch_with_file(self):
        """测试批量处理文件"""
        # 创建测试文件（包含实际的错误 trace）
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', str(test_file),
                    '--language', 'python',
                    '--template', 'modern'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)
                mock_generator_class.assert_called_once()
                mock_gen_instance.generate_poem.assert_called()

    def test_batch_with_directory(self):
        """测试批量处理目录"""
        # 创建测试文件
        test_file1 = Path(self.temp_dir) / "test1.py"
        test_file1.write_text("""Traceback (most recent call last):
  File "test1.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
""")

        test_file2 = Path(self.temp_dir) / "test2.py"
        test_file2.write_text("""Traceback (most recent call last):
  File "test2.py", line 1, in <module>
    undefined_variable
NameError: name 'undefined_variable' is not defined
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', self.temp_dir,
                    '--language', 'python'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)
                # ErrorCollector may extract multiple errors from each file
                # At minimum should call twice (once per file)
                self.assertGreaterEqual(mock_gen_instance.generate_poem.call_count, 2)

    def test_batch_output_json(self):
        """测试批量处理输出 JSON 格式"""
        # 创建测试文件
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', str(test_file),
                    '--output', os.path.join(self.temp_dir, 'output.json'),
                    '--format', 'json'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)

                # 验证 JSON 文件
                output_file = Path(self.temp_dir) / 'output.json'
                self.assertTrue(output_file.exists())

                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    self.assertIn('total', data)
                    self.assertIn('poems', data)
                    # ErrorCollector may extract multiple components from a single traceback
                    self.assertGreaterEqual(data['total'], 1)

    def test_batch_output_html(self):
        """测试批量处理输出 HTML 格式"""
        # 创建测试文件
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', str(test_file),
                    '--output', os.path.join(self.temp_dir, 'output.html'),
                    '--format', 'html'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)

                # 验证 HTML 文件
                output_file = Path(self.temp_dir) / 'output.html'
                self.assertTrue(output_file.exists())

                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn('<!DOCTYPE html>', content)
                    self.assertIn('Error Message Poet', content)

    def test_batch_output_text(self):
        """测试批量处理输出文本格式"""
        # 创建测试文件
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', str(test_file),
                    '--output', os.path.join(self.temp_dir, 'output.txt'),
                    '--format', 'text'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)

                # 验证文本文件
                output_file = Path(self.temp_dir) / 'output.txt'
                self.assertTrue(output_file.exists())

                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn('错误:', content)
                    self.assertIn('诗歌:', content)

    def test_batch_no_errors(self):
        """测试批量处理无错误的情况"""
        # 创建测试文件（无错误）
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("print('Hello, World!')")

        # 运行命令
        with patch('main.validate_config', return_value=True):
            result = self.runner.invoke(cli, [
                'batch',
                '--input', str(test_file),
                '--language', 'python'
            ])

            # 验证结果
            self.assertEqual(result.exit_code, 1)
            self.assertIn("未找到错误消息", result.output)

    def test_batch_invalid_input(self):
        """测试批量处理无效输入"""
        # 运行命令
        result = self.runner.invoke(cli, [
            'batch',
            '--input', '/nonexistent/path'
        ])

        # 验证结果
        # exit_code 可能是 1（配置错误）或 2（路径不存在）
        self.assertIn(result.exit_code, [1, 2])

    def test_batch_progress_display(self):
        """测试批量处理进度显示"""
        # 创建测试文件
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero

Traceback (most recent call last):
  File "test.py", line 3, in <module>
    undefined_variable
NameError: name 'undefined_variable' is not defined
""")

        # 模拟 PoetryGenerator 和 validate_config
        with patch('main.PoetryGenerator') as mock_generator_class:
            with patch('main.validate_config', return_value=True):
                mock_gen_instance = MagicMock()
                mock_gen_instance.generate_poem.return_value = "测试诗歌"
                mock_generator_class.return_value = mock_gen_instance

                result = self.runner.invoke(cli, [
                    'batch',
                    '--input', str(test_file),
                    '--language', 'python'
                ])

                # 验证结果
                self.assertEqual(result.exit_code, 0)
                # 应该显示进度信息
                self.assertIn("进度:", result.output)


if __name__ == '__main__':
    unittest.main()