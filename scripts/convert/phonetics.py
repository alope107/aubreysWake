import json
from typing import Dict, Iterable, List

from g2p_en import G2p

from convert.types import Filename

ALLOPHONE_LOOKUP = {
    'AA0': 'ɑ',
    'AA1': 'ˈɑː',
    'AA2': 'ˌɑ',
    'AE0': 'æ',
    'AE1': 'ˈæ',
    'AE2': 'ˌæ',
    'AH0': 'ə',
    'AH1': 'ˈʌ',
    'AH2': 'ˌʌ',
    'AO0': 'ɔ',
    'AO1': 'ˈɔː',
    'AO2': 'ˌɔ',
    'AW0': 'aʊ',
    'AW1': 'ˈaʊ',
    'AW2': 'ˌaʊ',
    'AY0': 'aɪ',
    'AY1': 'ˈaɪ',
    'AY2': 'ˌaɪ',
    'B': 'b',
    'CH': 'tʃ',
    'D': 'd',
    'DH': 'ð',
    'EH0': 'ɛ',
    'EH1': 'ˈɛ',
    'EH2': 'ˌɛ',
    'ER0': 'ɚ',
    'ER1': 'ˈɚ',
    'ER2': 'ˌɚ',
    'EY0': 'eɪ',
    'EY1': 'ˈeɪ',
    'EY2': 'ˌeɪ',
    'F': 'f',
    'G': 'g',
    'HH': 'h',
    'IH0': 'ɪ',
    'IH1': 'ˈɪ',
    'IH2': 'ˌɪ',
    'IY0': 'i',
    'IY1': 'ˈiː',
    'IY2': 'ˌi',
    'JH': 'dʒ',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'ŋ',
    'OW0': 'oʊ',
    'OW1': 'ˈoʊ',
    'OW2': 'ˌoʊ',
    'OY0': 'ɔɪ',
    'OY1': 'ˈɔɪ',
    'OY2': 'ˌɔɪ',
    'P': 'p',
    'R': 'ɹ',
    'S': 's',
    'SH': 'ʃ',
    'T': 't',
    'TH': 'θ',
    'UH0': 'ʊ',
    'UH1': 'ˈʊ',
    'UH2': 'ˌʊ',
    'UW': 'uː',
    'UW0': 'u',
    'UW1': 'ˈuː',
    'UW2': 'ˌu',
    'V': 'v',
    'W': 'w',
    'Y': 'j',
    'Z': 'z',
    'ZH': 'ʒ',
}

REVERSE_ALLOPHONE_LOOKUP = {ipa: g2p for g2p, ipa in ALLOPHONE_LOOKUP.items()}


def strip_markers(allophone: str) -> str:
    '''
    Removes stress / duration markers from an allophone
    '''
    return "".join(c for c in allophone if c not in "ˌˈː")


PHONEME_LOOKUP = {g2p_alph: strip_markers(ipa_alph)
                  for g2p_alph, ipa_alph in ALLOPHONE_LOOKUP.items()}


def text_to_g2p_allophone(inputStream: Iterable[str], g2p: G2p = None) -> List[List[str]]:
    '''
    Transliterates text into g2p_en's allophones.
    '''
    if g2p is None:
        g2p = G2p()
    return [g2p(line) for line in inputStream]


def to_ipa(sentence: List[str], allophones: bool = True) -> List[str]:
    '''
    Converts a List[str] containing g2p allophones to IPA.
    Contains allophones with stress/duration marker is allophones is True, otherwise
    includes only phonemes.
    Any symbols not in the lookup (e.g. punctuation) is left as is.
    '''
    lookup = ALLOPHONE_LOOKUP if allophones else PHONEME_LOOKUP

    return [lookup.get(symbol, symbol)
            for symbol in sentence]


def convert_and_dump(input_stream: Iterable[str],
                     output_g2p: Filename | None = None,
                     output_ipa_allo: Filename | None = None,
                     output_ipa_phon: Filename | None = None,
                     g2p: G2p = None) -> Dict[str, List[List[str]]]:
    '''
    Converts a text file or string to phonetic representation.
    Exactly one of input_file or input_str must be spe

    Returns a dictionary of "g2p_allos", "ipa_allos", and "ipa_phons" mapped to their
    corresponding representations of the text.

    If output filenames are specified, will additionally save the data in JSON format
    '''
    g2p_allos = text_to_g2p_allophone(input_stream, g2p)

    if output_g2p:
        with open(output_g2p, "w") as fout:
            json.dump(g2p_allos, fout, ensure_ascii=False)

    ipa_allos = [to_ipa(line) for line in g2p_allos]
    if output_ipa_allo:
        with open(output_ipa_allo, "w") as fout:
            json.dump(ipa_allos, fout, ensure_ascii=False)

    ipa_phons = [to_ipa(line, False) for line in g2p_allos]
    if output_ipa_phon:
        with open(output_ipa_phon, "w") as fout:
            json.dump(ipa_phons, fout, ensure_ascii=False)

    return {
        "g2p_allos": g2p_allos,
        "ipa_allos": ipa_allos,
        "ipa_phons": ipa_phons
    }
