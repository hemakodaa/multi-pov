from pathlib import PurePath, Path
import subprocess
import re
import argparse
import sqlite3
from queue import SimpleQueue
from urllib.parse import urlparse
from os import PathLike

parser = argparse.ArgumentParser("Automate multi-pov")
parser.add_argument("streamer", help="Streamer codename", type=str)
parser.add_argument(
    "--transcript", help="Download all transcripts", action="store_true"
)
parser.add_argument("--chat", help="Download all chat", action="store_true")


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


def main_keyword(txtfile: PathLike):
    # ====================
    # PUT KEYWORD HERE
    kw = "lol,lmao"
    DB_PATH = "db/chat.db"
    # kw = "buh"
    # ===================

    lines = []
    # c = re.compile(r"v=(.+)", re.IGNORECASE)
    # NOTE: must add a db checker here to skip existing chat entries
    # otherwise we just go through *all* of the urls in the list.
    lines = SimpleQueue()
    with open(txtfile, "r+") as f:
        _ = [lines.put(tuple(i.split(","))) for i in f.readlines()]
    if not lines:
        exit("lines is empty")
    cur = sqlite3.connect(DB_PATH).cursor()
    existing_yt_id: list[str] = [
        i[0].strip() for i in cur.execute("SELECT name from sqlite_sequence").fetchall()
    ]
    if not existing_yt_id:
        exit("db returns empty")
    while True:
        url, live_status = lines.get()
        url = url.strip()
        yt_id = get_video_id(url)
        live_status = live_status.strip()
        if live_status != "was_live":
            print(url + f" is {live_status}")
            continue
        if yt_id in existing_yt_id:
            continue
        result = subprocess.run(
            [
                "pdm",
                "run",
                "main",
                "-s",
                url,
                "--keyword",
                kw,
            ],
            capture_output=True,
        )
        print(result)
        print(url + " finished.")
        if lines.qsize() < 1:
            break
        print(f"Remaining: {lines.qsize()}")



def main_transcript(streamer: str, url_dump_dir: PathLike, txtfile: PathLike):
    # =====CHANGE FOLDER NAME HERE=======
    # FOLDER = "phish"
    # FOLDER = streamer
    # change to empty string to ignore the constant
    # ===================================

    lines = []
    c = re.compile(r"v=(.+)", re.IGNORECASE)
    with open(txtfile, "r+") as f:
        lines = [tuple(i.split(",")) for i in f.readlines()]
    if not lines:
        exit("variable 'lines' is empty")
    for url, live_status in lines:
        url = url.strip()
        live_status = live_status.strip()
        if live_status != "was_live":
            print(url + f" is {live_status}")
            continue
        id = c.search(url)
        current_filepath = f"{Path(url_dump_dir).joinpath('transcripts').joinpath(streamer).joinpath(id.group(1))}.md"
        if Path(current_filepath).exists():
            print(f"{current_filepath} already exists\nSkipping...\n")
            continue
        output = subprocess.run(
            [
                "pdm",
                "run",
                "main",
                "-s",
                url,
                "--transcript",
            ],
            capture_output=True,
        )
        with open(
            f"{Path(url_dump_dir).joinpath('transcripts').joinpath(streamer).joinpath(id.group(1))}.md",
            "w+",
        ) as f:
            f.write(output.stdout.decode(errors="ignore"))
        print(url + " finished.")


def main(args: argparse.Namespace):
    url_dir = PurePath(r"F:\dhaclips\scrape_tube\files")
    url_dump_dir = PurePath("video_url_dumps")
    txtfile = url_dir.joinpath(args.streamer + "-videos.txt")
    if args.transcript:
        main_transcript(args.streamer, url_dump_dir, txtfile)
    if args.chat:
        main_keyword(txtfile)
    if args.transcript and args.chat:
        main_transcript(args.streamer, url_dump_dir, txtfile)
        main_keyword(txtfile)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

    # main_transcript()
    # main_keyword()
