import math

def golden_section_math(f, a, b, tol=1e-6):
    phi = (1 + math.sqrt(5)) / 2

    while b - a > tol:
        c = a + (b - a) * (3 - math.sqrt(5)) / 2
        d = a + (b - a) * (math.sqrt(5) - 1) / 2
        
        if f(c) < f(d):
            b = d
        else:
            a = c

    return (a + b) / 2