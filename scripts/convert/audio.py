from pathlib import Path
from typing import Callable, Dict, List

from pydub import AudioSegment

from convert.types import Filename
from convert.phonetics import REVERSE_ALLOPHONE_LOOKUP


def gba_resample(sound: AudioSegment) -> AudioSegment:
    '''
    Resamples a sound to an unsigned 8 bit with 22050Hz.

    Format should be compatible with Gameboy Advance using Butano.
    '''
    return sound.set_sample_width(1).set_frame_rate(22050)


def load_ipa_audio(input_directory: Filename,
                   glob: str = "*",
                   transform: Callable[[AudioSegment], AudioSegment] | None = None,
                   output_directory: Filename | None = None
                   ) -> Dict[str, AudioSegment]:
    '''
    Loads a dictionary of IPA symbol to AudioSegment from a directory of samples.

    All files must be named with the appropriate IPA symbol. Does not recurse.

    Filters files based on a provided glob, performs no filtering by default.

    If a transform is supplied, it transforms the audio before putting it in the
    dictionary.

    If output_directory is specified, will save the transformed audio in the given location.
    The output filenames will be the g2p symbols and will all be WAVs.
    Will overwrite any existing WAV files with the same name.
    '''

    if transform is None:
        def transform(x): return x

    ipa_audio = {file.stem: transform(AudioSegment.from_file(file))
                 for file in Path(input_directory).glob(glob)}

    if output_directory:
        save_ipa_audio(ipa_audio, output_directory, REVERSE_ALLOPHONE_LOOKUP)

    return ipa_audio


def save_ipa_audio(ipa_audio: Dict[str, AudioSegment],
                   directory: Filename,
                   rename: Dict[str, str] | None = None) -> None:
    '''
    Saves the IPA sound samples in the given directory.

    If no rename is provided, the filenames will be the keys and will all be WAVs.
    If a rename is provided, the filename will be transformed.
    Will overwrite any existing WAV files with the same name.
    '''

    for symbol, sound in ipa_audio.items():
        if rename:
            if symbol in rename:
                symbol = rename[symbol]
            else:
                print(f"WARNING: Unknown symbol: {symbol}, skipping")
                continue
        filename = (Path(directory) / symbol).with_suffix(".wav")
        sound.export(filename, format="wav")
