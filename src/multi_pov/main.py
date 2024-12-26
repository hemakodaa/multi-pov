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
    # TODO: account for offsets that would go out of range of the video
    # negative timestamps tells yt-dlp to download from the end of the stream, instead of the start
    return delta


def main():
    # add a while loop and an option to change reference streamer here
    start = input("Start: ")
    end = input("End: ")
    resolution = input("Resolution: ")
    offset_dict = offset(args.offset_file, args.reference)
    print(offset_dict)
    for dict in offset_dict.get("list"):
        generate_command(
            dict["url"],
            adjusted_timestamps(start, dict["offset"]),
            adjusted_timestamps(end, dict["offset"]),
            DEFAULT_RESOLUTION if not resolution else resolution,
        )


if __name__ == "__main__":
    main()
