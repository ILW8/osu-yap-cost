import json
from statistics import stdev
from collections import defaultdict
from tabulate import tabulate


def the_yap(transcript_file: str, diarization_file: str):
    with open(transcript_file, "r") as infile:
        transcription_output = json.load(infile)
    transcript = transcription_output["transcription"]

    with open(diarization_file, "r") as infile:
        diarization_output = infile.readlines()
    diarization_output = [line.strip().split() for line in diarization_output]
    speakers = [(float(start.split("=")[-1][:-1]), float(end.split("=")[-1][:-1]), speaker)
                for start, end, speaker in diarization_output]

    # TODO: the below logic sometimes mis-attributes speakers, as it doesn't check for total overlap ratio
    #       but only checks the start timestamps of a speech segment.
    # I have a list of tuples in `speakers` indicating the start time, end time, and the speaker.
    # Eliminate overlaps by removing the overlapping speaker with the shortest duration.

    # this code is ugly as heck
    for idx in range(len(speakers)):
        if speakers[idx] is None:
            continue

        start, end, speaker = speakers[idx]
        for idx2 in range(idx + 1, len(speakers)):
            if speakers[idx2] is None:
                continue
            start2, end2, speaker2 = speakers[idx2]
            if start2 < end and end2 > start:
                if end - start > end2 - start2:
                    speakers[idx2] = None
                else:
                    speakers[idx] = None
                break

    speakers = [speaker for speaker in speakers if speaker is not None]

    caster_yappage = defaultdict(int)

    # todo: load speakers mapping from a data file
    speakers_map = {
        "speaker_SPEAKER_02": "ChillierPear",
        "speaker_SPEAKER_03": "D I O",
        "speaker_SPEAKER_01": "Azer"
        # "speaker_SPEAKER_04": "Doomsdau",
        # "speaker_SPEAKER_03": "Damarsh",
        # "speaker_SPEAKER_01": "SadShiba"
    }

    time_points = []
    data_points = defaultdict(list)
    all_speakers_set = set()
    for _, _, speaker in speakers:
        if speaker in speakers_map:
            speaker = speakers_map[speaker]
        all_speakers_set.add(speaker)

    for yapping in transcript:
        start, end = yapping["offsets"].values()
        start = start / 1000.
        text = yapping["text"]

        for s_start, s_end, speaker in speakers:
            if s_start <= start <= s_end and s_end - start > 0.5:
                if speaker in speakers_map:
                    speaker = speakers_map[speaker]
                else:
                    print(f"[{s_start} -> {s_end}] Unknown speaker {speaker}: {text}")
                caster_yappage[speaker] += len(text.split())

                time_points.append(start)
                for _speaker in all_speakers_set:
                    data_points[_speaker].append(caster_yappage[_speaker])
                break

    del caster_yappage["speaker_SPEAKER_00"]

    print("\n\n\n\n")

    table_data = []

    avg_words = sum(caster_yappage.values()) / len(caster_yappage)
    stdev_words = stdev(caster_yappage.values())
    for caster, words in caster_yappage.items():
        if words == 0:
            continue
        table_data.append([caster, words, round((words - avg_words) / stdev_words, 2)])

    table_data.sort(key=lambda x: x[2], reverse=True)

    print(tabulate((list(zip(*list(zip(*table_data))[:2]))),
                   ["caster", "words spoken", "z_yap"],
                   tablefmt="simple_outline"))
    return time_points, data_points
