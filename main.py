#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from urllib.parse import unquote

from tqdm import tqdm  # type: ignore

from helpers import fetch_bytes, slugify
from sources.matcher import match_manga_source

argparser = ArgumentParser(
    prog="manga-stealer",
    description="A tool to download manga from various sources.",
)
argparser.add_argument("source", help="The source to download from.")
argparser.add_argument("-o", "--output", help="The output directory for downloaded manga.", type=str, default=".")
argparser.add_argument("-c", "--chapters", help="The chapters to download. Example: `12:22.5` (between 12 and 22.5, 12 included, 22.5 excluded)", type=str, default="all")

args = argparser.parse_args()


def _parse_chapters(chapters: str) -> tuple[float, float]:
    """
    Parse the chapters argument into a tuple of floats.
    """
    if chapters == "all":
        return (0, float("inf"))

    try:
        start, end = map(float, chapters.split(":"))
        return (start, end)
    except ValueError:
        raise ValueError("Invalid chapters format. Use `start:end` or `all`.")


def main():
    start_chapter, end_chapter = _parse_chapters(args.chapters)

    print(f"Hello from manga-stealer! Downloading from source: {args.source}")
    source = match_manga_source(args.source)
    if source:
        print(f"Matched source: {source.__name__}")
    else:
        print("No matching source found.")
        return
    

    print(f"Fetching source...")
    src_result = source.fetch_source_fn(args.source, source.xpaths)
    if end_chapter != float("inf"):
        src_result.chapters = list(filter(lambda c: c.chapter_number_float >= start_chapter and c.chapter_number_float < end_chapter, src_result.chapters)) # type: ignore
    print(f"{src_result}")

    if len(src_result.chapters) == 0:
        print("No chapters found.")
        return
    
    out_path = os.path.join(args.output, slugify(src_result.name, allow_unicode=True))
    print(f"Downloading chapters to: {out_path}")
    os.makedirs(out_path, exist_ok=True)

    for c in tqdm(src_result.chapters, desc="Downloading chapters", unit="chapter"):
        chapter_out_path = os.path.join(out_path, slugify(c.title, allow_unicode=True))
        os.makedirs(chapter_out_path, exist_ok=True)

        chapter_pages = source.fetch_chapter_fn(c.url, source.xpaths)

        for page in chapter_pages:
            page_filename = unquote(os.path.basename(page))
            page_out_path = os.path.join(chapter_out_path, page_filename)


            page_content = fetch_bytes(page)
            with open(page_out_path, 'wb') as f:
                f.write(page_content)


if __name__ == "__main__":
    main()
