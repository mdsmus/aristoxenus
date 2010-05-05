from __future__ import print_function
import score

class ConvertError(Exception):
    pass


humdrum_table = {
    'natural': "n",
    "up-stem": '/',
    "down-stem": '\\',
    "harmonic": 'o',
    "trill-st": 't',
    "trill-wt": 'T',
    "turn": 'S',
    "inverted-turn": '$',
    "end-with-turn": 'R',
    "down-bow": 'u',
    "glissando-start": 'H',
    "glissando-end": 'h',
    "fermata": ';',
    "gruppetto": 'Q',
    "app-main-note": 'p',
    "mute": 'U',
    "tie-start": '[',
    "tie-end": ']',
    "tie-midle": '_',
    "slur-start": '(',
    "slur-end": ')',
    "phrase-start": '{',
    "phrase-end": '}',
    "staccato": '\'',
    "spiccato": 's',
    "pizzicato": '\\',
    "staccatissimo": '`',
    "tenuto": '~',
    "accent": '^',
    "arpeggiation": ':',
    "up-bow": 'v',
    "sforzando": 'z',
    "breath": ',',
    "mordent-st": 'm',
    "inverted-mordent-st": 'w',
    "mordent-wt": 'M',
    "inverted-mordent-wt": 'W',
    'beam-start': 'L',
    'beam-end': 'J',
    'beam-partial-right': 'K',
    'beam-partial-left': 'k'
    }


def score_to_humdrum(sco):
    for item in sco:
        if type(item) is list:
            print("\t".join([x.show_as_humdrum() for x in item]))
        else:
            item.show_as_humdrum()
