from commands import generate_command
from offset import offset, produce_timedelta
from constants import DEFAULT_RESOLUTION
import argparse

parser = argparse.ArgumentParser(prog="multi-pov", description="Clipper's tool")
parser.add_argument(
    "offset_file",
    help="Filename of the offset file (include extension e.g. .txt)",
    type=str,
)
parser.add_argument("-r", "--reference", help="Set the reference streamer", type=str)
args = parser.parse_args()


def adjusted_timestamps(t: str, offset: int):
    t_delta = produce_timedelta(t).total_seconds()
    delta = t_delta - offset
    return 0 if delta < 0 else delta


def timestamp_in_range(start: int, end: int) -> bool:
    # check if adjusted start and end timestamps are within range
    # of the particular video

    # Explanation:
    # negative timestamps tells yt-dlp to download from the end of the stream, instead of the start
    # problem arise when start=0 AND end=0, it will download the entire VOD.
    if start == 0 and end == 0:
        return False
    return True


def main():
    # add a while loop and an option to change reference streamer here
    resolution = input("Resolution: ")
    start = input("Start: ")
    end = input("End: ")
    offset_dict = offset(args.offset_file, args.reference)
    for dict in offset_dict.get("list"):
        adjusted_start = adjusted_timestamps(start, dict["offset"])
        adjusted_end = adjusted_timestamps(end, dict["offset"])
        if not timestamp_in_range(adjusted_start, adjusted_end):
            print(f"skipped {dict.get("streamer")}: timestamp is out of range.")
            continue
        generate_command(
            dict["url"],
            adjusted_start,
            adjusted_end,
            DEFAULT_RESOLUTION if not resolution else resolution,
        )


if __name__ == "__main__":
    main()
