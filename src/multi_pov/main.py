from commands import generate_command
from offset import offset
import argparse

parser = argparse.ArgumentParser(prog="multi-pov", description="Clipper's tool")
parser.add_argument(
    "offset_file",
    help="Filename of the offset file (include extension e.g. .txt)",
    type=str,
)
parser.add_argument("-r", "--reference", help="Set the reference streamer", type=str)
args = parser.parse_args()


def main():
    # add a while loop and an option to change reference streamer here
    list_of_time = offset(args.offset_file, args.reference)
    for dict in list_of_time:
        generate_command(
            dict["url"],
        )


if __name__ == "__main__":
    main()
