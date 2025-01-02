def lerp(start : int, end : int, t : float):
    if t < 0: return start
    if t > 1: return end
    return int(start + (end - start) * t)
