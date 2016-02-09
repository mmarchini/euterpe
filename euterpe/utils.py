from itertools import groupby


def median(sample):
    d = sorted(sample)
    e = [(f[0], len(list(f[1]))) for f in groupby(d)]
    m = reduce(lambda a, b: a[1] > b[1] and a or b, e, ('', 0))[0]

    return m
