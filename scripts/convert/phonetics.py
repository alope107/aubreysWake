import json
from typing import Dict, Iterable, List, Set

from g2p_en import G2p

from convert.types import Filename

ALLOPHONE_LOOKUP = {
    'aa0': 'ɑ',
    'aa1': 'ˈɑː',
    'aa2': 'ˌɑ',
    'ae0': 'æ',
    'ae1': 'ˈæ',
    'ae2': 'ˌæ',
    'ah0': 'ə',
    'ah1': 'ˈʌ',
    'ah2': 'ˌʌ',
    'ao0': 'ɔ',
    'ao1': 'ˈɔː',
    'ao2': 'ˌɔ',
    'aw0': 'aʊ',
    'aw1': 'ˈaʊ',
    'aw2': 'ˌaʊ',
    'ay0': 'aɪ',
    'ay1': 'ˈaɪ',
    'ay2': 'ˌaɪ',
    'b': 'b',
    'ch': 'tʃ',
    'd': 'd',
    'dh': 'ð',
    'eh0': 'ɛ',
    'eh1': 'ˈɛ',
    'eh2': 'ˌɛ',
    'er0': 'ɚ',
    'er1': 'ˈɚ',
    'er2': 'ˌɚ',
    'ey0': 'eɪ',
    'ey1': 'ˈeɪ',
    'ey2': 'ˌeɪ',
    'f': 'f',
    'g': 'g',
    'hh': 'h',
    'ih0': 'ɪ',
    'ih1': 'ˈɪ',
    'ih2': 'ˌɪ',
    'iy0': 'i',
    'iy1': 'ˈiː',
    'iy2': 'ˌi',
    'jh': 'dʒ',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'ng': 'ŋ',
    'ow0': 'oʊ',
    'ow1': 'ˈoʊ',
    'ow2': 'ˌoʊ',
    'oy0': 'ɔɪ',
    'oy1': 'ˈɔɪ',
    'oy2': 'ˌɔɪ',
    'p': 'p',
    'r': 'ɹ',
    's': 's',
    'sh': 'ʃ',
    't': 't',
    'th': 'θ',
    'uh0': 'ʊ',
    'uh1': 'ˈʊ',
    'uh2': 'ˌʊ',
    'uw': 'uː',
    'uw0': 'u',
    'uw1': 'ˈuː',
    'uw2': 'ˌu',
    'v': 'v',
    'w': 'w',
    'y': 'j',
    'z': 'z',
    'zh': 'ʒ'
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
    Transliterates text into lowercase versions of g2p_en's allophones.
    '''
    if g2p is None:
        g2p = G2p()
    return [[token.lower() for token in g2p(line)]
            for line in inputStream]


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


def diphones(word: Iterable[str]) -> Set[str]:
    '''
    Exploratory function for finding all diphones in a text
    '''
    return set((word[i], word[i + 1]) for i in range(len(word) - 1))
