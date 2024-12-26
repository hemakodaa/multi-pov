# read from offset file and determine the offset across different livers
from constants import OFFSET_FOLDER
import csv
from exceptions import FileEmptyError
from datetime import timedelta
from pathlib import Path
from enum import Enum, auto


class OffsetType(Enum):
    PLUS = auto()
    MINUS = auto()
    REFERENCE = auto()


def open_csv(offset_file: str) -> list[dict]:

    try:
        with open(
            Path.cwd().joinpath(OFFSET_FOLDER).joinpath(offset_file), "r"
        ) as file:
            file = csv.DictReader(file, fieldnames=["streamer", "time", "url"])
            if (
                Path()
                .cwd()
                .joinpath(OFFSET_FOLDER)
                .joinpath(offset_file)
                .stat()
                .st_size
                == 0
            ):
                raise FileEmptyError("File is empty")
            return [dict for dict in file]
    except FileNotFoundError as e:
        print(e)
        print(
            f"\n\nFile {offset_file} does not exist. Include the file's extension.\n\n"
        )


def safe_cast_to_int(string: str, default=None) -> int:
    try:
        return int(string)
    except (ValueError, TypeError) as e:
        print(e)
        print(
            f"\n\nSummary: {string} is not an integer.\nMake sure timestamps only contain numbers and ':' separator in offset file.\n\n"
        )
        return default


def strip_leading_zeros(s: str) -> str:
    lstrip = s.lstrip("0")
    return "0" if not lstrip else lstrip


def produce_timedelta(timestamp: str) -> timedelta:
    # turn timestamp string into a timedelta object
    # for convenient operations.
    split = timestamp.split(":")
    # timedelta cannot accept strings, it has to be integers
    # meaning "4:01" <-- "01" would error
    # thus lstrip("0")

    # "00".lstrip("0") <-- returns None

    if len(split) == 3:
        seconds = strip_leading_zeros(split.pop())
        minutes = strip_leading_zeros(split.pop())
        hours = strip_leading_zeros(split.pop())
        return timedelta(
            hours=safe_cast_to_int(hours),
            minutes=safe_cast_to_int(minutes),
            seconds=safe_cast_to_int(seconds),
        )
    if len(split) == 2:
        seconds = strip_leading_zeros(split.pop())
        minutes = strip_leading_zeros(split.pop())
        return timedelta(
            minutes=safe_cast_to_int(minutes), seconds=safe_cast_to_int(seconds)
        )
    return timedelta(seconds=safe_cast_to_int(strip_leading_zeros(split.pop())))


def calculate_offset(ref: timedelta, other: timedelta) -> float:
    return ref.total_seconds() - other.total_seconds()


def offset_type(ref: timedelta, other: timedelta) -> OffsetType:
    # timedelta arithmetic operation results are unsigned, meaning
    # we know the delta, but we don't know if it is BEFORE or AFTER the reference time.
    # this enum states what operations should be used when calculating
    # the final timestamp before downloading.
    if ref > other:
        return OffsetType.MINUS
    if ref < other:
        return OffsetType.PLUS
    else:
        return OffsetType.REFERENCE


def offset(offset_file: str, reference: str) -> dict[str, list[dict] | str]:
    list_of_time = [streamer for streamer in open_csv(offset_file)]
    ref = ""
    # by default first line of the file is going to be the reference time
    for dict in list_of_time:
        if dict["streamer"] == reference:
            ref = dict
    if not ref:
        ref = list_of_time[0]
    for dict in list_of_time:
        dict["offset"] = calculate_offset(
            produce_timedelta(ref.get("time")), produce_timedelta(dict.get("time"))
        )
    return {"list": list_of_time, "ref": ref}
