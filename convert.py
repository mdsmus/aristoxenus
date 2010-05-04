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
        if isinstance(item, score.Record):
            print("!!! {0}".format(item.data)) 
        elif isinstance(item, score.Comment):
            print("{0} {1}".format(item.level * "!", item.data))
        elif isinstance(item, score.BlankLine):
            print()
        elif isinstance(item, list):
            x = 0
            for el in item:
                if x != 0:
                    print("\t", end='', sep='')
                x += 1
                if isinstance(el, score.Comment):
                    print("{0} {1}".format(el.level * "!", el.data), end='')
                elif type(el) is score.Exclusive:
                    print("*{0}".format(el.name), end='')
                elif type(el) is score.Tandem:
                    print("*{0}".format(el.data), end='')
                elif type(el) is score.Note:
                    print("{1}{0}".format(el.name, el.duration ** -1), end='')
                elif type(el) is score.Rest:
                    print("{0}r".format(el.duration), end='')
                elif type(el) is score.Bar:
                    print("={0}".format(el.number), end='')
                elif type(el) is score.NullToken:
                    print(".", end='')
                else:
                    print(el, end='')
            print()
        else:
            raise ConvertError, "item in score is of unknown type: {0}".format(item)
            
