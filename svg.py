from math import pi
from cmath import exp
import re

path_regex = re.compile(r'<path[^>]*d=\"((?P<d>[^"]*))"', re.MULTILINE)

class PathDescription:
    def __init__(self, text : str):
        self.commands = []
        content = [_ for _ in text.replace(",", " ").split() if _]
        for item in content:
            if item.isalpha():
                self.commands += [[item]]
            else:
                self.commands[-1] += [float(item)]

    def get_point(command : list[float], index : int):
        return command[index + 1] + 1j * command[index + 2]

    def scale(self, factor : float):
        pass

    def move(self, dx : float, dy : float):
        pass


def get_first_path_description(svg : str):
    with open(svg) as file:
        return PathDescription(path_regex.search(file.read()).group("d"))

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

def get_coefficients(path : PathDescription, n : int):
    N = len(path.commands) - 1 # don't take M into account
    if N < 1:
        raise Exception("There is no path!")
    if path.commands[0][0] != "M":
        raise Exception("First command should be M[move]!")
    initial_point = PathDescription.get_point(path.commands[0], 0)
    point = initial_point
    lines = []
    for cmd in path.commands[1:]:
        if cmd[0] == "M":
            raise Exception("Path description should contain only one M[move]!")
        elif cmd[0] == "L":
            next_point = PathDescription.get_point(cmd, 0)
            lines += [get_line_coefficients(point, next_point, N, n)]
            point = next_point
        elif cmd[0] == "C":
            first_control = PathDescription.get_point(cmd, 0)
            second_control = PathDescription.get_point(cmd, 2)
            next_point = PathDescription.get_point(cmd, 4)
            lines += [get_cubic_coefficients(point, first_control, second_control, next_point, N, n)]
            point = next_point
        elif cmd[0] == "z":
            lines += [get_line_coefficients(point, initial_point, N, n)]
        else:
            raise Exception(f"Command {{{cmd[0]}}} not supported!")
    coefficients = lines[0]
    for T, l in enumerate(lines[1:], start=1):
        for k, c in enumerate(l, start=-n):
            coefficients[k + n] += c * exp(-2j * pi * k / N * T)
    return coefficients
