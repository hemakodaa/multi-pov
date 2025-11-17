from youtube_transcript_api import YouTubeTranscriptApi as yt_transcript
from urllib.parse import urlparse
from log import log_main
import re
import requests
from bs4 import BeautifulSoup
import pathlib
from pathlib import Path
from constants import LOGGER_BASE

module_logger = log_main(f"{LOGGER_BASE}.{__name__}")


def get_video_id(url: str) -> str | None:
    parse_url = urlparse(url)
    m = None
    if "watch" in parse_url.path:
        q = parse_url.query
        if "&" in q:
            m = re.search(r"v=([\w-]+)&", q, re.IGNORECASE)
        else:
            m = re.search(r"v=([\w-]+)", q, re.IGNORECASE)
    if "live" in parse_url.path:
        p = parse_url.path
        m = re.search(r"live\/([\w-]+)", p, re.IGNORECASE)
    return m if not m else m.group(1)


def transcript(url: str):
    video_id = get_video_id(url)
    module_logger.info(f"Retrieving transcript for {video_id}")
    t = yt_transcript().fetch(video_id=video_id)
    collection = []
    for dictionary in t.to_raw_data():
        text = dictionary.get("text")
        timestamp = dictionary.get("start")  # in seconds
        collection.append(
            f"[{text}](https://www.youtube.com/watch?v={video_id}&t={timestamp}s)"
        )
    # dha: "keep this, do the splicing with md2line"
    # hi this is dha from the future, turns out it was dumb
    print("\n".join(collection))
    # with open(f"{md_file}", "w+") as file:
    #     file.write(" ".join(collection))
    # print(f"Saved: {md_file}")


if __name__ == "__main__":
    url_list = [
        "https://www.youtube.com/watch?v=w-N6eibzFrA",
        "https://www.youtube.com/watch?v=pv5_A-OAQao&t=2580s",
        "https://www.youtube.com/live/pv5_A-OAQao?si=f5ySSxSyOgUHdLLp",
        "https://www.youtube.com/live/pv5_A-OAQao?si=f5ySSxSyOgUHdLLp&t=2593",
    ]
    url = url_list[1]
    transcript(url)
