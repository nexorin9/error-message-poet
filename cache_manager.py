"""
缓存管理模块 - 实现诗歌生成结果的缓存
"""
import os
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class CacheManager:
    """缓存管理器"""

    def __init__(self, cache_dir: str = "cache"):
        """
        初始化缓存管理器

        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = cache_dir
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_cache_key(
        self,
        error_message: str,
        model: str,
        template: str,
        language: str
    ) -> str:
        """
        生成缓存键

        Args:
            error_message: 错误消息
            model: 使用的模型
            template: 诗歌模板
            language: 编程语言

        Returns:
            缓存键（MD5 哈希）
        """
        # 创建缓存键的字符串表示
        cache_string = f"{error_message}|{model}|{template}|{language}"
        # 使用 MD5 生成哈希键
        cache_key = hashlib.md5(cache_string.encode('utf-8')).hexdigest()
        return cache_key

    def _get_cache_file_path(self, cache_key: str) -> str:
        """
        获取缓存文件路径

        Args:
            cache_key: 缓存键

        Returns:
            缓存文件路径
        """
        return os.path.join(self.cache_dir, f"{cache_key}.json")

    def _load_cache_entry(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        加载缓存条目

        Args:
            cache_key: 缓存键

        Returns:
            缓存条目，如果不存在则返回 None
        """
        cache_file = self._get_cache_file_path(cache_key)

        if not os.path.exists(cache_file):
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                entry = json.load(f)

            # 检查缓存是否过期（默认 24 小时）
            if 'timestamp' in entry:
                timestamp = datetime.fromisoformat(entry['timestamp'])
                if datetime.now() - timestamp > timedelta(hours=24):
                    # 缓存过期，删除
                    self._delete_cache_entry(cache_key)
                    return None

            return entry
        except (json.JSONDecodeError, IOError):
            return None

    def _save_cache_entry(self, cache_key: str, poem: str):
        """
        保存缓存条目

        Args:
            cache_key: 缓存键
            poem: 生成的诗歌
        """
        cache_file = self._get_cache_file_path(cache_key)

        entry = {
            'poem': poem,
            'timestamp': datetime.now().isoformat(),
            'model': cache_key[:8]  # 简化存储，只存部分信息
        }

        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(entry, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Failed to save cache entry: {e}")

    def get(
        self,
        error_message: str,
        model: str,
        template: str,
        language: str
    ) -> Optional[str]:
        """
        获取缓存的诗歌

        Args:
            error_message: 错误消息
            model: 使用的模型
            template: 诗歌模板
            language: 编程语言

        Returns:
            缓存的诗歌，如果不存在则返回 None
        """
        cache_key = self._generate_cache_key(error_message, model, template, language)
        entry = self._load_cache_entry(cache_key)

        if entry:
            return entry.get('poem')
        return None

    def set(
        self,
        error_message: str,
        poem: str,
        model: str,
        template: str,
        language: str
    ):
        """
        设置缓存

        Args:
            error_message: 错误消息
            poem: 生成的诗歌
            model: 使用的模型
            template: 诗歌模板
            language: 编程语言
        """
        cache_key = self._generate_cache_key(error_message, model, template, language)
        self._save_cache_entry(cache_key, poem)

    def delete(self, error_message: str, model: str, template: str, language: str):
        """
        删除缓存

        Args:
            error_message: 错误消息
            model: 使用的模型
            template: 诗歌模板
            language: 编程语言
        """
        cache_key = self._generate_cache_key(error_message, model, template, language)
        self._delete_cache_entry(cache_key)

    def _delete_cache_entry(self, cache_key: str):
        """
        删除单个缓存条目

        Args:
            cache_key: 缓存键
        """
        cache_file = self._get_cache_file_path(cache_key)

        try:
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except IOError as e:
            print(f"Warning: Failed to delete cache entry: {e}")

    def clear_all(self):
        """清空所有缓存"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    cache_file = os.path.join(self.cache_dir, filename)
                    os.remove(cache_file)
            print(f"Cache cleared: {self.cache_dir}")
        except IOError as e:
            print(f"Warning: Failed to clear cache: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            缓存统计信息
        """
        cache_files = [
            f for f in os.listdir(self.cache_dir)
            if f.endswith('.json')
        ]

        total_size = 0
        for filename in cache_files:
            cache_file = os.path.join(self.cache_dir, filename)
            total_size += os.path.getsize(cache_file)

        return {
            'total_entries': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': self.cache_dir
        }

    def cleanup_expired(self):
        """清理过期的缓存"""
        cleaned = 0

        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                cache_key = filename[:-5]  # 去掉 .json 后缀
                entry = self._load_cache_entry(cache_key)

                if entry is None:
                    cleaned += 1

        if cleaned > 0:
            print(f"Cleaned up {cleaned} expired cache entries")

        return cleaned