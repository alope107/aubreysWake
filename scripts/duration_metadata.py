import argparse
from pathlib import Path
import re
from typing import Dict

from pydub import AudioSegment

# Regex pattern to match sound item ID and filename
regex_pattern = r'sound_item\((\d+)\), string_view\("([^"]+)"\)'


def parse_header_file(path: Path) -> Dict[str, int]:
    """
    Parses the C++ header file to extract sound item IDs and corresponding filenames.

    Args:
        path (Path): The path to the C++ header file.

    Returns:
        Dict[str, int]: A dictionary mapping filenames (without extension) to their IDs.
    """
    content = path.read_text()
    matches = re.findall(regex_pattern, content)
    return {name: int(id) for id, name in matches}


def calculate_durations(directory: Path, sound_info: Dict[str, int]) -> Dict[int, int]:
    """
    Calculates the duration in frames for each WAV file in the specified directory.

    Args:
        directory (Path): The directory containing the WAV files.
        sound_info (Dict[str, int]): Dictionary mapping filenames to sound item IDs.

    Returns:
        Dict[int, int]: A dictionary mapping sound item IDs to their duration in frames.
    """
    durations = {}
    for file_path in directory.iterdir():
        if file_path.suffix == '.wav':
            name = file_path.stem
            if name in sound_info:
                audio = AudioSegment.from_file(file_path)
                duration_in_frames = int(audio.duration_seconds * 60)  # 60 fps
                durations[sound_info[name]] = duration_in_frames
    return durations


def generate_header_file(durations: Dict[int, int], output_path: Path) -> None:
    """
    Generates a C++ header file with the durations of the sound items.

    Args:
        durations (Dict[int, int]): A dictionary mapping sound item IDs to durations.
        output_path (Path): The path for the output C++ header file.
    """
    content = (
        '#ifndef WAKE_METADATA\n#define WAKE_METADATA\n\n'
        '#include "bn_sound_item.h"\n\n'
        'namespace wake {\n'
        '    constexpr inline int durations[] = {\n        '
        + ', '.join(str(durations[id]) for id in sorted(durations))
        + '\n    };\n\n'
        '    inline int duration(bn::sound_item sound) {\n'
        '        return durations[sound.id()];\n    }\n}\n'
        '#endif // WAKE_METADATA\n'
    )
    output_path.write_text(content)

# Main execution block


def main():
    parser = argparse.ArgumentParser(description="Generate a C++ header file with durations of WAV files.")
    parser.add_argument("cpp_header_path", type=Path, help="Path to the C++ header file")
    parser.add_argument("wav_directory", type=Path, help="Directory containing the WAV files")
    parser.add_argument("output_header_path", type=Path, help="Path for the output C++ header file")
    args = parser.parse_args()

    sound_info = parse_header_file(args.cpp_header_path)
    durations = calculate_durations(args.wav_directory, sound_info)
    generate_header_file(durations, args.output_header_path)

    print(args.output_header_path.name)


if __name__ == "__main__":
    main()
