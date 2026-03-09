"""
诗歌质量评估模块 - 评估生成诗歌的质量
"""
import re
from typing import List, Dict, Any, Tuple
from collections import Counter


class PoetryQualityEvaluator:
    """诗歌质量评估器"""

    def __init__(self):
        """初始化评估器"""
        self.metrics = {
            "fluency": 0,
            "poeticness": 0,
            "accuracy": 0,
            "coherence": 0
        }

    def evaluate(self, poem: str, error_message: str = "") -> Dict[str, Any]:
        """
        评估诗歌质量

        Args:
            poem: 诗歌内容
            error_message: 原始错误消息（用于评估准确性）

        Returns:
            评估结果
        """
        if not poem or not poem.strip():
            return {
                "score": 0,
                "metrics": self.metrics,
                "feedback": "Empty poem"
            }

        # 计算各维度得分
        fluency_score = self._evaluate_fluency(poem)
        poeticness_score = self._evaluate_poeticness(poem)
        accuracy_score = self._evaluate_accuracy(poem, error_message) if error_message else 0.5
        coherence_score = self._evaluate_coherence(poem)

        # 计算综合得分
        total_score = (fluency_score + poeticness_score + accuracy_score + coherence_score) / 4

        # 生成反馈
        feedback = self._generate_feedback(
            fluency_score, poeticness_score, accuracy_score, coherence_score
        )

        return {
            "score": round(total_score * 100, 2),
            "metrics": {
                "fluency": round(fluency_score * 100, 2),
                "poeticness": round(poeticness_score * 100, 2),
                "accuracy": round(accuracy_score * 100, 2),
                "coherence": round(coherence_score * 100, 2)
            },
            "feedback": feedback
        }

    def _evaluate_fluency(self, poem: str) -> float:
        """
        评估流畅度

        Args:
            poem: 诗歌内容

        Returns:
            流畅度得分 (0-1)
        """
        # 检查句子长度分布
        sentences = re.split(r'[.!?。！？]', poem)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.0

        # 计算句子长度方差（越均匀越好）
        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

        # 长度方差越小，流畅度越高
        fluency = max(0, 1 - variance / (avg_length ** 2 + 1))

        # 检查停用词比例（停用词越少越好）
        stop_words = {"的", "了", "在", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "这", "那", "有", "没有", "和", "与", "或", "但是", "而且", "所以", "因为"}
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', poem)
        stop_word_ratio = sum(1 for w in words if w in stop_words) / len(words) if words else 0

        fluency -= stop_word_ratio * 0.3

        # 重复词惩罚
        word_counts = Counter(words)
        total_words = len(words)
        unique_words = len(word_counts)
        repetition_ratio = (total_words - unique_words) / total_words
        fluency -= repetition_ratio * 0.4

        return max(0, min(1, fluency))

    def _evaluate_poeticness(self, poem: str) -> float:
        """
        评估诗意

        Args:
            poem: 诗歌内容

        Returns:
            诗意得分 (0-1)
        """
        # 检查意象词（形容词、动词、名词）
        adjectives = re.findall(r'[\u4e00-\u9fa5]{2,}', poem)
        if not adjectives:
            return 0.3

        # 检查意象词数量
        imagery_keywords = {
            "风", "雨", "云", "月", "花", "鸟", "山", "水", "海", "天",
            "梦", "心", "情", "爱", "恨", "泪", "笑", "歌", "舞", "诗",
            "夜", "晨", "光", "影", "色", "香", "味", "声", "静", "动"
        }
        imagery_count = sum(1 for word in adjectives if word in imagery_keywords)

        # 检查修辞手法
        rhetorical_patterns = {
            "比喻": [r'像', r'如', r'若', r'似'],
            "拟人": [r'的', r'化', r'成'],
            "排比": [r'又', r'也', r'还'],
            "夸张": [r'最', r'极', r'无比']
        }

        rhetorical_score = 0
        for technique, patterns in rhetorical_patterns.items():
            count = sum(1 for pattern in patterns if pattern in poem)
            rhetorical_score += count * 0.1

        # 检查韵律（简单检查押韵）
        rhyme_score = self._check_rhyme(poem)

        # 综合评分
        poeticness = (
            (imagery_count / len(adjectives)) * 0.4 +
            rhetorical_score * 0.3 +
            rhyme_score * 0.3
        )

        return max(0, min(1, poeticness))

    def _check_rhyme(self, poem: str) -> float:
        """
        检查押韵

        Args:
            poem: 诗歌内容

        Returns:
            押韵得分 (0-1)
        """
        # 简单押韵检查：检查句尾韵母
        sentences = re.split(r'[.!?。！？]', poem)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return 0.0

        # 提取句尾韵母
        rhymes = []
        for sentence in sentences[-3:]:  # 检查最后 3 句
            last_word = re.search(r'[\u4e00-\u9fa5]{2,}$', sentence)
            if last_word:
                rhyme = last_word.group(0)[-2:]  # 取最后两个字
                rhymes.append(rhyme)

        if not rhymes:
            return 0.0

        # 检查韵母是否相同
        rhyme_count = sum(1 for i in range(1, len(rhymes)) if rhymes[i] == rhymes[0])

        return min(1.0, rhyme_count / len(rhymes))

    def _evaluate_accuracy(self, poem: str, error_message: str) -> float:
        """
        评估准确性（诗歌是否反映了错误消息）

        Args:
            poem: 诗歌内容
            error_message: 原始错误消息

        Returns:
            准确性得分 (0-1)
        """
        if not error_message:
            return 0.5

        # 提取错误消息中的关键词
        error_words = re.findall(r'\b[a-z]{3,}\b', error_message.lower())
        error_words = [w for w in error_words if len(w) > 3]

        if not error_words:
            return 0.5

        # 检查诗歌中是否包含错误关键词
        poem_lower = poem.lower()
        matched_words = sum(1 for word in error_words if word in poem_lower)

        # 计算匹配率
        accuracy = matched_words / len(error_words)

        # 惩罚不相关的诗歌
        if accuracy == 0:
            accuracy = 0.1

        return max(0, min(1, accuracy))

    def _evaluate_coherence(self, poem: str) -> float:
        """
        评估连贯性

        Args:
            poem: 诗歌内容

        Returns:
            连贯性得分 (0-1)
        """
        # 检查重复词
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', poem)
        if not words:
            return 0.0

        word_counts = Counter(words)
        total_words = len(words)
        unique_words = len(word_counts)

        # 重复率越低，连贯性越高
        repetition_ratio = (total_words - unique_words) / total_words

        # 检查段落结构
        paragraphs = re.split(r'\n\s*\n', poem)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        if len(paragraphs) < 2:
            return 0.3

        # 段落数量适中
        coherence = max(0, 1 - repetition_ratio * 0.6)

        return max(0, min(1, coherence))

    def _generate_feedback(
        self,
        fluency: float,
        poeticness: float,
        accuracy: float,
        coherence: float
    ) -> str:
        """
        生成反馈

        Args:
            fluency: 流畅度得分
            poeticness: 诗意得分
            accuracy: 准确性得分
            coherence: 连贯性得分

        Returns:
            反馈文本
        """
        feedback_lines = []

        if fluency > 0.7:
            feedback_lines.append("✓ 流畅度优秀，读起来很自然")
        elif fluency > 0.5:
            feedback_lines.append("○ 流畅度良好，可以进一步优化")
        else:
            feedback_lines.append("✗ 流畅度有待提高，建议检查句子结构")

        if poeticness > 0.7:
            feedback_lines.append("✓ 诗意浓厚，意象丰富")
        elif poeticness > 0.5:
            feedback_lines.append("○ 诗意尚可，可以增加更多意象")
        else:
            feedback_lines.append("✗ 诗意不足，建议使用更多修辞手法")

        if accuracy > 0.7:
            feedback_lines.append("✓ 准确性高，很好地反映了错误消息")
        elif accuracy > 0.5:
            feedback_lines.append("○ 准确性一般，可以更贴近错误消息")
        else:
            feedback_lines.append("✗ 准确性较低，建议更准确地表达错误信息")

        if coherence > 0.7:
            feedback_lines.append("✓ 连贯性好，结构清晰")
        elif coherence > 0.5:
            feedback_lines.append("○ 连贯性尚可，可以优化段落结构")
        else:
            feedback_lines.append("✗ 连贯性不足，建议检查重复词")

        return "\n".join(feedback_lines)


# 便捷函数
def evaluate_poetry(poem: str, error_message: str = "") -> Dict[str, Any]:
    """
    便捷函数：评估诗歌质量

    Args:
        poem: 诗歌内容
        error_message: 原始错误消息

    Returns:
        评估结果
    """
    evaluator = PoetryQualityEvaluator()
    return evaluator.evaluate(poem, error_message)


def generate_quality_report(poem: str, error_message: str = "") -> str:
    """
    便捷函数：生成质量报告

    Args:
        poem: 诗歌内容
        error_message: 原始错误消息

    Returns:
        格式化的报告
    """
    evaluator = PoetryQualityEvaluator()
    result = evaluator.evaluate(poem, error_message)

    lines = []
    lines.append("=" * 60)
    lines.append("诗歌质量评估报告")
    lines.append("=" * 60)
    lines.append(f"综合得分: {result['score']}/100")
    lines.append("")

    lines.append("各维度得分:")
    for metric, score in result['metrics'].items():
        lines.append(f"  {metric}: {score}/100")
    lines.append("")

    lines.append("详细反馈:")
    lines.append(result['feedback'])
    lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)