"""
诗歌质量评估模块测试
"""
import pytest
from poetry_quality import PoetryQualityEvaluator, evaluate_poetry, generate_quality_report


class TestPoetryQualityEvaluator:
    """诗歌质量评估器测试"""

    def test_evaluate_empty_poem(self):
        """测试空诗歌"""
        evaluator = PoetryQualityEvaluator()
        result = evaluator.evaluate("")

        assert result["score"] == 0
        assert result["metrics"]["fluency"] == 0
        assert result["metrics"]["poeticness"] == 0
        assert "feedback" in result

    def test_evaluate_fluency(self):
        """测试流畅度评估"""
        evaluator = PoetryQualityEvaluator()

        # 流畅的诗歌
        fluent_poem = "风轻轻吹过，云在天上飘。"
        result = evaluator.evaluate(fluent_poem)

        assert result["metrics"]["fluency"] > 50

        # 不流畅的诗歌（重复词多）
        repetitive_poem = "风风风，云云云，风风风，云云云。"
        result = evaluator.evaluate(repetitive_poem)

        assert result["metrics"]["fluency"] < 95

    def test_evaluate_poeticness(self):
        """测试诗意评估"""
        evaluator = PoetryQualityEvaluator()

        # 有意象的诗歌
        poetic_poem = "月光洒在湖面，如梦似幻。"
        result = evaluator.evaluate(poetic_poem)

        assert result["metrics"]["poeticness"] > 0

        # 无意象的诗歌
        plain_poem = "这是一个错误。"
        result = evaluator.evaluate(plain_poem)

        assert result["metrics"]["poeticness"] < 10

    def test_evaluate_accuracy(self):
        """测试准确性评估"""
        evaluator = PoetryQualityEvaluator()

        # 包含错误关键词的诗歌
        poem_with_keywords = "连接超时，网络无法访问。"
        error_msg = "Connection timeout occurred"
        result = evaluator.evaluate(poem_with_keywords, error_msg)

        assert result["metrics"]["accuracy"] > 5

        # 不包含错误关键词的诗歌
        poem_without_keywords = "风轻轻吹过，云在天上飘。"
        result = evaluator.evaluate(poem_without_keywords, error_msg)

        assert result["metrics"]["accuracy"] < 15

    def test_evaluate_coherence(self):
        """测试连贯性评估"""
        evaluator = PoetryQualityEvaluator()

        # 连贯的诗歌
        coherent_poem = "月光洒在湖面，如梦似幻。\n\n风轻轻吹过，云在天上飘。"
        result = evaluator.evaluate(coherent_poem)

        assert result["metrics"]["coherence"] > 40

        # 不连贯的诗歌（重复词多）
        incoherent_poem = "风风风，云云云，风风风，云云云。"
        result = evaluator.evaluate(incoherent_poem)

        assert result["metrics"]["coherence"] < 32

    def test_generate_feedback(self):
        """测试反馈生成"""
        evaluator = PoetryQualityEvaluator()

        # 高质量诗歌
        high_quality_poem = "月光洒在湖面，如梦似幻。\n\n风轻轻吹过，云在天上飘。"
        result = evaluator.evaluate(high_quality_poem)

        feedback = result["feedback"]
        assert "流畅度" in feedback
        assert "诗意" in feedback
        assert "准确性" in feedback
        assert "连贯性" in feedback

    def test_evaluate_with_error_message(self):
        """测试带错误消息的评估"""
        evaluator = PoetryQualityEvaluator()

        poem = "数据库连接失败，请检查配置。"
        error_msg = "Database connection failed"

        result = evaluator.evaluate(poem, error_msg)

        assert "score" in result
        assert "metrics" in result
        assert "feedback" in result
        assert result["metrics"]["accuracy"] > 0.5

    def test_evaluate_without_error_message(self):
        """测试不带错误消息的评估"""
        evaluator = PoetryQualityEvaluator()

        poem = "月光洒在湖面，如梦似幻。"
        result = evaluator.evaluate(poem)

        assert "score" in result
        assert result["metrics"]["accuracy"] == 50  # 默认值

    def test_evaluate_rhyme(self):
        """测试押韵检查"""
        evaluator = PoetryQualityEvaluator()

        # 有押韵的诗歌
        rhyming_poem = "月光洒在湖面，如梦似幻。\n\n风轻轻吹过，云在天上飘。"
        result = evaluator.evaluate(rhyming_poem)

        assert result["metrics"]["poeticness"] > 0

        # 无押韵的诗歌
        non_rhyming_poem = "月光洒在湖面，如梦似幻。\n\n风轻轻吹过，云在天上飞。"
        result = evaluator.evaluate(non_rhyming_poem)

        assert result["metrics"]["poeticness"] < 8


class TestConvenienceFunctions:
    """便捷函数测试"""

    def test_evaluate_poetry_function(self):
        """测试 evaluate_poetry 便捷函数"""
        poem = "月光洒在湖面，如梦似幻。"
        result = evaluate_poetry(poem)

        assert "score" in result
        assert "metrics" in result

    def test_generate_quality_report_function(self):
        """测试 generate_quality_report 便捷函数"""
        poem = "月光洒在湖面，如梦似幻。"
        report = generate_quality_report(poem)

        assert "诗歌质量评估报告" in report
        assert "综合得分" in report
        assert "各维度得分" in report
        assert "详细反馈" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])