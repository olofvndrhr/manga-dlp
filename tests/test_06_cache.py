import json
from pathlib import Path

from mangadlp.cache import CacheDB


def test_cache_creation():
    cache_file = Path("cache.json")
    CacheDB(cache_file, "abc", "en", "test")

    assert cache_file.exists()
    cache_file.unlink()


def test_cache_insert():
    cache_file = Path("cache.json")
    cache = CacheDB(cache_file, "abc", "en", "test")
    cache.add_chapter("1")
    cache.add_chapter("2")

    cache_data = json.loads(cache_file.read_text(encoding="utf8"))

    assert cache_data["abc__en"]["chapters"] == ["1", "2"]
    assert cache_data["abc__en"]["name"] == "test"
    cache_file.unlink()


def test_cache_update():
    cache_file = Path("cache.json")
    cache = CacheDB(cache_file, "abc", "en", "test")
    cache.add_chapter("1")
    cache.add_chapter("2")

    cache_data = json.loads(cache_file.read_text(encoding="utf8"))
    assert cache_data["abc__en"]["chapters"] == ["1", "2"]

    cache.add_chapter("3")

    cache_data = json.loads(cache_file.read_text(encoding="utf8"))
    assert cache_data["abc__en"]["chapters"] == ["1", "2", "3"]

    cache_file.unlink()


def test_cache_multiple():
    cache_file = Path("cache.json")
    cache1 = CacheDB(cache_file, "abc", "en", "test")
    cache1.add_chapter("1")
    cache1.add_chapter("2")

    cache2 = CacheDB(cache_file, "def", "en", "test2")
    cache2.add_chapter("8")
    cache2.add_chapter("9")

    cache_data = json.loads(cache_file.read_text(encoding="utf8"))

    assert cache_data["abc__en"]["chapters"] == ["1", "2"]
    assert cache_data["abc__en"]["name"] == "test"
    assert cache_data["def__en"]["chapters"] == ["8", "9"]
    assert cache_data["def__en"]["name"] == "test2"

    cache_file.unlink()


def test_cache_lang():
    cache_file = Path("cache.json")
    cache1 = CacheDB(cache_file, "abc", "en", "test")
    cache1.add_chapter("1")
    cache1.add_chapter("2")

    cache2 = CacheDB(cache_file, "abc", "de", "test")
    cache2.add_chapter("8")
    cache2.add_chapter("9")

    cache_data = json.loads(cache_file.read_text(encoding="utf8"))

    assert cache_data["abc__en"]["chapters"] == ["1", "2"]
    assert cache_data["abc__de"]["chapters"] == ["8", "9"]

    cache_file.unlink()
