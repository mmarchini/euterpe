""" Melody extractor
"""

import vamp
import librosa
from mingus.containers import Note


class Extractor(object):

    _plugins = {
        'melody': 'mtg-melodia:melodia',
        'tempo': 'vamp-aubio:aubiotempo',
        'key': 'qm-vamp-plugins:qm-keydetector',
        'tuning': 'nnls-chroma:tuning',
        'harmony': 'nnls-chroma:chordino'
    }

    def __init__(self, filename):
        self.data, self.rate = librosa.load(filename)

    def _collect(self, extractor):
        return vamp.collect(self.data, self.rate, self._plugins.get(extractor))

    def melody(self, filename):
        collected_data = self._collect('melody')
        step = collected_data['vector'][0]
        melody_steps = collected_data['vector'][1]

        melody = []
        current_step = vamp.vampyhost.RealTime(0, 0)
        for melody_step in melody_steps:
            note = None
            if melody_step > 0:
                note = Note()
                note.from_hertz(melody_step)
            melody.append((current_step, note))
            current_step += step

        return melody
