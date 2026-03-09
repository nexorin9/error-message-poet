"""
模板加载系统 - 加载和管理诗歌模板
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class TemplateLoader:
    """模板加载器"""

    def __init__(self, templates_dir: str = "./templates"):
        """
        初始化模板加载器

        Args:
            templates_dir: 模板目录路径
        """
        self.templates_dir = Path(templates_dir)
        self.templates = {}

        # 加载所有模板
        self._load_all_templates()

    def _load_all_templates(self):
        """加载所有模板"""
        if not self.templates_dir.exists():
            return

        for template_file in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                    template_name = template_file.stem
                    self.templates[template_name] = template_content
            except Exception as e:
                print(f"加载模板 {template_file} 失败: {e}")

    def get_template(self, template_name: str) -> Optional[str]:
        """
        获取模板内容

        Args:
            template_name: 模板名称

        Returns:
            模板内容，如果不存在则返回 None
        """
        return self.templates.get(template_name)

    def list_templates(self) -> list:
        """
        列出所有可用模板

        Returns:
            模板名称列表
        """
        return list(self.templates.keys())

    def format_template(self, template: str, error_message: str) -> str:
        """
        格式化模板，替换变量

        Args:
            template: 模板内容
            error_message: 错误消息

        Returns:
            格式化后的模板
        """
        return template.format(error_message=error_message)

    def get_prompt(self, template_name: str, error_message: str) -> str:
        """
        获取格式化后的提示词

        Args:
            template_name: 模板名称
            error_message: 错误消息

        Returns:
            格式化后的提示词
        """
        template = self.get_template(template_name)
        if template is None:
            # 如果模板不存在，使用默认模板
            template = self.get_template("modern")

        return self.format_template(template, error_message)


# 全局模板加载器实例
template_loader = TemplateLoader()


def get_template_loader() -> TemplateLoader:
    """获取模板加载器实例"""
    return template_loader


def get_template(template_name: str, error_message: str) -> str:
    """
    便捷函数：获取格式化后的提示词

    Args:
        template_name: 模板名称
        error_message: 错误消息

    Returns:
        格式化后的提示词
    """
    return template_loader.get_prompt(template_name, error_message)