"""
诗歌生成模块 - 使用 LLM 将错误消息转化为诗歌
"""
import os
from typing import Optional, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
import requests
import json
from cache_manager import CacheManager
from template_loader import TemplateLoader


class PoetryGenerator:
    """诗歌生成器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化诗歌生成器

        Args:
            config: 配置字典，包含 API keys 和模型设置
        """
        self.config = config or {}
        self.openai_key = self.config.get('OPENAI_API_KEY')
        self.anthropic_key = self.config.get('ANTHROPIC_API_KEY')
        self.local_url = self.config.get('LOCAL_MODEL_URL')
        self.default_model = self.config.get('DEFAULT_MODEL', 'gpt-3.5-turbo')
        self.enable_cache = self.config.get('ENABLE_CACHE', True)

        # 初始化客户端
        self.openai_client = None
        self.anthropic_client = None

        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)

        if self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)

        # 初始化缓存管理器
        self.cache_manager = CacheManager() if self.enable_cache else None

        # 初始化模板加载器
        self.template_loader = TemplateLoader()

        # 检测可用的模型
        self.available_models = self._detect_available_models()

    def _detect_available_models(self) -> Dict[str, str]:
        """
        检测可用的模型提供商

        Returns:
            可用模型字典，键为提供商名称，值为模型名称
        """
        available = {}

        # 检测 OpenAI
        if self.openai_client:
            available['openai'] = 'gpt-3.5-turbo'

        # 检测 Anthropic
        if self.anthropic_client:
            available['anthropic'] = 'claude-3-haiku-20240307'

        # 检测本地模型
        if self.local_url:
            available['local'] = self.default_model

        return available

    def get_available_models(self) -> Dict[str, str]:
        """
        获取可用模型列表

        Returns:
            可用模型字典
        """
        return self.available_models

    def generate_poem(
        self,
        error_message: str,
        model: Optional[str] = None,
        template: str = "modern",
        language: str = "python"
    ) -> str:
        """
        生成诗歌

        Args:
            error_message: 错误消息
            model: 使用的模型
            template: 诗歌模板
            language: 编程语言

        Returns:
            生成的诗歌
        """
        model = model or self.default_model

        # 检查缓存
        if self.cache_manager:
            cached_poem = self.cache_manager.get(
                error_message, model, template, language
            )
            if cached_poem:
                print(f"Cache hit for error: {error_message[:50]}...")
                return cached_poem

        # 选择 API
        if self.openai_client and 'gpt' in model.lower():
            poem = self._generate_with_openai(error_message, model, template, language)
        elif self.anthropic_client and 'claude' in model.lower():
            poem = self._generate_with_anthropic(error_message, model, template, language)
        elif self.local_url:
            poem = self._generate_with_local(error_message, model, template, language)
        else:
            raise ValueError("No valid LLM provider configured")

        # 保存到缓存
        if self.cache_manager:
            self.cache_manager.set(
                error_message, poem, model, template, language
            )

        return poem

    def _generate_with_openai(
        self,
        error_message: str,
        model: str,
        template: str,
        language: str
    ) -> str:
        """使用 OpenAI 生成诗歌"""
        prompt = self._build_prompt(error_message, template, language)

        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个将技术错误转化为诗歌的诗人。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    def _generate_with_anthropic(
        self,
        error_message: str,
        model: str,
        template: str,
        language: str
    ) -> str:
        """使用 Anthropic 生成诗歌"""
        prompt = self._build_prompt(error_message, template, language)

        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=500,
            temperature=0.8,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text.strip()

    def _generate_with_local(
        self,
        error_message: str,
        model: str,
        template: str,
        language: str
    ) -> str:
        """使用本地模型生成诗歌"""
        prompt = self._build_prompt(error_message, template, language)

        response = requests.post(
            f"{self.local_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json().get('response', '').strip()

    def _build_prompt(
        self,
        error_message: str,
        template: str,
        language: str
    ) -> str:
        """构建生成诗歌的提示词"""
        # 尝试从模板加载器获取模板
        template_text = self.template_loader.get_template(template)

        if template_text:
            return template_text.format(error_message=error_message)
        else:
            # 如果模板不存在，使用默认模板
            templates = {
                "modern": """将以下错误消息转化为现代诗：

{error_message}

要求：
- 保持错误的核心含义
- 使用诗意的语言
- 可以使用隐喻和象征
- 每行不超过 20 字
- 共 4-8 行""",
                "classical": """将以下错误消息转化为古体诗（七言绝句）：

{error_message}

要求：
- 使用七言句式
- 押韵
- 保持错误的核心含义
- 共 4 行""",
                "free": """将以下错误消息转化为自由诗：

{error_message}

要求：
- 自由的格式和节奏
- 可以使用分行、换行
- 保持错误的核心含义
- 表达情感和意境"""
            }

            template_text = templates.get(template, templates["modern"])
            return template_text.format(error_message=error_message)

    def generate_batch(
        self,
        error_messages: list,
        model: Optional[str] = None,
        template: str = "modern"
    ) -> list:
        """
        批量生成诗歌

        Args:
            error_messages: 错误消息列表
            model: 使用的模型
            template: 诗歌模板

        Returns:
            诗歌列表
        """
        poems = []
        for error in error_messages:
            poem = self.generate_poem(error, model, template)
            poems.append(poem)
        return poems