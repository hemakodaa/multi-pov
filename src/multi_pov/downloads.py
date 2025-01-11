from typing import Callable
from enum import Enum, auto
from argparse import Namespace
from offset import produce_timedelta
import concurrent.futures


class DownloadKind(Enum):
    SECTION = auto()
    FULL = auto()


class BulkDownload(Enum):
    YES = auto()
    NO = auto()


def adjusted_timestamps(t: str, offset: int) -> float | int:
    t_delta = produce_timedelta(t).total_seconds()
    delta = t_delta - offset
    return 0 if delta < 0 else delta


def bulk_download(
    fn: Callable,
    kind: DownloadKind,
    offset_dict: dict,
    args: Namespace,
    start: str | None = None,
    end: str | None = None,
):
    end_msg = []
    match kind:
        case DownloadKind.SECTION:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.threads
            ) as executor:
                downloads = {
                    executor.submit(
                        fn,
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
        case DownloadKind.FULL:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.threads
            ) as executor:
                downloads = {
                    executor.submit(
                        fn,
                        dict.get("url"),
                        args.resolution,
                    ): dict
                    for dict in offset_dict.get("list")
                }
                for future in concurrent.futures.as_completed(downloads):
                    msg = future.result()
                    end_msg.append(msg)
            return end_msg


def single_download(
    fn: Callable,
    kind: DownloadKind,
    d: dict,
    args: Namespace,
    start: str | None = None,
    end: str | None = None,
):
    match kind:
        case DownloadKind.SECTION:
            msg = fn(
                d.get("list")[0].get("url"),
                produce_timedelta(start).total_seconds(),
                produce_timedelta(end).total_seconds(),
                args.resolution,
            )
        case DownloadKind.FULL:
            msg = fn(d.get("list")[0].get("url"), args.resolution)
        case _:
            msg = "No video was downloaded."
    return msg
