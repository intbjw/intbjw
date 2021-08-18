import httpx
import json
import pathlib
import re
import os
import datetime

wakatime_raw_url = "https://gist.githubusercontent.com/intbjw/b3f5ba2c84e8e524c10ca588825ff915/raw/"

root = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_code_time():
    return httpx.get(wakatime_raw_url)


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open(encoding='UTF-8').read()

    code_time_text = "\n```text\n"+fetch_code_time().text+"\n```\n"
    rewritten = replace_chunk(readme_contents, "code_time", code_time_text)
    readme.open("w", encoding='UTF-8').write(rewritten)
