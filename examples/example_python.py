#!/usr/bin/env python3
"""
Error Message Poet - Python 示例
将系统错误消息转化为诗歌
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from error_collector import collect_errors_from_traceback
from poetry_generator import PoetryGenerator
from poetry_quality import evaluate_poetry, generate_quality_report


def example_single_conversion():
    """示例 1: 转换单个错误消息"""
    print("=" * 60)
    print("示例 1: 转换单个错误消息")
    print("=" * 60)

    # 模拟一个 Python 错误
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        error = collect_errors_from_traceback(e)

        print(f"\n原始错误消息:\n{error['message']}\n")

        # 使用默认配置生成诗歌
        generator = PoetryGenerator()
        poem = generator.generate(error)

        print(f"生成的诗歌:\n{poem}\n")

        # 评估诗歌质量
        quality = evaluate_poetry(poem, error['message'])
        print(f"诗歌质量评估:")
        print(f"  综合得分: {quality['score']}/100")
        print(f"  流畅度: {quality['metrics']['fluency']}/100")
        print(f"  诗意: {quality['metrics']['poeticness']}/100")
        print(f"  准确性: {quality['metrics']['accuracy']}/100")
        print(f"  连贯性: {quality['metrics']['coherence']}/100")
        print(f"\n详细反馈:\n{quality['feedback']}")


def example_batch_conversion():
    """示例 2: 批量转换错误消息"""
    print("\n" + "=" * 60)
    print("示例 2: 批量转换错误消息")
    print("=" * 60)

    # 模拟多个错误
    errors = [
        {
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "language": "python"
        },
        {
            "type": "FileNotFoundError",
            "message": "file not found: /path/to/file.txt",
            "language": "python"
        },
        {
            "type": "ConnectionError",
            "message": "connection timeout",
            "language": "python"
        }
    ]

    generator = PoetryGenerator()

    print(f"\n共 {len(errors)} 个错误:\n")

    for i, error in enumerate(errors, 1):
        print(f"[{i}] {error['type']}: {error['message']}")
        poem = generator.generate(error)
        print(f"    → {poem}\n")


def example_with_templates():
    """示例 3: 使用自定义模板"""
    print("\n" + "=" * 60)
    print("示例 3: 使用自定义模板")
    print("=" * 60)

    error = {
        "type": "TimeoutError",
        "message": "request timeout after 30 seconds",
        "language": "python"
    }

    generator = PoetryGenerator()

    # 使用现代诗模板
    print("\n使用现代诗模板:")
    poem = generator.generate(error, template="modern")
    print(poem)

    # 使用古体诗模板
    print("\n使用古体诗模板:")
    poem = generator.generate(error, template="classical")
    print(poem)

    # 使用自由诗模板
    print("\n使用自由诗模板:")
    poem = generator.generate(error, template="free")
    print(poem)


def example_quality_report():
    """示例 4: 生成质量报告"""
    print("\n" + "=" * 60)
    print("示例 4: 生成质量报告")
    print("=" * 60)

    error = {
        "type": "DatabaseError",
        "message": "database connection failed",
        "language": "python"
    }

    generator = PoetryGenerator()
    poem = generator.generate(error)

    print(f"\n原始错误: {error['message']}")
    print(f"\n生成的诗歌:\n{poem}\n")

    # 生成详细质量报告
    report = generate_quality_report(poem, error['message'])
    print(report)


def example_error_analysis():
    """示例 5: 错误消息分析"""
    print("\n" + "=" * 60)
    print("示例 5: 错误消息分析")
    print("=" * 60)

    from error_analyzer import analyze_errors, generate_error_report

    errors = [
        {
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "language": "python"
        },
        {
            "type": "FileNotFoundError",
            "message": "file not found: /path/to/file.txt",
            "language": "python"
        },
        {
            "type": "ConnectionError",
            "message": "connection timeout",
            "language": "python"
        }
    ]

    # 分析错误
    analysis = analyze_errors(errors)

    # 生成报告
    report = generate_error_report(errors)
    print(report)


def main():
    """主函数"""
    print("\nError Message Poet - Python 示例\n")

    # 检查是否提供了示例编号
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        if example_num == 1:
            example_single_conversion()
        elif example_num == 2:
            example_batch_conversion()
        elif example_num == 3:
            example_with_templates()
        elif example_num == 4:
            example_quality_report()
        elif example_num == 5:
            example_error_analysis()
        else:
            print(f"未知示例编号: {example_num}")
            print("可用示例: 1-5")
    else:
        # 运行所有示例
        example_single_conversion()
        example_batch_conversion()
        example_with_templates()
        example_quality_report()
        example_error_analysis()

    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()