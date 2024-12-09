# noinspection PyPackageRequirements
from pyannote.audio.pipelines.utils.hook import ProgressHook
# noinspection PyPackageRequirements
from pyannote.audio import Pipeline

import torch
import os
from dotenv import load_dotenv


def diarize(filename: str, output_label: str):
    result_file = os.path.join("data", output_label + "_diarization.txt")

    if os.path.exists(result_file) and os.path.isfile(result_file):
        print("output file already exists, skipping diarization")
        return result_file

    load_dotenv()
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")

    if hf_token is None:
        print("Hugging Face token not found in environment (HUGGINGFACE_TOKEN)")
        return

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)
    pipeline.to(torch.device("cuda"))

    # apply pretrained pipeline
    # fixme: this isn't working
    with ProgressHook(transient=True) as hook:
        diarization = pipeline(filename, hook=hook)

    with open(result_file, "w") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.write(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}\n")

    return result_file
