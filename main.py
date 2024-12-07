from diarization import diarize
from download import download_from_playlist, get_manifest_from_url, merge_parts, resample_audio
import os
import shutil

from yap_cost import the_yap

# VARIABLES TO EDIT:
SRC_VOD_URL = "https://www.twitch.tv/videos/2320755972"  # twitch vod link
DATA_LABEL = "showmatch_gf"  # prefix for files to be saved into data folder


def main():
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found in PATH")
        return
    manifest_url = get_manifest_from_url(SRC_VOD_URL)
    print(f"Manifest URL: {manifest_url}")
    prefix, fragments = download_from_playlist(manifest_url)
    print(fragments)

    merged_audio_path = os.path.join(prefix, "final_merged.wav")
    merged_audio_resampled_path = os.path.join(prefix, "final_resampled.wav")
    merge_parts([os.path.join(prefix, fragment) for fragment in fragments], merged_audio_path, overwrite_output=False)
    assert os.path.exists(merged_audio_path)

    diarization_data_path = diarize(merged_audio_path, DATA_LABEL)

    # todo: run whisper.cpp from here
    # for now, hardcode a path to transcript
    resampled_audio_path = resample_audio(merged_audio_path, merged_audio_resampled_path, 16_000)
    transcript_path = os.path.join("data", "showmatch_gf_yap_transcript.json")

    the_yap(transcript_path, diarization_data_path)


if __name__ == '__main__':
    main()
