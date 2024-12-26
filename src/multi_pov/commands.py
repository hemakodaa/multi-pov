import subprocess
from pathlib import Path
from constants import YT_DLP, DOWNLOAD_FOLDER, FILENAME


def generate_command(url: str, start: str, end: str, resolution: int):
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
