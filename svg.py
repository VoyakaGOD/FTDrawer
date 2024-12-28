from math import pi
from cmath import exp
import re

path_regex = re.compile(r'<path[^>]*d=\"((?P<d>[^"]*))"', re.MULTILINE)
pi2 = pi * pi
pi3 = pi2 * pi

def get_first_path(svg : str) -> str:
    with open(svg) as file:
        return path_regex.search(file.read()).group("d")

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

def get_cubic_coefficients(start : complex, first_control : complex, second_control : complex, end : complex, N : int, n : int):
    coefficients = []
    a = start
    b = 3 * (first_control - start)
    c = 3 * second_control + 3 * start - 6 * first_control
    d = (end - start + 3 * first_control - 3 * second_control)
    for k in range(-n, n + 1):
        if k == 0:
            coefficients += [(a + b/2 + c/3) / N]
        else:
            I = exp(-2j * pi * k / N)
            alpha = (I - 1) / pi / k * 0.5j
            beta = I / pi / k * 0.5j - 0.5j * N * alpha / pi / k
            gamma = I / pi / k * 0.5j - 1j * N * beta / pi / k
            delta = I / pi / k * 0.5j - 1.5j * N * gamma / pi / k
            coefficients += [a * alpha + b * beta + c * gamma + d * delta]
    return coefficients

def get_coefficients(path : str, n : int):
    content = [_ for _ in path.replace(",", " ").split() if _]
    N = content.count("L") + content.count("C") + content.count("z")
    ptr = 0
    lines = []
    point = None
    initial_point = None
    while ptr < len(content):
        if content[ptr] == "M":
            point = float(content[ptr + 1]) + 1j * float(content[ptr + 2])
            initial_point = point
            ptr += 3
        elif content[ptr] == "L":
            next_point = float(content[ptr + 1]) + 1j * float(content[ptr + 2])
            lines += [get_line_coefficients(point, next_point, N, n)]
            point = next_point
            ptr += 3
        elif content[ptr] == "C":
            first_control = float(content[ptr + 1]) + 1j * float(content[ptr + 2])
            second_control = float(content[ptr + 3]) + 1j * float(content[ptr + 4])
            next_point = float(content[ptr + 5]) + 1j * float(content[ptr + 6])
            lines += [get_cubic_coefficients(point, first_control, second_control, next_point, N, n)]
            point = next_point
            ptr += 7
        elif content[ptr] == "z":
            lines += [get_line_coefficients(point, initial_point, N, n)]
            ptr += 1
        else:
            raise Exception(f"[{content[ptr]}]Not supported yet!!!")
    coefficients = lines[0]
    for T, l in enumerate(lines[1:], start=1):
        for k, c in enumerate(l, start=-n):
            coefficients[k + n] += c * exp(-2j * pi * k / N * T)
    return coefficients
