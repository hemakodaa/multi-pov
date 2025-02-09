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
import argparse
import re
from notable_moments import notable_activity, notable_keyword

parser = argparse.ArgumentParser(
    prog="multi-pov", description="Download multiple POVs at once"
)
parser.add_argument(
    "-o",
    "--offsetfile",
    help="Filename of the offset file (include extension e.g. .txt)",
    type=str,
    metavar="FILENAME",
)
parser.add_argument(
    "-r", "--reference", help="Set the reference streamer", type=str, metavar="NAME"
)
parser.add_argument(
    "-t",
    "--threads",
    help="Set the amount of parallel downloads (default=4)",
    type=int,
    default=4,
    metavar="AMOUNT",
)
parser.add_argument(
    "-p",
    "--resolution",
    help="Set the maximum resolution (default=1080)",
    type=int,
    default=1080,
)
parser.add_argument(
    "-s", "--single", help="Download single videos", type=str, metavar="URL"
)
parser.add_argument("--full", help="Download full VODs.", action="store_true")
parser.add_argument(
    "-n",
    "--notable",
    help="Show notable timestamp from a VOD based on chat activity",
    type=int,
    choices=range(1, 101),
    metavar="PERCENTILE",
)
parser.add_argument(
    "--keyword",
    help="Show notable timestamps based on keywords appearing in live chat. Use ',' delimiter for multiple keywords",
    type=str,
    metavar="REGEX",
)
parser.add_argument(
    "--transcript",
    help="Get an audio transcription of YouTube video",
    action="store_true",
)
args = parser.parse_args()


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
            end_msg = bulk_download(fn, kind, offset_dict, args, start, end)
        case BulkDownload.NO:
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
    print(
        "Warning: wrong timestamp format. Accepted format: 0-86400 seconds, mm:ss, hh:mm:ss"
    )
    input("Press any key to continue...")
    return False


def notable() -> str:
    timestamp = notable_activity(args.single, args.notable, False)
    print("\n".join([f"[{td(minutes=t)}] {args.single}&t={t}m" for t, _ in timestamp]))
    return f"Showing top {100 - args.notable}% of chat activity"


def keyword() -> str:
    replace_with_pipes = args.keyword.replace(",", "|")
    timestamp = notable_keyword(args.single, replace_with_pipes)
    print(f"Showing activity for keyword: {replace_with_pipes}")
    print(
        "\n".join(
            [
                f"[{td(minutes=t)}][occurences: {f}] {args.single}&t={int(t)}m"
                for t, f in timestamp
            ]
        )
    )


def main():
    # single download means there's not really a 'reference'
    if args.single:
        if args.notable:
            exit(notable())
        if args.keyword:
            exit(keyword())
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
    if not args.offsetfile and not args.single:
        exit(parser.print_help())
    main()
