from pathlib import Path
from typing import Dict, Iterable, List
from collections.abc import Container
from itertools import groupby

from pydub import AudioSegment

from convert.types import Filename
from convert import phonetics


def concat_phones(phones: Iterable[str],
                  lookup: Dict[str, AudioSegment],
                  speedup: float = 2.0,
                  volume_change: float = 18) -> AudioSegment:
    return sum(lookup[phone] for phone in phones).speedup(speedup, 50) + volume_change


def group_phones(sentence: Iterable[str], phones: Container[str]) -> List[List[str]]:
    return [list(group) for key, group in
            groupby(sentence, lambda x: x in phones) if key]


def line_to_sound(line_phones: Iterable[str],
                  lookup: Dict[str, AudioSegment],
                  silence: AudioSegment = AudioSegment.silent(100, frame_rate=22050),
                  speedup: float = 2.0,
                  volume_change: float = 18) -> AudioSegment:
    sounds = []
    word_phones = group_phones(line_phones, lookup.keys())
    for word in word_phones:
        sounds.extend((concat_phones(word, lookup, speedup, volume_change), silence))
    return sum(sounds[:-1])


def text_to_speech(input_stream: List[List[str]],
                   lookup: Dict[str, AudioSegment],
                   output_directory: Filename | None = None,
                   phone_type: str = "ipa_phon") -> List[AudioSegment]:
    lines = phonetics.convert_and_dump(input_stream)[phone_type]

    if output_directory is not None:
        output_directory = Path(output_directory)

    sounds = []

    for i, line in enumerate(lines):
        sound = line_to_sound(line, lookup)
        sounds.append(sound)
        if output_directory is not None:
            filename = (output_directory / str(i)).with_suffix(".wav")
            sound.export(filename, format="wav")

    return sounds