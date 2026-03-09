"""
缓存管理器单元测试
"""
import os
import json
import pytest
from datetime import datetime, timedelta
from cache_manager import CacheManager


class TestCacheManager:
    """缓存管理器测试类"""

    @pytest.fixture
    def cache_manager(self):
        """创建缓存管理器实例"""
        # 使用临时目录进行测试
        import tempfile
        temp_dir = tempfile.mkdtemp()
        manager = CacheManager(cache_dir=temp_dir)
        yield manager
        # 清理
        import shutil
        shutil.rmtree(temp_dir)

    def test_cache_key_generation(self, cache_manager):
        """测试缓存键生成"""
        error_message = "File not found: test.py"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        cache_key = cache_manager._generate_cache_key(
            error_message, model, template, language
        )

        # 验证缓存键是 MD5 哈希
        assert len(cache_key) == 32  # MD5 哈希长度
        assert cache_key.isalnum()

    def test_cache_key_consistency(self, cache_manager):
        """测试缓存键的一致性"""
        error_message = "File not found: test.py"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        key1 = cache_manager._generate_cache_key(
            error_message, model, template, language
        )
        key2 = cache_manager._generate_cache_key(
            error_message, model, template, language
        )

        assert key1 == key2

    def test_cache_set_and_get(self, cache_manager):
        """测试缓存设置和获取"""
        error_message = "File not found: test.py"
        poem = "在代码的荒原上，\n文件迷失了方向，\n找不到它的归宿。"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 设置缓存
        cache_manager.set(error_message, poem, model, template, language)

        # 获取缓存
        retrieved_poem = cache_manager.get(error_message, model, template, language)

        assert retrieved_poem == poem

    def test_cache_miss(self, cache_manager):
        """测试缓存未命中"""
        error_message = "File not found: test.py"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 获取不存在的缓存
        retrieved_poem = cache_manager.get(error_message, model, template, language)

        assert retrieved_poem is None

    def test_cache_delete(self, cache_manager):
        """测试缓存删除"""
        error_message = "File not found: test.py"
        poem = "在代码的荒原上，\n文件迷失了方向，\n找不到它的归宿。"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 设置缓存
        cache_manager.set(error_message, poem, model, template, language)

        # 删除缓存
        cache_manager.delete(error_message, model, template, language)

        # 验证缓存已删除
        retrieved_poem = cache_manager.get(error_message, model, template, language)
        assert retrieved_poem is None

    def test_cache_file_structure(self, cache_manager):
        """测试缓存文件结构"""
        error_message = "File not found: test.py"
        poem = "在代码的荒原上，\n文件迷失了方向，\n找不到它的归宿。"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 设置缓存
        cache_manager.set(error_message, poem, model, template, language)

        # 检查缓存文件是否存在
        cache_key = cache_manager._generate_cache_key(
            error_message, model, template, language
        )
        cache_file = cache_manager._get_cache_file_path(cache_key)

        assert os.path.exists(cache_file)

        # 检查缓存文件内容
        with open(cache_file, 'r', encoding='utf-8') as f:
            entry = json.load(f)

        assert 'poem' in entry
        assert entry['poem'] == poem
        assert 'timestamp' in entry

    def test_cache_stats(self, cache_manager):
        """测试缓存统计"""
        error_message = "File not found: test.py"
        poem = "在代码的荒原上，\n文件迷失了方向，\n找不到它的归宿。"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 设置缓存
        cache_manager.set(error_message, poem, model, template, language)

        # 获取统计信息
        stats = cache_manager.get_cache_stats()

        assert stats['total_entries'] == 1
        assert stats['total_size_bytes'] > 0
        # total_size_mb 可能为 0.0，这是正常的，因为文件可能很小
        assert stats['total_size_mb'] >= 0

    def test_clear_all_cache(self, cache_manager):
        """测试清空所有缓存"""
        # 设置多个缓存
        for i in range(3):
            error_message = f"Error {i}: test.py"
            poem = f"Poem {i}"
            cache_manager.set(
                error_message, poem, "gpt-3.5-turbo", "modern", "python"
            )

        # 清空缓存
        cache_manager.clear_all()

        # 验证缓存已清空
        stats = cache_manager.get_cache_stats()
        assert stats['total_entries'] == 0

    def test_cleanup_expired_cache(self, cache_manager):
        """测试清理过期缓存"""
        error_message = "File not found: test.py"
        poem = "在代码的荒原上，\n文件迷失了方向，\n找不到它的归宿。"
        model = "gpt-3.5-turbo"
        template = "modern"
        language = "python"

        # 设置缓存
        cache_manager.set(error_message, poem, model, template, language)

        # 手动修改缓存时间戳为过去（模拟过期）
        cache_key = cache_manager._generate_cache_key(
            error_message, model, template, language
        )
        cache_file = cache_manager._get_cache_file_path(cache_key)

        with open(cache_file, 'r', encoding='utf-8') as f:
            entry = json.load(f)

        entry['timestamp'] = (datetime.now() - timedelta(hours=25)).isoformat()

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

        # 清理过期缓存
        cleaned = cache_manager.cleanup_expired()

        assert cleaned == 1

        # 验证缓存已删除
        retrieved_poem = cache_manager.get(error_message, model, template, language)
        assert retrieved_poem is None

    def test_cache_with_different_parameters(self, cache_manager):
        """测试不同参数的缓存隔离"""
        error_message = "File not found: test.py"
        poem1 = "Poem for modern template"
        poem2 = "Poem for classical template"
        model = "gpt-3.5-turbo"
        language = "python"

        # 使用不同模板设置缓存
        cache_manager.set(error_message, poem1, model, "modern", language)
        cache_manager.set(error_message, poem2, model, "classical", language)

        # 验证缓存隔离
        retrieved_poem1 = cache_manager.get(error_message, model, "modern", language)
        retrieved_poem2 = cache_manager.get(error_message, model, "classical", language)

        assert retrieved_poem1 == poem1
        assert retrieved_poem2 == poem2
        assert retrieved_poem1 != retrieved_poem2