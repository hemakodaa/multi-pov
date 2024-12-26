# read from offset file and determine the offset across different livers
from constants import OFFSET_FOLDER
import csv
from datetime import timedelta
from pathlib import Path
from enum import Enum, auto


class OffsetType(Enum):
    PLUS = auto()
    MINUS = auto()
    NONE = auto()


def open_csv(offset_file: str) -> list[dict]:
    # add checks to make sure the offset file is correct
    with open(Path.cwd().joinpath(OFFSET_FOLDER).joinpath(offset_file), "r") as file:
        file = csv.DictReader(file, fieldnames=["streamer", "time", "url"])
        return [dict for dict in file]


def safe_cast_to_int(string: str, default=None) -> int:
    try:
        return int(string)
    except (ValueError, TypeError) as e:
        print(
            e
            + f"\n\nSummary: {string} is not an integer.\nMake sure timestamps only contains numbers and ':' separator in offset file."
        )
        return default


def produce_timedelta(timestamp: str) -> timedelta:
    split = timestamp.split(":")
    # timedelta cannot accept strings, has to be integers
    # meaning "4:01" <-- "01" would error
    # thus lstrip("0")
    if len(split) == 3:
        seconds = split.pop().lstrip("0")
        minutes = split.pop().lstrip("0")
        hours = split.pop().lstrip("0")
        return timedelta(
            hours=safe_cast_to_int(hours),
            minutes=safe_cast_to_int(minutes),
            seconds=safe_cast_to_int(seconds),
        )
    if len(split) == 2:
        seconds = split.pop().lstrip("0")
        minutes = split.pop().lstrip("0")
        return timedelta(
            minutes=safe_cast_to_int(minutes), seconds=safe_cast_to_int(seconds)
        )
    return timedelta(seconds=safe_cast_to_int(split.pop().lstrip("0")))


def calculate_offset(ref: timedelta, other: timedelta) -> timedelta:
    return ref - other


def offset_type(ref: timedelta, other: timedelta) -> OffsetType:
    if ref > other:
        return OffsetType.MINUS
    if ref < other:
        return OffsetType.PLUS
    else:
        return OffsetType.NONE


def offset(offset_file: str):
    list_of_time = [streamer for streamer in open_csv(offset_file)]
    ref = list_of_time[0].get(
        "time"
    )  # by default first line of the file is going to be the reference time
    for dict in list_of_time:
        dict["offset"] = calculate_offset(
            produce_timedelta(ref), produce_timedelta(dict.get("time"))
        )
        dict["offset_type"] = offset_type(ref, dict.get("time"))
    print(list_of_time)


if __name__ == "__main__":
    offset("offset.txt")
