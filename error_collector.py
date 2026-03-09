"""
错误收集模块 - 收集 Python 和 JavaScript 的错误消息
"""
import os
import re
import json
from typing import List, Dict, Any, Optional
import traceback as tb_module


class ErrorCollector:
    """错误收集器"""

    def __init__(self):
        """初始化错误收集器"""
        self.errors = []

    def collect_from_file(
        self,
        file_path: str,
        language: str = "python"
    ) -> List[Dict[str, Any]]:
        """
        从文件收集错误

        Args:
            file_path: 文件路径
            language: 编程语言 (python, javascript)

        Returns:
            错误消息列表
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if language == "python":
            return self._collect_python_errors(content)
        elif language == "javascript":
            return self._collect_javascript_errors(content)
        else:
            raise ValueError(f"Unsupported language: {language}")

    def collect_from_string(
        self,
        content: str,
        language: str = "python"
    ) -> List[Dict[str, Any]]:
        """
        从字符串收集错误

        Args:
            content: 代码内容
            language: 编程语言

        Returns:
            错误消息列表
        """
        if language == "python":
            return self._collect_python_errors(content)
        elif language == "javascript":
            return self._collect_javascript_errors(content)
        else:
            raise ValueError(f"Unsupported language: {language}")

    def collect_from_traceback(
        self,
        exc_info: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        从 traceback 收集错误

        Args:
            exc_info: 异常信息 (sys.exc_info())

        Returns:
            错误消息列表
        """
        if exc_info is None:
            exc_info = tb_module.extract_stack()
        else:
            # 如果提供了 exc_info，需要提取 traceback
            if len(exc_info) >= 3:
                exc_info = tb_module.extract_tb(exc_info[2])

        errors = []
        # extract_stack 和 extract_tb 都返回 StackSummary
        if hasattr(exc_info, '__iter__'):
            for frame in exc_info:
                # StackSummary 中的元素是 FrameSummary
                if hasattr(frame, 'filename'):
                    error = {
                        "type": getattr(frame, 'name', 'unknown'),
                        "file": frame.filename,
                        "line": frame.lineno,
                        "code": getattr(frame, 'line', ''),
                        "message": f"Error in {getattr(frame, 'name', 'unknown')} at {frame.filename}:{frame.lineno}"
                    }
                    errors.append(error)

        return errors

    def _collect_python_errors(self, content: str) -> List[Dict[str, Any]]:
        """收集 Python 错误"""
        errors = []

        # 匹配 Python 错误模式
        patterns = [
            r"Traceback \(most recent call last\):(.+?)(?=\Z)",
            r"Error:\s*(.+?)(?=\n\s*\n|\Z)",
            r"Exception:\s*(.+?)(?=\n\s*\n|\Z)",
            r"File \"([^\"]+)\", line (\d+), in ([^\s]+)\s*(.+?)$",
            r"(\w+Error):\s*(.+?)$"
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                error = self._parse_python_error(match, content)
                if error:
                    errors.append(error)

        return errors

    def _parse_python_error(self, match: re.Match, content: str) -> Optional[Dict[str, Any]]:
        """解析 Python 错误"""
        error_text = match.group(0)

        # 提取错误类型
        error_type_match = re.search(r"(\w+Error):\s*(.*?)$", error_text)
        if error_type_match:
            error_type = error_type_match.group(1)
            error_message = error_type_match.group(2).strip()
        else:
            error_type = "UnknownError"
            error_message = error_text.strip()

        # 提取文件和行号
        file_match = re.search(r"File \"([^\"]+)\", line (\d+)", error_text)
        if file_match:
            file_path = file_match.group(1)
            line_number = int(file_match.group(2))
        else:
            file_path = "unknown"
            line_number = 0

        # 提取函数名
        func_match = re.search(r"in ([^\s]+)", error_text)
        if func_match:
            func_name = func_match.group(1)
        else:
            func_name = "unknown"

        return {
            "type": error_type,
            "message": error_message,
            "file": file_path,
            "line": line_number,
            "function": func_name,
            "language": "python"
        }

    def _collect_javascript_errors(self, content: str) -> List[Dict[str, Any]]:
        """收集 JavaScript 错误"""
        errors = []

        # 匹配 JavaScript 错误模式
        patterns = [
            r"Error:\s*(.+?)(?=\n\s*\n|\Z)",
            r"TypeError:\s*(.+?)(?=\n\s*\n|\Z)",
            r"ReferenceError:\s*(.+?)(?=\n\s*\n|\Z)",
            r"SyntaxError:\s*(.+?)(?=\n\s*\n|\Z)",
            r"at\s+([^\s]+)\s+\(([^)]+)\)",
            r"Uncaught\s+(.*?):\s*(.+?)$"
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                error = self._parse_javascript_error(match, content)
                if error:
                    errors.append(error)

        return errors

    def _parse_javascript_error(self, match: re.Match, content: str) -> Optional[Dict[str, Any]]:
        """解析 JavaScript 错误"""
        error_text = match.group(0)

        # 提取错误类型
        error_type_match = re.search(r"(Uncaught\s+)?(TypeError|ReferenceError|SyntaxError|Error):\s*(.*?)$", error_text)
        if error_type_match:
            error_type = error_type_match.group(2) or "Error"
            error_message = error_type_match.group(3).strip()
        else:
            error_type = "UnknownError"
            error_message = error_text.strip()

        # 提取文件和行号
        file_match = re.search(r"at\s+([^\s]+)\s+\(([^)]+)\)", error_text)
        if file_match:
            file_path = file_match.group(2)
            line_number = 0  # JavaScript 错误通常不包含行号
        else:
            file_path = "unknown"
            line_number = 0

        # 提取函数名
        func_match = re.search(r"at\s+([^\s]+)\s+\(", error_text)
        if func_match:
            func_name = func_match.group(1)
        else:
            func_name = "unknown"

        return {
            "type": error_type,
            "message": error_message,
            "file": file_path,
            "line": line_number,
            "function": func_name,
            "language": "javascript"
        }

    def format_error(self, error: Dict[str, Any]) -> str:
        """
        格式化错误消息

        Args:
            error: 错误字典

        Returns:
            格式化后的错误消息
        """
        if error["language"] == "python":
            return f"{error['type']}: {error['message']} at {error['file']}:{error['line']}"
        else:
            return f"{error['type']}: {error['message']} at {error['file']}:{error['line']}"

    def get_error_summary(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取错误摘要

        Args:
            errors: 错误列表

        Returns:
            错误摘要
        """
        if not errors:
            return {"total": 0}

        # 统计错误类型
        type_counts = {}
        for error in errors:
            error_type = error["type"]
            type_counts[error_type] = type_counts.get(error_type, 0) + 1

        # 统计编程语言
        language_counts = {}
        for error in errors:
            language = error["language"]
            language_counts[language] = language_counts.get(language, 0) + 1

        return {
            "total": len(errors),
            "types": type_counts,
            "languages": language_counts
        }


# 便捷函数
def collect_errors(
    input_source: str,
    language: str = "python"
) -> List[Dict[str, Any]]:
    """
    便捷函数：收集错误

    Args:
        input_source: 输入源（文件路径或字符串）
        language: 编程语言

    Returns:
        错误消息列表
    """
    collector = ErrorCollector()

    if os.path.exists(input_source):
        return collector.collect_from_file(input_source, language)
    else:
        return collector.collect_from_string(input_source, language)