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
            alpha = (I - 1) / pi / k * 0.5j
            beta = I / pi / k * 0.5j - 0.5j * N * alpha / pi / k
            coefficients += [a * alpha + b * beta]
    return coefficients

def get_quadratic_coefficients(start : complex, control : complex, end : complex, N : int, n : int):
    coefficients = []
    a = start
    b = 2 * (control - start)
    c = (end + start - 2 * control)
    for k in range(-n, n + 1):
        if k == 0:
            coefficients += [(a + b/2 + c/3) / N]
        else:
            I = exp(-2j * pi * k / N)
            alpha = (I - 1) / pi / k * 0.5j
            beta = I / pi / k * 0.5j - 0.5j * N * alpha / pi / k
            gamma = I / pi / k * 0.5j - 1j * N * beta / pi / k
            coefficients += [a * alpha + b * beta + c * gamma]
    return coefficients

def get_qubic_coefficients(start : complex, first_control : complex, second_control : complex, end : complex, N : int, n : int):
    pass

def get_coefficients(path : str, n : int):
    N = 3
    l1 = get_line_coefficients(200 + 100j, 200 + 300j, N, n)
    l2 = get_quadratic_coefficients(200 + 300j, 200 + 100j, 100 + 100j, N, n)
    #l2 = get_line_coefficients(200 + 300j, 100 + 100j, N, n)
    l3 = get_line_coefficients(100 + 100j, 200 + 100j, N, n)

    lx = get_line_coefficients(15 + 0j, 0 + 0j, N, n)
    lx = get_line_coefficients(15 + 0j, 0 + 0j, N, n)
    coefficients = l1.copy()
    for T, l in enumerate([l2, l3], start=1):
        for k, c in enumerate(l, start=-n):
            coefficients[k + n] += c * exp(-2j * pi * k / N * T)
    return coefficients
