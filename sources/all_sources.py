from dataclasses import dataclass
from typing import Callable

from . import BaseSource, XPaths
from .funcs import *


@dataclass
class MerlinScans(BaseSource):
    identifiers = ["merlinscans.com"]
    xpaths = XPaths(
        name="//div[@class='seriestuhead']/h1[@class='entry-title']/text()",
        chapter_title="//div[@class='eplister']/ul/li/div/div/a/span[@class='chapternum']/text()",
        chapter_url="//div[@class='eplister']/ul/li/div/div/a/@href",
        images="/html/body/div/div[2]/div/script[2]/text()",
    )
    fetch_source_fn = default
    fetch_chapter_fn = merlin_img_urls


@dataclass
class AsuraComics(BaseSource):
    identifiers = ["asuracomic.net"]
    xpaths = XPaths(
        name="//title/text()",
        chapter_title="//h3[@class='text-sm text-white font-medium flex flex-row' and not(span/svg)]//text()",
        chapter_url="//h3[@class='text-sm text-white font-medium flex flex-row' and not(span/svg)]/parent::a/@href",
        images="//body/script/text()",
    )
    fetch_source_fn = asura_source
    fetch_chapter_fn = asura_img_urls


ALL_SOURCES: list[type[BaseSource]] = [
    MerlinScans,
    AsuraComics
]
