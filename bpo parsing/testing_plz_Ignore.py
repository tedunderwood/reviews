import ast
import pandas as pd

from itertools import groupby
x = [0, 1, 2, 3, 4, 5, 6, 7]

def projection(val):
    return val % 3
set=[{1,2},{2,3}]

x_sorted = sorted(x, key=projection)
print(x_sorted)

x_grouped = [list(it) for k, it in groupby(x_sorted, projection)]
print(x_grouped)

#[[0, 3, 6], [1, 4, 7], [2, 5]]