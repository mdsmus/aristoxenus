art = {'n': "natural",
       '/': "up-stem",
       '\\': "down-stem",
       'o': "harmonic",
       't': "trill-st",
       'T': "trill-wt",
       'S': "turn",
       '$': "inverted-turn",
       'R': "end-with-turn",
       'u': "down-bow",
       'H': "glissando-start",
       'h': "glissando-end",
       ';': "fermata",
       'Q': "gruppetto",
       'p': "app-main-note",
       'U': "mute",
       '[': "tie-start",
       ']': "tie-end",
       '_': "tie-midle",
       '(': "slur-start",
       ')': "slur-end",
       '{': "phrase-start",
       '}': "phrase-end",
       '\'': "staccato",
       's': "spiccato",
       '\\': "pizzicato",
       '`': "staccatissimo",
       '~': "tenuto",
       '^': "accent",
       ':': "arpeggiation",
       'v': "up-bow",
       'z': "sforzando",
       ',': "breath",
       'm': "mordent-st",
       'w': "inverted-mordent-st",
       'M': "mordent-wt",
       'W': "inverted-mordent-wt"}

beams = {'L': 'beam-start',
         'J': 'beam-end',
         'K': 'beam-partial-right',
         'k': 'beam-partial-left'}


types = {'dur': ("0123456789", "Duration must be together."),
         'note': ("abcdefgABCDEFG", "Notes must be together."),
         'dot': (".", "Dots must be together or after a number."),
         'acc': ("#-", "Accs."),
         'art': (art,),
         'beam': (beams,),
         'rest': ("r", "Rest."),
         'acciac': ("q", "App"),
         'app': ("P",)}