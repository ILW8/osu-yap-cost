from download import download_from_playlist, get_manifest_from_url, merge_parts
import os
import shutil


def main():
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found in PATH")
        return
    manifest_url = get_manifest_from_url("https://www.twitch.tv/videos/2315679372")
    prefix, fragments = download_from_playlist(manifest_url)
    print(fragments)

    final_path = os.path.join(prefix, "final_merged.wav")
    merge_parts([os.path.join(prefix, fragment) for fragment in fragments], final_path, overwrite_output=False)

    assert os.path.exists(final_path)


if __name__ == '__main__':
    main()
