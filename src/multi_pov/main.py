from commands import download
from offset import offset, produce_timedelta
import argparse
import concurrent.futures
import re

parser = argparse.ArgumentParser(
    prog="multi-pov", description="Download multiple POVs at once"
)
parser.add_argument(
    "offset_file",
    help="Filename of the offset file (include extension e.g. .txt)",
    type=str,
)
parser.add_argument("-r", "--reference", help="Set the reference streamer", type=str)
parser.add_argument(
    "-t",
    "--threads",
    help="Set the amount of parallel downloads (default=4)",
    type=int,
    default=4,
)
parser.add_argument(
    "-p",
    "--resolution",
    help="Set the maximum resolution (default=1080)",
    type=int,
    default=1080,
)
args = parser.parse_args()


def adjusted_timestamps(t: str, offset: int):
    t_delta = produce_timedelta(t).total_seconds()
    delta = t_delta - offset
    return 0 if delta < 0 else delta


def start_download(start: str, end: str, offset_dict: dict) -> list[str]:
    end_msg = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        downloads = {
            executor.submit(
                download,
                dict.get("url"),
                adjusted_timestamps(start, dict.get("offset")),
                adjusted_timestamps(end, dict.get("offset")),
                args.resolution,
            ): dict
            for dict in offset_dict.get("list")
        }
        for future in concurrent.futures.as_completed(downloads):
            msg = future.result()
            end_msg.append(msg)
    return end_msg


def sanitize_timestamp_input(input_timestamp: str) -> bool:
    s = re.match(r"^\d{1,2}$", input_timestamp)
    ms = re.match(r"^\d{1,2}:\d{1,2}$", input_timestamp)
    hms = re.match(r"^\d{1,2}:\d{1,2}:\d{1,2}$", input_timestamp)
    if any([s, ms, hms]):
        return True
    print("Warning: wrong timestamp format. Accepted format: ss, mm:ss, hh:mm:ss")
    input("Press any key to continue...")
    return False


def main():
    offset_dict: dict[str, str] = offset(args.offset_file, args.reference)
    reference_streamer = offset_dict.get("ref")
    while True:
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
        result = start_download(start, end, offset_dict)
        for msg in result:
            print(msg)


if __name__ == "__main__":
    main()
