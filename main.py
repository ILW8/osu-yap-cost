from download import download_from_playlist, get_manifest_from_url
import shutil


def main():
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found in PATH")
        return
    manifest_url = get_manifest_from_url("https://www.twitch.tv/videos/2315679372")
    download_from_playlist(manifest_url)


if __name__ == '__main__':
    main()
