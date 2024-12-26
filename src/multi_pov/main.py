from commands import download
from offset import offset, produce_timedelta
from constants import DEFAULT_RESOLUTION
import argparse
import concurrent.futures

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
args = parser.parse_args()


def adjusted_timestamps(t: str, offset: int):
    t_delta = produce_timedelta(t).total_seconds()
    delta = t_delta - offset
    return 0 if delta < 0 else delta


def main():
    # add a while loop and an option to change reference streamer here
    resolution = input("Resolution: ")
    start = input("Start: ")
    end = input("End: ")
    offset_dict = offset(args.offset_file, args.reference)
    end_msg = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        downloads = {
            executor.submit(
                download,
                dict.get("url"),
                adjusted_timestamps(start, dict.get("offset")),
                adjusted_timestamps(end, dict.get("offset")),
                DEFAULT_RESOLUTION if not resolution else resolution,
            ): dict
            for dict in offset_dict.get("list")
        }
        for future in concurrent.futures.as_completed(downloads):
            msg = future.result()
            end_msg.append(msg)

    for msg in end_msg:
        print(msg)
    end_msg.clear()


if __name__ == "__main__":
    main()
