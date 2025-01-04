from math import pi
from cmath import exp
from pygame import Rect, Vector2
import re

path_regex = re.compile(r'<path[^>]*d=\"((?P<d>[^"]*))"', re.MULTILINE)
command_regex = re.compile(r'([a-zA-Z])([^a-zA-Z]*)', re.MULTILINE)
separators_regex = re.compile(r'[,\n\t\r]')

class PathDescription:
    def __init__(self, text : str):
        self.commands = []
        text = separators_regex.sub(" ", text).replace("-", " -")
        for cmd in command_regex.findall(text):
            content = [_ for _ in cmd[1].split() if _]
            self.commands += [[cmd[0]] + [float(x) for x in content]]

    def get_point(command : list[float], index : int):
        return command[index + 1] + 1j * command[index + 2]

    def scale(self, factor : float):
        for cmd in self.commands:
            for i in range(1, len(cmd)):
                cmd[i] *= factor

    def move(self, dx : float, dy : float):
        for cmd in self.commands:
            if cmd[0].islower():
                continue
            if cmd[0] == "H":
                cmd[1] += dx
            elif cmd[0] == "V":
                cmd[1] += dy
            else:
                for i in range(1, len(cmd), 2):
                    cmd[i] += dx
                    cmd[i + 1] += dy

    # returns not the exact bounding rect
    def get_bounding_rect(self):
        if (len(self.commands) == 0) or (self.commands[0][0] != "M"):
            raise Exception("Invalid PathDescription!")
        min_x = max_x = self.commands[0][1]
        min_y = max_y = self.commands[0][2]
        point = (0, 0)
        for cmd in self.commands:
            shift = point if cmd[0].islower() else (0, 0) 
            if cmd[0].upper() == "H":
                new_x = cmd[1] + shift[0]
                min_x = min(min_x, new_x)
                max_x = max(max_x, new_x)
                point = new_x, point[1]
                continue
            if cmd[0].upper() == "V":
                new_y = cmd[1] + shift[1]
                min_y = min(min_y, new_y)
                max_y = max(max_y, new_y)
                point = point[0], new_y
                continue
            for i in range(1, len(cmd) - 1, 2):
                min_x = min(min_x, cmd[i] + shift[0])
                max_x = max(max_x, cmd[i] + shift[0])
                min_y = min(min_y, cmd[i + 1] + shift[1])
                max_y = max(max_y, cmd[i + 1] + shift[1])
            if len(cmd) != 1: # not Z/z
                point = cmd[1] + shift[0], cmd[2] + shift[1]
        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def fit_in(self, size : Vector2):
        self_rect = self.get_bounding_rect()
        ratio = min(size.x / self_rect.width, size.y / self_rect.height)
        self.scale(ratio)
        self.move(-self_rect.center[0] * ratio, -self_rect.center[1] * ratio)

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
    last_control_point = None # for S/s T/t
    lines = []
    for cmd in path.commands[1:]:
        shift = point if cmd[0].islower() else 0
        cmd[0] = cmd[0].upper()
        if cmd[0] in "MLHV":
            if cmd[0] == "M":
                print("WARNING: Path description contains extra M/m[move]!")
            if cmd[0] == "H":
                next_point = (cmd[1] + shift.real) + 1j * point.imag
            elif cmd[0] == "V":
                next_point = point.real + 1j * (cmd[1] + shift.imag)
            else:
                next_point = PathDescription.get_point(cmd, 0) + shift
            lines += [get_line_coefficients(point, next_point, N, n)]
            point = next_point
        elif cmd[0] in "CS":
            if cmd[0] == "C":
                first_control = PathDescription.get_point(cmd, 0) + shift
                next_index = 2
            else:
                first_control = 2 * point - last_control_point
                next_index = 0
            second_control = PathDescription.get_point(cmd, next_index) + shift
            next_point = PathDescription.get_point(cmd, next_index + 2) + shift
            lines += [get_cubic_coefficients(point, first_control, second_control, next_point, N, n)]
            point = next_point
            last_control_point = second_control
        elif cmd[0] in "TQ":
            if cmd[0] == "Q":
                control = PathDescription.get_point(cmd, 0) + shift
                next_index = 2
            else:
                control = 2 * point - last_control_point
                next_index = 0
            next_point = PathDescription.get_point(cmd, next_index) + shift
            lines += [get_quadratic_coefficients(point, control, next_point, N, n)]
            point = next_point
            last_control_point = control
        elif cmd[0] == "Z":
            lines += [get_line_coefficients(point, initial_point, N, n)]
        else:
            raise Exception(f"Command {{{cmd[0]}}} not supported!") # no support planned for A/a
    coefficients = lines[0]
    for T, l in enumerate(lines[1:], start=1):
        for k, c in enumerate(l, start=-n):
            coefficients[k + n] += c * exp(-2j * pi * k / N * T)
    return coefficients
