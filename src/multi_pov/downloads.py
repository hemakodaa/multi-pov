from typing import Callable
from enum import Enum, auto
from argparse import Namespace
from offset import produce_timedelta
from log import log_main
import concurrent.futures
from constants import LOGGER_BASE

module_logger = log_main(f"{LOGGER_BASE}.{__name__}")


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
            module_logger.info("Spawning workers for section downloads...")
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
            module_logger.info("Spawning workers for full video downloads...")
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
            module_logger.info(f"Starting {start} - {end} section download for {args.single}")
            msg = fn(
                d.get("list")[0].get("url"),
                produce_timedelta(start).total_seconds(),
                produce_timedelta(end).total_seconds(),
                args.resolution,
            )
        case DownloadKind.FULL:
            url = d.get("list")[0].get("url")
            module_logger.info(f"Starting full video download: {url}")
            msg = fn(url, args.resolution)
        case _:
            msg = "No video was downloaded."
    return msg
