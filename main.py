"""
Error Message Poet - CLI 入口
"""
import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import click
from dotenv import load_dotenv
from error_collector import ErrorCollector, collect_errors
from poetry_generator import PoetryGenerator
from config import Config, validate_config, get_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 加载环境变量
load_dotenv()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Error Message Poet - 将系统错误消息转化为诗歌"""
    pass


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True), help='输入文件路径')
@click.option('--output', '-o', type=click.Path(), help='输出文件路径')
@click.option('--language', '-l', type=click.Choice(['python', 'javascript']), default='python', help='编程语言')
@click.option('--model', '-m', help='使用的模型')
@click.option('--template', '-t', type=click.Choice(['modern', 'classical', 'free']), default='modern', help='诗歌模板')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text', help='输出格式')
@click.option('--stdin', is_flag=True, help='从标准输入读取')
def convert(input: Optional[str], output: Optional[str], language: str, model: Optional[str],
            template: str, format: str, stdin: bool):
    """
    将错误消息转换为诗歌

    示例:
        error-poet convert --input errors.txt --output poems.txt
        echo "ZeroDivisionError: division by zero" | error-poet convert --stdin
    """
    # 验证配置
    if not validate_config():
        sys.exit(1)

    # 获取配置
    cfg = get_config()

    # 读取输入
    if stdin:
        content = sys.stdin.read()
    elif input:
        try:
            with open(input, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            click.echo(f"读取文件失败: {e}", err=True)
            sys.exit(1)
    else:
        click.echo("错误: 请提供 --input 或 --stdin 参数", err=True)
        sys.exit(1)

    # 收集错误
    logger.info(f"正在收集 {language} 错误...")
    collector = ErrorCollector()
    errors = collector.collect_from_string(content, language)

    if not errors:
        click.echo("未找到错误消息", err=True)
        sys.exit(1)

    click.echo(f"找到 {len(errors)} 个错误", err=True)

    # 生成诗歌
    click.echo("正在生成诗歌...", err=True)
    generator = PoetryGenerator({
        'OPENAI_API_KEY': cfg.get('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': cfg.get('ANTHROPIC_API_KEY'),
        'LOCAL_MODEL_URL': cfg.get('LOCAL_MODEL_URL'),
        'DEFAULT_MODEL': model or cfg.get('DEFAULT_MODEL')
    })

    poems = []
    for error in errors:
        try:
            poem = generator.generate_poem(
                error['message'],
                model=cfg.get('DEFAULT_MODEL'),
                template=template,
                language=language
            )
            poems.append({
                'error': error,
                'poem': poem
            })
        except Exception as e:
            logger.error(f"生成诗歌失败: {e}")
            click.echo(f"生成诗歌失败: {e}", err=True)
            poems.append({
                'error': error,
                'poem': f"生成失败: {str(e)}"
            })

    # 输出结果
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                if format == 'json':
                    json.dump(poems, f, ensure_ascii=False, indent=2)
                elif format == 'html':
                    f.write(_format_html(poems))
                else:
                    for item in poems:
                        f.write(f"错误: {item['error']['message']}\n")
                        f.write(f"诗歌: {item['poem']}\n")
                        f.write("-" * 50 + "\n")
            click.echo(f"结果已保存到 {output}", err=True)
        except Exception as e:
            click.echo(f"写入文件失败: {e}", err=True)
            sys.exit(1)
    else:
        if format == 'json':
            click.echo(json.dumps(poems, ensure_ascii=False, indent=2))
        elif format == 'html':
            click.echo(_format_html(poems))
        else:
            for item in poems:
                click.echo(f"\n错误: {item['error']['message']}")
                click.echo(f"诗歌: {item['poem']}")


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True), help='输入文件或目录')
@click.option('--output', '-o', type=click.Path(), help='输出文件路径')
@click.option('--language', '-l', type=click.Choice(['python', 'javascript']), default='python', help='编程语言')
@click.option('--model', '-m', help='使用的模型')
@click.option('--template', '-t', type=click.Choice(['modern', 'classical', 'free']), default='modern', help='诗歌模板')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text', help='输出格式')
def batch(input: Optional[str], output: Optional[str], language: str, model: Optional[str], template: str, format: str):
    """
    批量处理多个错误消息

    示例:
        error-poet batch --input ./errors --output poems.json
        error-poet batch --input ./errors --format html --output poems.html
    """
    # 验证配置
    if not validate_config():
        sys.exit(1)

    # 获取配置
    cfg = get_config()

    collector = ErrorCollector()

    if os.path.isfile(input):
        errors = collector.collect_from_file(input, language)
    elif os.path.isdir(input):
        # 处理目录中的所有文件
        errors = []
        file_count = 0
        for file_path in Path(input).rglob('*'):
            if file_path.is_file():
                try:
                    file_errors = collector.collect_from_file(str(file_path), language)
                    errors.extend(file_errors)
                    file_count += 1
                except Exception as e:
                    logger.error(f"处理文件 {file_path} 失败: {e}")
                    click.echo(f"处理文件 {file_path} 失败: {e}", err=True)
        click.echo(f"已处理 {file_count} 个文件", err=True)
    else:
        click.echo(f"错误: 输入路径不存在: {input}", err=True)
        sys.exit(1)

    if not errors:
        click.echo("未找到错误消息", err=True)
        sys.exit(1)

    click.echo(f"找到 {len(errors)} 个错误")

    generator = PoetryGenerator({
        'OPENAI_API_KEY': cfg.get('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': cfg.get('ANTHROPIC_API_KEY'),
        'LOCAL_MODEL_URL': cfg.get('LOCAL_MODEL_URL'),
        'DEFAULT_MODEL': model or cfg.get('DEFAULT_MODEL')
    })

    # 批量生成诗歌，带进度显示
    poems = []
    total = len(errors)
    click.echo(f"正在生成 {total} 首诗歌...", err=True)

    for idx, error in enumerate(errors, 1):
        try:
            poem = generator.generate_poem(
                error['message'],
                model=cfg.get('DEFAULT_MODEL'),
                template=template,
                language=language
            )
            poems.append({
                'error': error,
                'poem': poem
            })

            # 显示进度
            progress = (idx / total) * 100
            click.echo(f"进度: {idx}/{total} ({progress:.1f}%)", err=True)
        except Exception as e:
            logger.error(f"生成诗歌失败 [{idx}/{total}]: {e}")
            click.echo(f"生成诗歌失败 [{idx}/{total}]: {e}", err=True)
            poems.append({
                'error': error,
                'poem': f"生成失败: {str(e)}"
            })

    # 输出结果
    result = {
        'total': total,
        'poems': poems
    }

    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                if format == 'json':
                    json.dump(result, f, ensure_ascii=False, indent=2)
                elif format == 'html':
                    f.write(_format_html(result['poems']))
                else:
                    for item in result['poems']:
                        f.write(f"错误: {item['error']['message']}\n")
                        f.write(f"诗歌: {item['poem']}\n")
                        f.write("-" * 50 + "\n")
            click.echo(f"结果已保存到 {output}", err=True)
        except Exception as e:
            click.echo(f"写入文件失败: {e}", err=True)
            sys.exit(1)
    else:
        if format == 'json':
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        elif format == 'html':
            click.echo(_format_html(result['poems']))
        else:
            for item in result['poems']:
                click.echo(f"\n错误: {item['error']['message']}")
                click.echo(f"诗歌: {item['poem']}")
            click.echo(f"\n总计: {total} 首诗歌")


@cli.command()
@click.option('--language', '-l', type=click.Choice(['python', 'javascript']), default='python', help='编程语言')
def analyze(language: str):
    """
    分析错误消息特征

    示例:
        error-poet analyze --language python
    """
    # 从标准输入读取
    content = sys.stdin.read()

    collector = ErrorCollector()
    errors = collector.collect_from_string(content, language)

    if not errors:
        click.echo("未找到错误消息", err=True)
        sys.exit(1)

    summary = collector.get_error_summary(errors)

    click.echo("\n错误分析报告:")
    click.echo(f"总错误数: {summary['total']}")
    click.echo("\n错误类型分布:")
    for error_type, count in summary['types'].items():
        click.echo(f"  {error_type}: {count}")
    click.echo("\n编程语言分布:")
    for lang, count in summary['languages'].items():
        click.echo(f"  {lang}: {count}")


@cli.command()
def config():
    """显示配置信息"""
    cfg = get_config()
    cfg.print_config()


def _format_html(poems: List[Dict[str, Any]]) -> str:
    """格式化为 HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Error Message Poet</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .error { background: #f5f5f5; padding: 15px; margin: 20px 0; border-left: 4px solid #ff6b6b; }
            .poem { background: #e8f4f8; padding: 15px; margin: 20px 0; border-left: 4px solid #4ecdc4; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; }
        </style>
    </head>
    <body>
        <h1>Error Message Poet</h1>
    """

    for item in poems:
        html += f"""
        <div class="error">
            <h2>错误: {item['error']['message']}</h2>
            <p>类型: {item['error']['type']}</p>
            <p>文件: {item['error']['file']}:{item['error']['line']}</p>
        </div>
        <div class="poem">
            <h2>诗歌</h2>
            <p>{item['poem']}</p>
        </div>
        """

    html += """
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    cli()