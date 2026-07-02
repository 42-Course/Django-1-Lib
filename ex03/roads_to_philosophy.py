#!/usr/bin/python3
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString

BASE = "https://en.wikipedia.org"
SEARCH_URL = BASE + "/w/index.php"
HEADERS = {"User-Agent": "PiscineDjango/1.0 (educational project)"}


def fetch(params=None, url=SEARCH_URL):
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def _tokens(node, italic):
    """Yield ('text', str) / ('a', tag) tokens in document order, flagging
    whether each is inside an italic context."""
    for child in node.children:
        if isinstance(child, NavigableString):
            yield ("text", str(child), italic)
        elif child.name in ("i", "em"):
            yield from _tokens(child, True)
        elif child.name == "a":
            yield ("a", child, italic)
        elif child.name in ("sup", "style", "small"):
            continue
        else:
            yield from _tokens(child, italic)


SKIP_CONTAINERS = ("infobox", "hatnote", "navbox", "sidebar", "thumb",
                   "reflist", "ambox")


def _in_bad_container(tag):
    """True if the paragraph lives inside a table/infobox/note box rather than
    the article body."""
    for parent in tag.parents:
        if parent.name == "body":
            break
        if parent.name in ("table", "td", "th"):
            return True
        for cls in (parent.get("class") or []):
            if any(key in cls for key in SKIP_CONTAINERS):
                return True
    return False


def article_path(href):
    """Return the '/wiki/...' path for a link, stripping any host prefix.

    Wikipedia sometimes emits protocol-relative ('//en.wikipedia.org/wiki/X')
    or absolute ('https://en.wikipedia.org/wiki/X') hrefs instead of the usual
    relative '/wiki/X'. Normalize them all to the bare path."""
    if href.startswith("//"):
        href = "https:" + href
    if href.startswith("http"):
        parsed = urlparse(href)
        if parsed.netloc and parsed.netloc != "en.wikipedia.org":
            return None  # link to another language / project, not a valid road
        href = parsed.path
    return href if href.startswith("/wiki/") else None


def first_link(soup):
    """First intro link that is not italic, not in parentheses, and points to
    a real article."""
    # A page can hold several mw-parser-output blocks (short description,
    # hatnotes...). Keep the one that actually carries the article body.
    candidates = soup.select("div.mw-parser-output")
    if not candidates:
        return None
    content = max(candidates, key=lambda c: len(c.find_all("p")))
    for paragraph in content.find_all("p"):
        if "mw-empty-elt" in (paragraph.get("class") or []):
            continue
        if _in_bad_container(paragraph):
            continue
        depth = 0
        for token in _tokens(paragraph, False):
            if token[0] == "text":
                depth += token[1].count("(") - token[1].count(")")
            else:
                _, tag, in_italic = token
                path = article_path(tag.get("href", ""))
                if (not in_italic and depth == 0
                        and path is not None
                        and ":" not in path.split("/wiki/")[1]):
                    return path
    return None


def title_of(soup):
    heading = soup.select_one("h1#firstHeading")
    return heading.get_text().strip() if heading else None


def roads_to_philosophy(search):
    soup = fetch({"search": search, "title": "Special:Search"})
    visited = []

    while True:
        title = title_of(soup)
        if title is None:
            print("It's a dead end !")
            return
        if title in visited:
            print(title)
            print("It leads to an infinite loop !")
            return
        print(title)
        visited.append(title)

        if title.lower() == "philosophy":
            print("{} roads from {} to philosophy !".format(
                len(visited) - 1, search))
            return

        href = first_link(soup)
        if href is None:
            print("It's a dead end !")
            return
        soup = fetch(url=BASE + href)


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2 or not sys.argv[1].strip():
            raise ValueError("usage: roads_to_philosophy.py <search>")
        roads_to_philosophy(sys.argv[1])
    except Exception as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
