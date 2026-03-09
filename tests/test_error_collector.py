"""
错误收集模块单元测试
"""
import unittest
import os
import tempfile
from error_collector import ErrorCollector, collect_errors


class TestErrorCollector(unittest.TestCase):
    """错误收集器测试"""

    def setUp(self):
        """测试前准备"""
        self.collector = ErrorCollector()

    def test_collect_python_errors_from_string(self):
        """测试从字符串收集 Python 错误"""
        python_code = """
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    divide(10, 0)
  File "test.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
"""

        errors = self.collector.collect_from_string(python_code, "python")

        self.assertGreater(len(errors), 0)
        self.assertTrue(any(e["language"] == "python" for e in errors))

    def test_collect_javascript_errors_from_string(self):
        """测试从字符串收集 JavaScript 错误"""
        javascript_code = """
Error: division by zero
    at divide (test.js:2:15)
    at <anonymous> (test.js:5:5)
"""

        errors = self.collector.collect_from_string(javascript_code, "javascript")

        self.assertGreater(len(errors), 0)
        self.assertTrue(any(e["language"] == "javascript" for e in errors))

    def test_collect_from_file(self):
        """测试从文件收集错误"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    divide(10, 0)
  File "test.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
""")
            temp_file = f.name

        try:
            errors = self.collector.collect_from_file(temp_file, "python")
            self.assertGreater(len(errors), 0)
        finally:
            os.unlink(temp_file)

    def test_format_error(self):
        """测试错误格式化"""
        error = {
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "file": "test.py",
            "line": 3,
            "function": "divide",
            "language": "python"
        }

        formatted = self.collector.format_error(error)
        self.assertIn("ZeroDivisionError", formatted)
        self.assertIn("division by zero", formatted)

    def test_get_error_summary(self):
        """测试错误摘要"""
        errors = [
            {"type": "ZeroDivisionError", "message": "division by zero", "file": "test.py", "line": 3, "function": "divide", "language": "python"},
            {"type": "TypeError", "message": "unsupported operand type", "file": "test.py", "line": 5, "function": "add", "language": "python"},
            {"type": "ReferenceError", "message": "x is not defined", "file": "app.js", "line": 10, "function": "init", "language": "javascript"}
        ]

        summary = self.collector.get_error_summary(errors)

        self.assertEqual(summary["total"], 3)
        self.assertIn("ZeroDivisionError", summary["types"])
        self.assertIn("python", summary["languages"])

    def test_collect_from_traceback(self):
        """测试从 traceback 收集错误"""
        try:
            1 / 0
        except:
            errors = self.collector.collect_from_traceback()

        self.assertGreater(len(errors), 0)

    def test_collect_errors_convenience_function(self):
        """测试便捷函数"""
        python_code = """
Traceback (most recent call last):
  File "test.py", line 2, in <module>
    1 / 0
ZeroDivisionError: division by zero
"""

        errors = collect_errors(python_code, "python")

        self.assertGreater(len(errors), 0)

    def test_unsupported_language(self):
        """测试不支持的语言"""
        with self.assertRaises(ValueError):
            self.collector.collect_from_string("code", "unsupported")


if __name__ == '__main__':
    unittest.main()