from diarization import diarize
from download import download_from_playlist, get_manifest_from_url, merge_parts
import os
import shutil


def main():
    # if shutil.which("ffmpeg") is None:
    #     print("ffmpeg not found in PATH")
    #     return
    # manifest_url = get_manifest_from_url("https://www.twitch.tv/videos/2320297522")
    # prefix, fragments = download_from_playlist(manifest_url)
    # print(fragments)
    #
    # final_path = os.path.join(prefix, "final_merged.wav")
    # merge_parts([os.path.join(prefix, fragment) for fragment in fragments], final_path, overwrite_output=False)
    #
    # assert os.path.exists(final_path)

    diarize(r"C:\Users\daohe\PycharmProjects\caster-yap-cost\osu_yap_losers_gf_original_cut.wav")


if __name__ == '__main__':
    main()
