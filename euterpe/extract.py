""" Melody extractor
"""

import vamp
import librosa
from scipy import stats
from mingus.containers import Note

from euterpe import chordino
from euterpe.utils import median


class Extractor(object):

    _plugins = {
        'melody': 'mtg-melodia:melodia',
        # 'tempo': 'vamp-aubio:aubiotempo',
        'tempo': 'qm-vamp-plugins:qm-tempotracker',
        'key': 'qm-vamp-plugins:qm-keydetector',
        'tuning': 'nnls-chroma:tuning',
        'harmony': 'nnls-chroma:chordino'
    }

    def __init__(self, filename):
        self.data, self.rate = librosa.load(filename)

    def _collect(self, extractor, settings={}):
        return vamp.collect(
            self.data,
            self.rate,
            self._plugins.get(extractor),
            parameters=settings
        )

    def melody(self, settings={}):
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

    def harmony(self, settings={}):
        collect = self._collect('harmony', settings).get('list')
        tstamps = [c.get('timestamp') for c in collect]
        intervals = [float(tstamps[i+1]-tstamps[i]) for i in range(0, len(tstamps)-1)]

        hmean = stats.hmean(intervals)
        h_intervals = [0]
        h_intervals += [i+1 for i, val in enumerate(intervals) if val > hmean]

        d = [collect[i]['label'] for i in h_intervals]
        d = filter(lambda a: a != 'N', d)
        d = map(chordino.simplify_chord, d)

        return chordino.markov_chainer(d)

    def tuning(self, settings={}):
        collect = self._collect('tuning', settings)
        tuning = collect.get('list')[0].get('values')[0]
        collect = self._collect('key', {
            'tuning': float(tuning)
        }).get('list')

        tuning = median([c['label'] for c in collect])

        return tuning

    def tempo(self, settings={}):
        collect = self._collect('tempo', settings).get('list')
        tempo = median([c.get('label') for c in collect])

        return tempo
