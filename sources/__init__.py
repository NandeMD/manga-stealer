import re
from dataclasses import dataclass
from typing import Callable

CHAPTER_NUM_RE = re.compile(r"(\d+(\.\d+)?)")


class ChapterInfo:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    @property
    def chapter_number(self):
        match = CHAPTER_NUM_RE.search(self.title)
        return match.group(0) if match else None
    
    @property
    def chapter_number_float(self):
        ch_num = self.chapter_number

        if ch_num:
            try:
                return float(ch_num)
            except ValueError:
                return None
        return None
    
    @property
    def chapter_number_int(self):
        ch_num = self.chapter_number

        if ch_num:
            try:
                return int(ch_num)
            except ValueError:
                return None
        return None

    def __repr__(self):
        return f"ChapterInfo(title={self.title}, url={self.url})"
    


class XPaths:
    def __init__(self, name: str, chapter_title: str, chapter_url: str, images: str):
        self.name = name
        self.chapter_title = chapter_title
        self.chapter_url = chapter_url
        self.images = images



class SourceResult:
    def __init__(self, name: str, chapters: list[ChapterInfo]):
        self.name = name
        self.chapters = chapters

    def __repr__(self):
        return f"SourceResult(name={self.name}, chapters={self.chapters})"
    
    def __str__(self):
        return f"Title: {self.name} --- Chapter Count: {len(self.chapters)}\n"


@dataclass
class BaseSource:
    identifiers: list[str]
    xpaths: XPaths
    fetch_source_fn: Callable[[str, XPaths], SourceResult]
    fetch_chapter_fn: Callable[[str, XPaths], list[str]]