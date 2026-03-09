"""
错误消息分析模块测试
"""
import pytest
from error_analyzer import ErrorAnalyzer, analyze_errors, generate_error_report


class TestErrorAnalyzer:
    """错误分析器测试"""

    def test_analyze_empty_errors(self):
        """测试空错误列表"""
        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors([])

        assert result["total"] == 0
        assert result["types"] == {}
        assert result["categories"] == {}
        assert result["severities"] == {}
        assert result["keywords"] == {}

    def test_analyze_network_errors(self):
        """测试网络错误分析"""
        errors = [
            {"type": "ConnectionError", "message": "Connection timeout after 30 seconds", "language": "python"},
            {"type": "TimeoutError", "message": "Request timeout", "language": "python"},
            {"type": "NetworkError", "message": "Network unreachable", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 3
        assert "network" in result["categories"]
        assert result["categories"]["network"]["ConnectionError"] == 1
        assert result["categories"]["network"]["TimeoutError"] == 1
        assert result["categories"]["network"]["NetworkError"] == 1

    def test_analyze_database_errors(self):
        """测试数据库错误分析"""
        errors = [
            {"type": "OperationalError", "message": "Database connection failed", "language": "python"},
            {"type": "ProgrammingError", "message": "Invalid SQL query", "language": "python"},
            {"type": "IntegrityError", "message": "Duplicate entry", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 3
        assert "database" in result["categories"]
        assert result["categories"]["database"]["OperationalError"] == 1
        assert result["categories"]["database"]["ProgrammingError"] == 1
        assert result["categories"]["database"]["IntegrityError"] == 1

    def test_analyze_severity(self):
        """测试严重程度评估"""
        errors = [
            {"type": "FatalError", "message": "System crash - unrecoverable", "language": "python"},
            {"type": "Error", "message": "Failed to connect to server", "language": "python"},
            {"type": "Warning", "message": "Deprecated API usage", "language": "python"},
            {"type": "Info", "message": "Debug information", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 4
        assert result["severities"]["critical"] == 1
        assert result["severities"]["high"] == 1
        assert result["severities"]["medium"] == 1
        assert result["severities"]["low"] == 1

    def test_extract_keywords(self):
        """测试关键词提取"""
        errors = [
            {"type": "Error", "message": "Connection timeout occurred", "language": "python"},
            {"type": "Error", "message": "Database query failed", "language": "python"},
            {"type": "Error", "message": "File not found error", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 3
        assert len(result["keywords"]) > 0
        assert "connection" in result["keywords"]
        assert "timeout" in result["keywords"]
        assert "database" in result["keywords"]

    def test_error_statistics(self):
        """测试错误统计"""
        errors = [
            {"type": "Error", "message": "Test error", "language": "python", "file": "test.py", "line": 10},
            {"type": "Error", "message": "Test error", "language": "python", "file": "test.py", "line": 20},
            {"type": "Error", "message": "Test error", "language": "javascript", "file": "app.js", "line": 15},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 3
        assert result["statistics"]["by_language"]["python"] == 2
        assert result["statistics"]["by_language"]["javascript"] == 1
        assert result["statistics"]["by_file"]["test.py"] == 2
        assert result["statistics"]["by_file"]["app.js"] == 1
        assert result["statistics"]["most_common_type"] == "Error"
        assert result["statistics"]["most_common_type_count"] == 3

    def test_get_error_report(self):
        """测试错误报告生成"""
        errors = [
            {"type": "ConnectionError", "message": "Connection timeout", "language": "python"},
            {"type": "Error", "message": "Failed operation", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        report = analyzer.get_error_report(analyzer.analyze_errors(errors))

        assert "错误消息分析报告" in report
        assert "总错误数: 2" in report
        assert "network" in report
        assert "high" in report

    def test_error_type_classification(self):
        """测试错误类型分类"""
        errors = [
            {"type": "FileNotFoundError", "message": "File not found at path", "language": "python"},
            {"type": "PermissionError", "message": "Permission denied", "language": "python"},
            {"type": "ValueError", "message": "Invalid value provided", "language": "python"},
        ]

        analyzer = ErrorAnalyzer()
        result = analyzer.analyze_errors(errors)

        assert result["total"] == 3
        assert "file" in result["categories"]
        assert "validation" in result["categories"]
        assert result["categories"]["file"]["FileNotFoundError"] == 1
        assert result["categories"]["file"]["PermissionError"] == 1
        assert result["categories"]["validation"]["ValueError"] == 1


class TestConvenienceFunctions:
    """便捷函数测试"""

    def test_analyze_errors_function(self):
        """测试 analyze_errors 便捷函数"""
        errors = [
            {"type": "Error", "message": "Test error", "language": "python"},
        ]

        result = analyze_errors(errors)

        assert result["total"] == 1
        assert "types" in result

    def test_generate_error_report_function(self):
        """测试 generate_error_report 便捷函数"""
        errors = [
            {"type": "Error", "message": "Test error", "language": "python"},
        ]

        report = generate_error_report(errors)

        assert "错误消息分析报告" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])