"""
配置管理模块 - 环境变量和配置验证
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import click


# 加载环境变量
load_dotenv()


class Config:
    """配置管理器"""

    def __init__(self):
        """初始化配置"""
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        config = {
            # API Keys
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),

            # Local Model
            'LOCAL_MODEL_URL': os.getenv('LOCAL_MODEL_URL'),

            # Default Settings
            'DEFAULT_MODEL': os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo'),
            'CACHE_DIR': os.getenv('CACHE_DIR', './cache'),
            'OUTPUT_FORMAT': os.getenv('OUTPUT_FORMAT', 'text'),
            'ENABLE_CACHE': os.getenv('ENABLE_CACHE', 'true').lower() == 'true',
            'TEMPLATE': os.getenv('TEMPLATE', 'modern'),
            'BATCH_CONCURRENCY': int(os.getenv('BATCH_CONCURRENCY', '5')),
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO')
        }

        return config

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def validate(self) -> Dict[str, str]:
        """
        验证配置

        Returns:
            验证结果字典，包含错误信息
        """
        errors = {}

        # 验证 API Keys（至少需要一个，除非使用本地模型）
        has_openai = bool(self._config.get('OPENAI_API_KEY'))
        has_anthropic = bool(self._config.get('ANTHROPIC_API_KEY'))
        has_local = bool(self._config.get('LOCAL_MODEL_URL'))

        if not has_openai and not has_anthropic and not has_local:
            errors['API_KEYS'] = '至少需要配置一个 API key (OPENAI_API_KEY 或 ANTHROPIC_API_KEY)，或配置 LOCAL_MODEL_URL 使用本地模型'

        # 验证本地模型 URL
        if self._config.get('LOCAL_MODEL_URL') and not has_local:
            errors['LOCAL_MODEL'] = 'LOCAL_MODEL_URL 配置无效'

        # 验证缓存目录
        cache_dir = self._config.get('CACHE_DIR')
        if cache_dir:
            try:
                os.makedirs(cache_dir, exist_ok=True)
            except Exception as e:
                errors['CACHE_DIR'] = f"无法创建缓存目录: {e}"

        # 验证输出格式
        output_format = self._config.get('OUTPUT_FORMAT')
        if output_format not in ['text', 'json', 'html']:
            errors['OUTPUT_FORMAT'] = f"无效的输出格式: {output_format}"

        # 验证模板
        template = self._config.get('TEMPLATE')
        if template not in ['modern', 'classical', 'free']:
            errors['TEMPLATE'] = f"无效的模板: {template}"

        # 验证并发数
        concurrency = self._config.get('BATCH_CONCURRENCY')
        if concurrency < 1 or concurrency > 20:
            errors['BATCH_CONCURRENCY'] = f"并发数必须在 1-20 之间: {concurrency}"

        return errors

    def print_config(self):
        """打印配置信息（不显示敏感信息）"""
        config_info = {
            'DEFAULT_MODEL': self._config.get('DEFAULT_MODEL'),
            'CACHE_DIR': self._config.get('CACHE_DIR'),
            'OUTPUT_FORMAT': self._config.get('OUTPUT_FORMAT'),
            'ENABLE_CACHE': self._config.get('ENABLE_CACHE'),
            'TEMPLATE': self._config.get('TEMPLATE'),
            'BATCH_CONCURRENCY': self._config.get('BATCH_CONCURRENCY'),
            'LOG_LEVEL': self._config.get('LOG_LEVEL')
        }

        click.echo("配置信息:")
        for key, value in config_info.items():
            click.echo(f"  {key}: {value}")

        # 显示 API Keys 状态
        has_openai = bool(self._config.get('OPENAI_API_KEY'))
        has_anthropic = bool(self._config.get('ANTHROPIC_API_KEY'))
        has_local = bool(self._config.get('LOCAL_MODEL_URL'))

        click.echo("\nAPI 提供商:")
        if has_openai:
            click.echo("  ✓ OpenAI")
        if has_anthropic:
            click.echo("  ✓ Anthropic")
        if has_local:
            click.echo("  ✓ Local Model")

        if not has_openai and not has_anthropic and not has_local:
            click.echo("  ✗ 未配置任何 API 提供商")


# 全局配置实例
config = Config()


def validate_config():
    """验证配置并显示错误"""
    errors = config.validate()

    if errors:
        click.echo("\n配置错误:", err=True)
        for key, error in errors.items():
            click.echo(f"  {key}: {error}", err=True)
        return False

    return True


def get_config() -> Config:
    """获取配置实例"""
    return config