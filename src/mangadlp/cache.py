import json
from pathlib import Path
from typing import List, Union

from loguru import logger as log

from mangadlp.models import CacheData, CacheKeyData


class CacheDB:
    def __init__(
        self,
        db_path: Union[str, Path],
        manga_uuid: str,
        manga_lang: str,
        manga_name: str,
    ) -> None:
        self.db_path = Path(db_path)
        self.uuid = manga_uuid
        self.lang = manga_lang
        self.name = manga_name
        self.db_key = f"{manga_uuid}__{manga_lang}"

        self._prepare_db()

        self.db_data = self._read_db()
        # create db key entry if not found
        if not self.db_data.get(self.db_key):
            self.db_data[self.db_key] = {}

        self.db_uuid_data: CacheKeyData = self.db_data[self.db_key]
        if not self.db_uuid_data.get("name"):
            self.db_uuid_data.update({"name": self.name})
            self._write_db()

        self.db_uuid_chapters: List[str] = self.db_uuid_data.get("chapters") or []

    def _prepare_db(self) -> None:
        if self.db_path.exists():
            return
        # create empty cache
        try:
            self.db_path.touch()
            self.db_path.write_text(json.dumps({}), encoding="utf8")
        except Exception as exc:
            log.error("Can't create db-file")
            raise exc

    def _read_db(self) -> CacheData:
        log.info(f"Reading cache-db: {self.db_path}")
        try:
            db_txt = self.db_path.read_text(encoding="utf8")
            db_dict: CacheData = json.loads(db_txt)
        except Exception as exc:
            log.error("Can't load cache-db")
            raise exc

        return db_dict

    def _write_db(self) -> None:
        db_dump = json.dumps(self.db_data, indent=4, sort_keys=True)
        self.db_path.write_text(db_dump, encoding="utf8")

    def add_chapter(self, chapter: str) -> None:
        log.info(f"Adding chapter to cache-db: {chapter}")
        self.db_uuid_chapters.append(chapter)
        # dedup entries
        updated_chapters = list({*self.db_uuid_chapters})
        sorted_chapters = sort_chapters(updated_chapters)
        try:
            self.db_data[self.db_key]["chapters"] = sorted_chapters
            self._write_db()
        except Exception as exc:
            log.error("Can't write cache-db")
            raise exc


def sort_chapters(chapters: List[str]) -> List[str]:
    try:
        sorted_list = sorted(chapters, key=float)
    except Exception:
        log.debug("Can't sort cache by float, using default sorting")
        sorted_list = sorted(chapters)

    return sorted_list
