import json
from statistics import stdev
from collections import defaultdict
from tabulate import tabulate


def the_yap():
    with open("data/2320297522_yap_transcript.json", "r") as infile:
        transcription_output = json.load(infile)
    transcript = transcription_output["transcription"]

    with open("data/2320297522_diarization_output.txt", "r") as infile:
        diarization_output = infile.readlines()
    diarization_output = [line.strip().split() for line in diarization_output]
    speakers = [(float(start.split("=")[-1][:-1]), float(end.split("=")[-1][:-1]), speaker)
                for start, end, speaker in diarization_output]

    # I have a list of tuples in `speakers` indicating the start time, end time, and the speaker.
    # Eliminate overlaps by removing the overlapping speaker with the shortest duration.

    # this code is ugly as heck tho...
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
        end = end / 1000.
        text = yapping["text"]
        # print(start, end)

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
    # print(caster_yappage)

    del caster_yappage["speaker_SPEAKER_00"]

    print("\n\n\n\n")

    table_data = []

    avg_words = sum(caster_yappage.values()) / len(caster_yappage)
    stdev_words = stdev(caster_yappage.values())
    for caster, words in caster_yappage.items():
        if words == 0:
            continue
        # table_data.append([caster, words, round((words - avg_words) / stdev_words, 2)])
        table_data.append([caster, words, round((words - avg_words) / stdev_words, 2)])

    table_data.sort(key=lambda x: x[2], reverse=True)

    print(tabulate((list(zip(*list(zip(*table_data))[:2]))),
                   ["caster", "words spoken", "z_yap"],
                   tablefmt="simple_outline"))
    return time_points, data_points


if __name__ == '__main__':
    the_yap()
