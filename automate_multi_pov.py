from pathlib import PurePath, Path
import subprocess
import re
import argparse
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
        lines = [i for i in f.readlines()]
    if not lines:
        exit("lines is empty")
    for line in lines:
        # _ = c.search(line)
        # if Path(
        #     f"{Path(url_dump_dir).joinpath(kw).joinpath(id.group(1))}.txt"
        # ).exists():
        #     print(f"{id.group(1)} exists, Skipping...")
        # continue
        _ = subprocess.run(
            [
                "pdm",
                "run",
                "main",
                "-s",
                line,
                "--keyword",
                kw,
            ],
            capture_output=True,
        )
        # with open(
        #     f"{Path(url_dump_dir).joinpath(kw).joinpath(id.group(1))}.txt", "w+"
        # ) as f:
        #     text = output.stdout.decode()
        #     reconcile_link = re.sub(r"\r\n&", "&", text)
        #     remove_extra_newline = re.sub(r"\r\n\[", "\n[", reconcile_link)
        #     f.write(remove_extra_newline)
        print(line + " finished.")


def main_transcript(streamer: str, url_dump_dir: PathLike, txtfile: PathLike):
    # =====CHANGE FOLDER NAME HERE=======
    # FOLDER = "phish"
    # FOLDER = streamer
    # change to empty string to ignore the constant
    # ===================================

    lines = []
    c = re.compile(r"v=(.+)", re.IGNORECASE)
    with open(txtfile, "r+") as f:
        lines = [i for i in f.readlines()]
    if not lines:
        exit("variable 'lines' is empty")
    for line in lines:
        id = c.search(line)
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
                line,
                "--transcript",
            ],
            capture_output=True,
        )
        with open(
            f"{Path(url_dump_dir).joinpath('transcripts').joinpath(streamer).joinpath(id.group(1))}.md",
            "w+",
        ) as f:
            f.write(output.stdout.decode(errors="ignore"))
        print(line + " finished.")


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
