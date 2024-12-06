import math

import requests
import os
import concurrent.futures
from urllib.parse import urlparse, urlunparse

from yt_dlp import YoutubeDL


def get_manifest_from_url(url: str) -> str | None:
    """
    Gets .m3u8 manifest URL from twitch URL
    :param url: Twitch VOD URL (e.g. "https://www.twitch.tv/videos/2315679372")
    :return: .m3u8 manifest URL, or None if failed
    """
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info['url']


def download_file(uri: str, filename: str) -> None:
    resp = requests.get(uri)
    resp.raise_for_status()
    with open(filename, "wb") as out_fd:
        out_fd.write(resp.content)


def download_from_playlist(uri: str, download_path_prefix="downloads", max_concurrent: int = 4) -> None:
    assert uri.endswith(".m3u8")
    if not os.path.exists(download_path_prefix.rstrip("/")) and not os.path.isdir(download_path_prefix.rstrip("/")):
        os.makedirs(download_path_prefix.rstrip("/"))

    print("Downloading manifest file...")
    manifest_path = os.path.join(download_path_prefix, "playlist.m3u8")
    download_file(uri, manifest_path)

    with open(manifest_path, "r") as infile:
        manifest_content = infile.read()

    fragments = [line for line in manifest_content.splitlines() if line.endswith(".ts")]
    if len(fragments) == 0:
        print("Found no fragments in manifest, aborting.")
        return

    print(f"Found {len(fragments)} fragments")

    parsed_uri = urlparse(uri)
    base_uri = urlunparse((parsed_uri.scheme,
                           parsed_uri.netloc,
                           "/".join(parsed_uri.path.split("/")[:-1]),
                           '',
                           '',
                           ''))

    pad_amount = int(math.log10(len(fragments))) + 1
    count_completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        safe_uri = "".join([c if c.isalnum() else "_" for c in uri])
        intermediate_path = os.path.join(download_path_prefix, safe_uri)
        if not os.path.exists(intermediate_path):
            os.makedirs(intermediate_path)

        futures_to_path = {executor.submit(download_file,
                                           base_uri + fragment_url,
                                           os.path.join(intermediate_path, fragment_url.split("/")[-1])): fragment_url
                           for fragment_url in fragments}

        for future in concurrent.futures.as_completed(futures_to_path):
            count_completed += 1
            print(f"[{count_completed:>{pad_amount}}/{len(fragments)}] {futures_to_path[future]} completed")
    print("Downloading fragments complete.")
