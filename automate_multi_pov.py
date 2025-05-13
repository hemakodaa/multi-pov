from pathlib import Path
import subprocess
import re

url_dump_dir = "video_url_dumps"


def main_keyword():
    # ====================
    # PUT KEYWORD HERE
    kw = "phishfin"
    # ===================

    lines = []
    c = re.compile(r"v=(.+)", re.IGNORECASE)
    with open(Path(url_dump_dir).joinpath("phish-videos.txt"), "r+") as f:
        lines = [i for i in f.readlines()]
    if not lines:
        exit("lines is empty")
    for line in lines:
        id = c.search(line)
        if Path(
            f"{Path(url_dump_dir).joinpath(kw).joinpath(id.group(1))}.txt"
        ).exists():
            continue
        output = subprocess.run(
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
        with open(
            f"{Path(url_dump_dir).joinpath(kw).joinpath(id.group(1))}.txt", "w+"
        ) as f:
            text = output.stdout.decode()
            reconcile_link = re.sub(r"\r\n&", "&", text)
            remove_extra_newline = re.sub(r"\r\n\[", "\n[", reconcile_link)
            f.write(remove_extra_newline)
        print(line + " finished.")


def main_transcript():
    lines = []
    c = re.compile(r"v=(.+)", re.IGNORECASE)
    with open(Path(url_dump_dir).joinpath("phish-videos.txt"), "r+") as f:
        lines = [i for i in f.readlines()]
    if not lines:
        exit("lines is empty")
    for line in lines:
        id = c.search(line)
        current_filepath = (
            f"{Path(url_dump_dir).joinpath('transcripts').joinpath(id.group(1))}.md"
        )
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
            f"{Path(url_dump_dir).joinpath('transcripts').joinpath(id.group(1))}.md",
            "w+",
        ) as f:
            f.write(output.stdout.decode(errors="ignore"))
        print(line + " finished.")


# main_transcript()
main_keyword()
