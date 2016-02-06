
from mingus.core.chords import from_shorthand, determine
from mingus.core.chords import minor_triad, major_triad

params = [
    ('useNNLS', [0.0, 1.0]),  # Default: 1
    ('rollon', map(lambda r: r/2., range(0, 11))),  # Default: 0
    ('tuningmode', [0.0, 1.0]),  # Default: ?
    ('whitening', map(lambda r: r/10., range(0, 11))),  # Default: 1
    ('s', [0.5, 0.699999988079071, 0.8999999761581421]),  # Default: 0.7
    ('boostn', map(lambda r: r/10., range(0, 11))),  # Default: 0.1
    ('usehartesyntax', [0.0, 1.0]),  # Default: ?
]


def next_parameter(current_index=0):
    key, values = params[current_index]
    for value in values:
        if current_index == (len(params) - 1):
            yield {key: value}
        else:
            next_index = current_index + 1
            for params_dict in next_parameter(next_index):
                params_dict.update({key: value})
                yield params_dict


def simplify_chord(chord):
    chord_shorthand = chord
    chord = from_shorthand(chord_shorthand)
    chord_main_note = chord[0]
    if not chord_shorthand.startswith(chord_main_note):
        chord_main_note = ""
        for i, note in enumerate(chord):
            if chord_shorthand.startswith(note):
                chord_main_note = max(note, chord_main_note)
        if not chord_main_note:
            raise ValueError("Unexpected chord: %s" % chord_shorthand)
    minor_chord = minor_triad(chord_main_note)
    minor_diff = len(set(chord) - set(minor_chord))

    major_chord = major_triad(chord_main_note)
    major_diff = len(set(chord) - set(major_chord))

    if minor_diff < major_diff:
        return determine(minor_chord, True, True, True)[0]
    elif major_diff < minor_diff:
        return determine(major_chord, True, True, True)[0]
    else:
        raise ValueError("Unexpected chord: %s" % chord_shorthand)


def markov_chainer(chords, chain_size=4):
    markov_chain = {}
    for i in range(0, len(chords)-1):
        next_notes = markov_chain.get(chords[i], {})
        next_notes[chords[i+1]] = next_notes.get(chords[i+1], 0) + 1
        markov_chain[chords[i]] = next_notes
    from pprint import pprint; pprint(markov_chain)

    top_note = None
    top_note_count = 0
    for note in markov_chain:
        next_notes = markov_chain.get(note)
        markov_chain[note] = sorted(next_notes.iteritems(), key=lambda n: n[1], reverse=True)[0]
        if markov_chain[note][1] > top_note_count:
            top_note = note
            top_note_count = markov_chain[note][1]

    markoved_chords = [top_note]
    for i in range(3):
        markoved_chords.append(markov_chain[markoved_chords[-1]][0])

    return markoved_chords
