import json
from pathlib import Path
from typing import Union

from loguru import logger as log


class CacheDB:
    def __init__(self, db_path: Union[str, Path], uuid: str, lang: str) -> None:
        self.db_path = Path(db_path)
        self.uuid = uuid
        self.lang = lang
        self.db_key = f"{uuid}__{lang}"

        self._prepare()

        self.db_data = self.read_db()
        if not self.db_data.get(self.db_key):
            self.db_data[self.db_key] = {}
        self.db_uuid_data: dict = self.db_data[self.db_key]
        self.db_uuid_chapters: list = self.db_uuid_data.get("chapters") or []

    def _prepare(self):
        if self.db_path.exists() and self.db_path.is_file():
            return
        try:
            self.db_path.touch()
            self.db_path.write_text(json.dumps({}), encoding="utf8")
        except Exception as exc:
            log.error("Can't create db-file")
            raise exc

    def read_db(self) -> dict:
        log.info(f"Reading cache-db: {self.db_path}")
        try:
            db_txt = self.db_path.read_text(encoding="utf8")
            db_dict: dict = json.loads(db_txt)
        except Exception as exc:
            log.error("Can't load cache-db")
            raise exc

        return db_dict

    def add_chapter(self, chapter: str) -> None:
        log.info(f"Adding chapter to cache-db: {chapter}")
        self.db_uuid_chapters.append(chapter)
        # dedup entries
        updated_chapters = list({*self.db_uuid_chapters})
        try:
            self.db_data[self.db_key]["chapters"] = sorted(updated_chapters)
            self.db_path.write_text(json.dumps(self.db_data, indent=4), encoding="utf8")
        except Exception as exc:
            log.error("Can't write cache-db")
            raise exc
