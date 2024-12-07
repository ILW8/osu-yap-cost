import os

from pyannote.audio import Pipeline
import torch

from dotenv import load_dotenv


def diarize(filename: str):
    load_dotenv()
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")

    if hf_token is None:
        print("Hugging Face token not found in environment (HUGGINGFACE_TOKEN)")
        return

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)

    # send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda"))

    # apply pretrained pipeline
    diarization = pipeline(filename)

    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    # start=0.2s stop=1.5s speaker_0
    # start=1.8s stop=3.9s speaker_1
    # start=4.2s stop=5.7s speaker_0
    # ...
