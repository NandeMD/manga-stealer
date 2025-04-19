from cloudscraper import create_scraper
from lxml import html
from orjson import loads
import re

from . import ChapterInfo, SourceResult, XPaths

html_parser = html.HTMLParser(collect_ids=False)
FLARE_SOLVERR_SESSIN_NAME = "robin"

def __fetch_url(url) -> str:
    scraper = create_scraper()
    with scraper.get(url) as response:
        site = response.text

    del scraper
    del response

    return site


def default(url: str, xpaths: XPaths) -> SourceResult:
    """
    Default function to fetch the source.
    :param url: URL to fetch the source from.
    :param xpaths: XPaths object containing the xpaths to be used.
    :return: SourceResult object containing the name and chapters.
    """
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    name = tree.xpath(xpaths.name)[0]
    chapters = [
        ChapterInfo(
            title=chapter_title,
            url=chapter_url,
        )
        for chapter_title, chapter_url in zip(
            tree.xpath(xpaths.chapter_title),
            tree.xpath(xpaths.chapter_url),
        )
    ]

    return SourceResult(name=name, chapters=chapters)
    

def merlin_img_urls(url: str, xpaths: XPaths) -> list[str]:
    """
    Function to fetch the image URLs from the merlin scans site.
    """
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    ts_script: str = tree.xpath(xpaths.images)[0]
    ts_script = ts_script.removeprefix("ts_reader.run(")
    ts_script = ts_script.removesuffix(");")

    ts_payload = loads(ts_script)
    images = ts_payload["sources"][0]["images"]
    

    return images

def asura_img_urls(url: str, xpaths: XPaths) -> list[str]:
    """
    Function to fetch the image URLs from the asura comic site.
    """
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    ts_script = tree.xpath(xpaths.images)
    all_script = "".join(ts_script)
    url_pattern = r"https?://[^\s\"'>]+"
    urls = re.findall(url_pattern, all_script)
    urls = [url.replace("\\", "") for url in urls]
    urls = list(filter(lambda x: x.endswith("-optimized.webp"), urls))
    pattern = pattern = r"/\d{2}-optimized\.webp$"
    filtered_strings: list[str] = [s for s in urls if re.search(pattern, s)]

    return filtered_strings

def asura_source(url: str, xpaths: XPaths) -> SourceResult:
    """
    Function to fetch the source from the asura comic site.
    """
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    name = tree.xpath(xpaths.name)[0]
    chapters_separated = tree.xpath(xpaths.chapter_title)
    chapter_titles = [" ".join(chapters_separated[i:i+2]) for i in range(0, len(chapters_separated), 2)]
    chapter_urls = [f"https://asuracomic.net/series/{uri}" for uri in tree.xpath(xpaths.chapter_url)]
    chapters = [
        ChapterInfo(
            title=chapter_title,
            url=chapter_url,
        )
        for chapter_title, chapter_url in zip(
            chapter_titles,
            chapter_urls,
        )
    ]

    return SourceResult(name=name, chapters=chapters)