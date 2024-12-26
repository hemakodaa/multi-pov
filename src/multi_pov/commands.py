import subprocess
from pathlib import Path
from constants import YT_DLP, DOWNLOAD_FOLDER, FILENAME


def timestamp_in_range(start: int, end: int) -> bool:
    # check if adjusted start and end timestamps are within range
    # of the particular video

    # Explanation:
    # negative timestamps tells yt-dlp to download from the end of the stream, instead of the start
    # problem arise when start=0 AND end=0, it will download the entire VOD.
    if start == 0 and end == 0:
        return False
    return True


def download(url: str, start: str, end: str, resolution: int):
    if not timestamp_in_range(start, end):
        return f"Skipped {url}: timestamp out of range"
    download_sections_switch = "--download-sections"
    download_sections = f"*{start}-{end}"
    format_selection_switch = "-f"
    # [format_note!*=Premium] <= exclude premium bitrates
    format_selection = f"bestvideo[height<={resolution}][format_note!*=Premium][ext=mp4]+bestaudio[ext=m4a]"
    output_selection_switch = "-o"
    output_selection = f"{Path().cwd().joinpath(DOWNLOAD_FOLDER).joinpath(FILENAME)}"
    subprocess.run(
        [
            YT_DLP,
            download_sections_switch,
            download_sections,
            format_selection_switch,
            format_selection,
            output_selection_switch,
            output_selection,
            url,
        ]
    )
    return f"Downloaded: {url}"
