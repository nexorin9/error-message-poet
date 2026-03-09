"""
错误消息分析模块 - 分析错误消息的特征
"""
import re
from typing import List, Dict, Any, Set
from collections import Counter


class ErrorAnalyzer:
    """错误消息分析器"""

    # 错误类型分类规则
    ERROR_TYPE_CATEGORIES = {
        "database": ["database", "sql", "query", "table", "column", "row", "cursor", "sqlite", "mysql", "postgresql", "db", "entry", "duplicate"],
        "network": ["timeout", "network", "socket", "http", "request", "response", "api", "url", "dns", "gateway", "http", "connection"],
        "file": ["file", "directory", "path", "not found", "permission", "read", "write", "open", "close", "exists", "path"],
        "validation": ["invalid", "validation", "required", "missing", "format", "type", "constraint", "check", "value"],
        "authentication": ["authentication", "auth", "login", "password", "token", "session", "permission", "access", "login"],
        "memory": ["memory", "out of memory", "heap", "stack", "allocation", "overflow", "memory"],
        "logic": ["logic", "condition", "assert", "assertion", "index", "key", "value", "type", "logic"],
        "syntax": ["syntax", "parse", "compile", "unexpected", "illegal", "syntax"],
        "runtime": ["runtime", "exception", "error", "failed", "failed to", "runtime"],
    }

    # 严重程度关键词
    SEVERITY_KEYWORDS = {
        "critical": ["fatal", "critical", "crash", "system", "shutdown", "unrecoverable", "deadlock"],
        "high": ["error", "exception", "failed", "failed to", "cannot", "unable", "invalid"],
        "medium": ["warning", "deprecated", "obsolete", "unused", "slow", "performance"],
        "low": ["info", "debug", "trace", "notice", "suggestion"],
    }

    def __init__(self):
        """初始化分析器"""
        self.error_types = []
        self.severities = []
        self.keywords = []

    def analyze_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析错误消息

        Args:
            errors: 错误列表

        Returns:
            分析结果
        """
        if not errors:
            return {
                "total": 0,
                "types": {},
                "categories": {},
                "severities": {},
                "keywords": {},
                "statistics": {}
            }

        # 错误类型分类
        type_categories = self._classify_error_types(errors)

        # 严重程度评估
        severity_scores = self._assess_severity(errors)

        # 关键词提取
        extracted_keywords = self._extract_keywords(errors)

        # 错误消息统计
        statistics = self._get_error_statistics(errors)

        return {
            "total": len(errors),
            "types": type_categories,
            "categories": type_categories,
            "severities": severity_scores,
            "keywords": extracted_keywords,
            "statistics": statistics
        }

    def _classify_error_types(self, errors: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """
        错误类型分类

        Args:
            errors: 错误列表

        Returns:
            分类结果 {category: {error_type: count}}
        """
        categories = {category: {} for category in self.ERROR_TYPE_CATEGORIES.keys()}
        categories["other"] = {}

        for error in errors:
            error_type = error.get("type", "UnknownError")
            message = error.get("message", "").lower()

            # 查找匹配的分类（按关键词长度降序，优先匹配更长的关键词）
            matched_category = None
            for category, keywords in self.ERROR_TYPE_CATEGORIES.items():
                # 按关键词长度降序排序
                sorted_keywords = sorted(keywords, key=len, reverse=True)
                for keyword in sorted_keywords:
                    if keyword in message:
                        matched_category = category
                        break
                if matched_category:
                    break

            if matched_category:
                categories[matched_category][error_type] = categories[matched_category].get(error_type, 0) + 1
            else:
                categories["other"][error_type] = categories["other"].get(error_type, 0) + 1

        return categories

    def _assess_severity(self, errors: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        严重程度评估

        Args:
            errors: 错误列表

        Returns:
            严重程度统计 {severity: count}
        """
        severity_scores = {severity: 0 for severity in self.SEVERITY_KEYWORDS.keys()}

        for error in errors:
            message = error.get("message", "").lower()

            # 查找匹配的严重程度
            matched_severity = "low"
            for severity, keywords in self.SEVERITY_KEYWORDS.items():
                if any(keyword in message for keyword in keywords):
                    matched_severity = severity
                    break

            severity_scores[matched_severity] += 1

        return severity_scores

    def _extract_keywords(self, errors: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        关键词提取

        Args:
            errors: 错误列表

        Returns:
            关键词统计 {keyword: count}
        """
        all_keywords = []

        for error in errors:
            message = error.get("message", "").lower()

            # 提取关键词（去除常见停用词）
            words = re.findall(r'\b[a-z]{3,}\b', message)

            # 过滤停用词
            stop_words = {"the", "and", "for", "with", "from", "this", "that", "are", "was", "were", "have", "has", "had"}
            filtered_words = [word for word in words if word not in stop_words]

            all_keywords.extend(filtered_words)

        # 统计关键词频率
        keyword_counts = Counter(all_keywords).most_common(20)

        return {keyword: count for keyword, count in keyword_counts}

    def _get_error_statistics(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        错误消息统计

        Args:
            errors: 错误列表

        Returns:
            统计信息
        """
        if not errors:
            return {}

        # 按编程语言统计
        language_stats = {}
        for error in errors:
            language = error.get("language", "unknown")
            language_stats[language] = language_stats.get(language, 0) + 1

        # 按文件统计
        file_stats = {}
        for error in errors:
            file = error.get("file", "unknown")
            file_stats[file] = file_stats.get(file, 0) + 1

        # 按行号统计
        line_stats = {}
        for error in errors:
            line = error.get("line", 0)
            line_stats[line] = line_stats.get(line, 0) + 1

        # 最常见的错误类型
        type_counts = {}
        for error in errors:
            error_type = error.get("type", "UnknownError")
            type_counts[error_type] = type_counts.get(error_type, 0) + 1

        most_common_type = Counter(type_counts).most_common(1)

        return {
            "by_language": language_stats,
            "by_file": file_stats,
            "by_line": line_stats,
            "most_common_type": most_common_type[0][0] if most_common_type else None,
            "most_common_type_count": most_common_type[0][1] if most_common_type else 0
        }

    def _summarize_categories(self, categories: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        """
        汇总分类统计

        Args:
            categories: 分类结果

        Returns:
            汇总统计
        """
        summary = {}
        for category, type_counts in categories.items():
            if isinstance(type_counts, dict):
                summary[category] = sum(type_counts.values())
            else:
                summary[category] = type_counts

        return summary

    def get_error_report(self, analysis: Dict[str, Any]) -> str:
        """
        生成错误报告

        Args:
            analysis: 分析结果

        Returns:
            格式化的报告
        """
        lines = []
        lines.append("=" * 60)
        lines.append("错误消息分析报告")
        lines.append("=" * 60)
        lines.append(f"总错误数: {analysis['total']}")
        lines.append("")

        # 分类统计
        lines.append("分类统计:")
        for category, type_counts in sorted(analysis['categories'].items(), key=lambda x: sum(x[1].values()) if isinstance(x[1], dict) else x[1], reverse=True):
            count = sum(type_counts.values()) if isinstance(type_counts, dict) else type_counts
            lines.append(f"  {category}: {count}")
        lines.append("")

        # 严重程度
        lines.append("严重程度:")
        for severity, count in sorted(analysis['severities'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {severity}: {count}")
        lines.append("")

        # 关键词
        lines.append("高频关键词:")
        for keyword, count in analysis['keywords'].items():
            lines.append(f"  {keyword}: {count}")
        lines.append("")

        # 统计信息
        stats = analysis['statistics']
        lines.append("统计信息:")
        if stats.get('most_common_type'):
            lines.append(f"  最常见错误类型: {stats['most_common_type']} ({stats['most_common_type_count']} 次)")
        lines.append(f"  按语言分布: {stats.get('by_language', {})}")
        lines.append(f"  按文件分布: {stats.get('by_file', {})}")
        lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)


# 便捷函数
def analyze_errors(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    便捷函数：分析错误

    Args:
        errors: 错误列表

    Returns:
        分析结果
    """
    analyzer = ErrorAnalyzer()
    return analyzer.analyze_errors(errors)


def generate_error_report(errors: List[Dict[str, Any]]) -> str:
    """
    便捷函数：生成错误报告

    Args:
        errors: 错误列表

    Returns:
        格式化的报告
    """
    analyzer = ErrorAnalyzer()
    analysis = analyzer.analyze_errors(errors)
    return analyzer.get_error_report(analysis)