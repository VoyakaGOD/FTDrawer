from math import pi
import re

path_regex = re.compile(r's<path[^>]*d=\"((?P<d>[^"]*))"', re.MULTILINE)
pi2 = pi * pi
pi3 = pi2 * pi

def I(k : int):
    return 1 if (k % 2 == 0) else -1

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
            coefficients += [(start + end) / 2]
        else:
            coefficients += [a * (I(k) - 1) / pi / k * 1j + b * I(k) / pi / k * 1j - b * (I(k) - 1) / pi2 / k / k]
            #coefficients += [b / pi / k]
    return coefficients

def get_coefficients(path : str, n : int):
    l1 = get_line_coefficients(0 + 0j, 200 + 200j, 2, n)
    l2 = get_line_coefficients(200 + 200j, 0 + 0j, 2, n)
    l3 = get_line_coefficients(800 + 300j, 900 + 0j, 2, n)
    l4 = get_line_coefficients(900 + 0j, 0j, 2, n)
    coefficients = l1.copy()
    for k, c in enumerate(l2, start=-n):
        coefficients[k + n] += c * I(k)
        coefficients[k + n] /= 2
    return coefficients
