
from collections import OrderedDict

params = [
    ('useNNLS', [0.0, 1.0]),
    ('rollon', map(lambda r: r/2., range(0, 11))),
    ('tuningmode', [0.0, 1.0]),
    ('whitening', map(lambda r: r/10., range(0, 11))),
    ('s', [0.5, 0.699999988079071, 0.8999999761581421]),
    ('boostn', map(lambda r: r/10., range(0, 11))),
    ('usehartesyntax', [0.0, 1.0]),
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
