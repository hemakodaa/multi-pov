from commands import section_download, full_download
from downloads import (
    DownloadKind,
    BulkDownload,
    single_download,
    bulk_download,
)
from transcript import transcript
from offset import offset
from typing import Callable
from datetime import timedelta as td
from helper import which_site
import argparse
import re
import cli
from log import make_log
from notable_moments import notable_activity, notable_keyword


def start_download(
    fn: Callable,
    kind: DownloadKind,
    bulk: BulkDownload,
    offset_dict: dict,
    start: str | None = None,
    end: str | None = None,
) -> list[str]:
    end_msg = []
    match bulk:
        case BulkDownload.YES:
            module_logger.info("Starting bulk download...")
            end_msg = bulk_download(fn, kind, offset_dict, args, start, end)
        case BulkDownload.NO:
            module_logger.info("Starting download...")
            end_msg.append(single_download(fn, kind, offset_dict, args, start, end))
        case _:
            end_msg = []
    return end_msg


def sanitize_timestamp_input(input_timestamp: str) -> bool:
    s = re.match(r"^\d{1,5}$", input_timestamp)
    ms = re.match(r"^\d{1,2}:\d{1,2}$", input_timestamp)
    hms = re.match(r"^\d{1,2}:\d{1,2}:\d{1,2}$", input_timestamp)
    if any([s, ms, hms]):
        return True
    module_logger.warning(f"Wrong timestamp format {input_timestamp}")
    print(
        "Warning: wrong timestamp format. Accepted format: 0-86400 seconds, mm:ss, hh:mm:ss"
    )
    input("Press any key to continue...")
    return False


def notable(args: argparse.Namespace) -> str:
    module_logger.info("Retrieving moments with notable activity...")
    site = which_site(args.single)
    timestamp = notable_activity(args.single, args.notable, False)
    if site == "youtube":
        separator = "&"
    elif site == "twitch":
        separator = "?"
    else:
        raise ValueError("BUG: new site netloc hasn't been checked")
    print(
        "\n".join(
            [f"[{td(minutes=t)}] {args.single}{separator}t={t}m" for t, _ in timestamp]
        )
    )
    return f"Showing top {100 - args.notable}% of chat activity"


def keyword(args: argparse.Namespace):
    replace_with_pipes = args.keyword.replace(",", "|")
    module_logger.info(
        f"Retrieving moments with specified keyword: {replace_with_pipes}"
    )
    timestamp = notable_keyword(args.single, replace_with_pipes)
    site = which_site(args.single)
    if site == "youtube":
        separator = "&"
    elif site == "twitch":
        separator = "?"
    else:
        raise ValueError("BUG: new site netloc hasn't been checked")
    print(
        "\n".join(
            [
                f"[{td(minutes=t)}][occurences: {f}] {args.single}{separator}t={int(t)}m"
                for t, f in timestamp
            ]
        )
    )
    return f"Showing results for keyword: {replace_with_pipes}"


def main(args: argparse.Namespace):
    # single download means there's not really a 'reference'
    if args.single:
        if args.notable:
            exit(notable(args))
        if args.keyword:
            exit(keyword(args))
        reference_streamer = {
            "url": args.single,
            "streamer": "single_download" if not args.reference else args.reference,
        }  # need better name
        offset_dict = {"list": [reference_streamer], "ref": reference_streamer}
        if args.transcript:
            transcript(args.single)
            exit()

    else:
        offset_dict: dict[str, str] = offset(args.offsetfile, args.reference)
        reference_streamer = offset_dict.get("ref")

    # a full vod download
    if args.full:
        module_logger.info("Starting full video download...")
        result = start_download(
            full_download,
            DownloadKind.FULL,
            BulkDownload.NO if args.single else BulkDownload.YES,
            offset_dict,
        )
        for msg in result:
            print(msg)
        exit("Download Finished")

    # section downloads
    while True:
        try:
            print(
                f"\nReference streamer: {reference_streamer.get("streamer").strip()}\nURL: {reference_streamer.get("url").strip()}"
            )
            print("\nStreamers:")
            for d in offset_dict.get("list"):
                if d.get("streamer") == offset_dict.get("ref").get("streamer"):
                    print(f"{d.get("streamer")} (REF)")
                    continue
                print(d.get("streamer"))
            print(f"\nMax resolution: {args.resolution}p\n")
            start = input("Start: ")
            if not sanitize_timestamp_input(start):
                continue
            end = input("End: ")
            if not sanitize_timestamp_input(end):
                continue
            result = start_download(
                section_download,
                DownloadKind.SECTION,
                BulkDownload.NO if args.single else BulkDownload.YES,
                offset_dict,
                start,
                end,
            )
            for msg in result:
                print(msg)
        except KeyboardInterrupt:
            exit("\nExited.")


if __name__ == "__main__":
    # if no arguments is given, print the help page.
    module_logger = make_log()
    args, parser = cli.cli_main()
    if not args.offsetfile and not args.single:
        exit(parser.print_help())
    main(args)
