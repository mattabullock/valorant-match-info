#!/usr/bin/env python

# M (scaling + reflection + rotation + translation)
# [ a b c ] [x]   [x']
# [ d e f ] [y] = [y']
# [ 0 0 1 ] [1]   [1 ]
# a*x + b*y + c - x' = 0
# d*x + e*y + f - y' = 0

# need at least 6
known_translations = [
    # first pair is (x,y) from the API
    # second pair is the pixel coordinates from the image
    ((2815, 818), (180, 546)),  # enemy reyna
    ((450, -682), (361, 659)),  # Woofles
    ((1658, -707), (267, 661)),  # psycho
    ((707, 1732), (340, 474)),  # enemy raze
    ((-2785, 4019), (606, 300)),  # enemy omen
    ((-5818, 669), (519, 837)),  # enemy jett
]

import sympy as sym

a, b, c, d, e, f = sym.symbols("a b c d e f")


def gen_eq(translation):
    p1, p2 = translation[0], translation[1]
    return [
        p1[0] * a + p1[1] * b + c - p2[0],
        p1[0] * d + p1[1] * e + f - p2[1],
    ]


def gen_eqs(k):
    eqs = []
    for t in k:
        eqs.extend(gen_eq(t))
    return eqs


print(sym.solve(gen_eqs(known_translations), (a, b, c, d, e, f)))
