from argparse import ArgumentParser
from typing import List
import sys

from convert import audio, phonetics, tts


def parse(args: List[str]) -> ArgumentParser:
    parser = ArgumentParser("Utilities for preparing text and audio for GBA TTS")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    text_parser = subparsers.add_parser('transliterate',
                                        help="used to transliterate a text into different phonetic representations")
    text_parser.add_argument("input_file",
                             type=str,
                             help="Location of the original source text to phonetically transcribe")
    text_parser.add_argument("--output_g2p",
                             type=str,
                             help="Location of the file to output the g2p allophones JSON to")
    text_parser.add_argument("--output_ipa_allo",
                             type=str,
                             help="Location of the file to output the ipa allophones JSON to")
    text_parser.add_argument("--output_ipa_phon",
                             type=str,
                             help="Location of the file to output the ipa phonemes JSON to")

    resampler_parser = subparsers.add_parser('resample',
                                             help="utility to convert a directory of phonemes into a format usable for Butano on the GBA")
    resampler_parser.add_argument("input_directory",
                                  type=str,
                                  help="Location of the source recordings")
    resampler_parser.add_argument("output_directory",
                                  type=str,
                                  help="Location the new recordings will be saved to")

    tts_parser = subparsers.add_parser('tts',
                                       help="utility to convert text to speech. Select only one of file or text for input")
    tts_parser.add_argument("input_file",
                            type=str,
                            help="Location of the source text file")
    tts_parser.add_argument("output_directory",
                            type=str,
                            help="Directory that will hold the output wavs")
    tts_parser.add_argument("phone_directory",
                            type=str,
                            help="Directory holding the reference phones")
    tts_parser.add_argument("phone_type",
                            choices=["g2p_allos", "ipa_allos", "ipa_phons"],
                            help="Directory holding the reference phones")

    parsed_args = parser.parse_args(args)

    if parsed_args.command is None:
        parser.print_help()
        sys.exit(1)

    return parsed_args


if __name__ == "__main__":
    args = parse(sys.argv[1:])

    if args.command == "transliterate":
        with open(args.input_file) as fin:
            phonetics.convert_and_dump(fin,
                                       args.output_g2p,
                                       args.output_ipa_allo,
                                       args.output_ipa_phon
                                       )
    elif args.command == "resample":
        audio.load_ipa_audio(args.input_directory,
                             output_directory=args.output_directory,
                             transform=audio.gba_resample)
    elif args.command == "tts":
        with open(args.input_file) as fin:
            tts.text_to_speech(fin,
                               audio.load_ipa_audio(args.phone_directory),
                               args.output_directory,
                               args.phone_type
                               )

    print("Finished successfully!")
