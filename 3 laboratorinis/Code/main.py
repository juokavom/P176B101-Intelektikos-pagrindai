# Jokubas Akramas
# IFF-8/12
# 2021-04-29
from functools import reduce


def parse_int_if_can(number):
    try:
        parsed = int(number)
        return parsed
    except ValueError:
        return -1


def validate_input_data(data, min_val, max_val):
    return reduce(lambda prev, curr: prev and (min_val <= parse_int_if_can(curr) <= max_val), data, True)


# 2. Užkrauti failo turinį į darbinę atmintį.
sunspots = [x.split('\n')[0].split('\t') for x in open('sunspot.txt').readlines()]

(years, spots) = zip(*sunspots)

# 3. Patikrinti ar užkrauta atitinkama matrica – pirmas stulpelis atitinka metus,
# antras – saulės dienų aktyvumą
print(validate_input_data(years, 1700, 2021))
print(validate_input_data(spots, 0, 1000))
