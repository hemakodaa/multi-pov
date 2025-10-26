import argparse


def cli_main() -> argparse.Namespace:
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
    return args, parser