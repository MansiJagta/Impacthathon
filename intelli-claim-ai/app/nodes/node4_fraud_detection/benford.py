import math

def first_digit(n):
    while n >= 10:
        n //= 10
    return n


def benford_probability(d):
    return math.log10(1 + 1/d)


def benford_score(amount):
    if amount <= 0:
        return 0

    d = first_digit(int(amount))
    expected = benford_probability(d)

    # deviation from expected distribution
    return abs(0.301 - expected)  # simplified