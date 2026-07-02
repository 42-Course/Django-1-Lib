#!/usr/bin/python3
import sys
import json

import requests
import dewiki

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "PiscineDjango/1.0 (educational project)"}


def fetch_wikitext(search):
    params = {
        "format": "json",
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "redirects": 1,
        "titles": search,
    }
    response = requests.get(API_URL, params=params, headers=HEADERS,
                            timeout=10)
    response.raise_for_status()
    data = json.loads(response.text)

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    if "missing" in page or "revisions" not in page:
        raise ValueError("no result found for '{}'".format(search))
    return page["title"], page["revisions"][0]["slots"]["main"]["*"]


def request_wikipedia(search):
    title, wikitext = fetch_wikitext(search)
    text = dewiki.from_string(wikitext)

    filename = title.replace(" ", "_") + ".wiki"
    with open(filename, "w") as f:
        f.write(text)


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2 or not sys.argv[1].strip():
            raise ValueError("usage: request_wikipedia.py <search>")
        request_wikipedia(sys.argv[1])
    except Exception as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
