from cloudscraper import create_scraper
from lxml import html
from orjson import loads

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