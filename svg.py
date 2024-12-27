from math import pi
from cmath import exp
import re

path_regex = re.compile(r's<path[^>]*d=\"((?P<d>[^"]*))"', re.MULTILINE)
pi2 = pi * pi
pi3 = pi2 * pi

def get_first_path(svg : str) -> str:
    with open(svg) as file:
        content = path_regex.search(file.read()).group("d")
        return content

def get_line_coefficients(start : complex, end : complex, N : int, n : int):
    coefficients = []
    a = start
    b = end - start
    for k in range(-n, n + 1):
        if k == 0:
            coefficients += [(start + end) / 2 / N]
        else:
            I = exp(-2j * pi * k / N)
            coefficients += [a * (I - 1) / pi / k * 0.5j + b * I / pi / k * 0.5j - b * N * (I - 1) / 4 / pi2 / k / k]
    return coefficients

def get_coefficients(path : str, n : int):
    N = 8
    l1 = get_line_coefficients(0 + 0j, 60 + 30*1.75j, N, n)
    l2 = get_line_coefficients(60 + 30*1.75j, 120 + 0j, N, n)
    l3 = get_line_coefficients(120 + 0j, 0 + 15*1.75j, N, n)
    l4 = get_line_coefficients(0 + 15*1.75j, 60 - 15*1.75j, N, n)
    l5 = get_line_coefficients(60 - 15*1.75j, 120 + 15*1.75j, N, n)
    l6 = get_line_coefficients(120 + 15*1.75j, 0 + 0j, N, n)
    l7 = get_line_coefficients(0 + 0j, 0 + 0j, N, n)
    l8 = get_line_coefficients(0 + 0j, 0 + 0j, N, n)

    lx = get_line_coefficients(15 + 0j, 0 + 0j, N, n)
    lx = get_line_coefficients(15 + 0j, 0 + 0j, N, n)
    coefficients = l1.copy()
    for T, l in enumerate([l2, l3, l4, l5, l6, l7, l8], start=1):
        for k, c in enumerate(l, start=-n):
            coefficients[k + n] += c * exp(-2j * pi * k / N * T)
    return coefficients
