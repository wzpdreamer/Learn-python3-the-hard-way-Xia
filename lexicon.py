lexicon = {'north': ('direction', 'north'), 'south': ('direction', 'south'), 'east': ('direction', 'east'),
    'west': ('direction', 'west'),

    'go': ('verb', 'go'), 'kill': ('verb', 'kill'), 'eat': ('verb', 'eat'),

    'the': ('stop', 'the'), 'in': ('stop', 'in'), 'of': ('stop', 'of'),

    'bear': ('noun', 'bear'), 'princess': ('noun', 'princess'), }


def convert_number(s):
    try:
        return int(s)
    except ValueError:
        return None


def scan(sentence):
    words = sentence.split()
    result = []

    for word in words:
        if convert_number(word):
            result.append(('number', int(word)))
        elif word in lexicon.keys():
            result.append(lexicon[word])
        else:
            result.append(('error', word))
    return result
