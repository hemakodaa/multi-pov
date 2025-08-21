from urllib.parse import urlparse
import re

def which_site(url: str):
    parser = urlparse(url)
    yt = "youtube"
    twitch = "twitch"
    keyword = [yt, twitch]
    current_keyword = f"Current searched SLD: {','.join(keyword)}"

    if "www" in parser.netloc:
        compile = re.compile(r"\.(\w+)\.", re.IGNORECASE)
    else:
        compile = re.compile(r"\.{,1}(\w+)\.", re.IGNORECASE)

    search = compile.search(parser.netloc)
    print("SLD (netloc):" + parser.netloc)
    print(f"Matched SLD: {search}")
    if not search:
        exit(f"No SLD match found. {current_keyword}")

    needle = search.group(1)

    if needle not in keyword:
        exit(
            f"regex pattern matched, however SLD is not found in keyword. {current_keyword}"
        )

    return needle