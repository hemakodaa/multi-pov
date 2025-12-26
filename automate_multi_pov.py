from pathlib import PurePath, Path
import subprocess
import re
import argparse
import csv
from os import PathLike

parser = argparse.ArgumentParser("Automate multi-pov")
parser.add_argument("streamer", help="Streamer codename", type=str)
parser.add_argument(
    "--transcript", help="Download all transcripts", action="store_true"
)
parser.add_argument("--chat", help="Download all chat", action="store_true")


def main_keyword(txtfile: PathLike):
    # ====================
    # PUT KEYWORD HERE
    kw = "lol,lmao"
    # kw = "buh"
    # ===================

    lines = []
    # c = re.compile(r"v=(.+)", re.IGNORECASE)
    with open(txtfile, "r+") as f:
        lines = [tuple(i.split(",")) for i in f.readlines()]
    if not lines:
        exit("lines is empty")
    for url, live_status in lines:
        url = url.strip()
        live_status = live_status.strip()
        if live_status != "was_live":
            print(url + f" is {live_status}")
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
    url_dump_dir = PurePath("video_url_dumps")
    txtfile = url_dump_dir.joinpath(args.streamer + "-videos.txt")
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
