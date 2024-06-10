import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from pulp import *

def complete_or_fractionally_complete_latin_square(partial_square):
    n = len(partial_square)
    prob = LpProblem("FractionallyCompletableLatinSquare", LpMinimize)

    color = LpVariable.dicts("Color", (range(n), range(n), range(n)), lowBound=0, upBound=1)

    prob += 0

    for i in range(n):
        for j in range(n):
            prob += lpSum(color[i][j][k] for k in range(n)) == 1, f"Sum of colors in cell ({i},{j})"

    for k in range(n):
        for i in range(n):
            prob += lpSum(color[i][j][k] for j in range(n)) == 1, f"Color {k+1} sum in row {i}"
        for j in range(n):
            prob += lpSum(color[i][j][k] for i in range(n)) == 1, f"Color {k+1} sum in column {j}"

    for i in range(n):
        for j in range(n):
            if partial_square[i][j] != 0:
                for k in range(n):
                    if k == partial_square[i][j] - 1:
                        prob += color[i][j][k] == 1, f"Fixed color {k+1} in cell ({i},{j})"
                    else:
                        prob += color[i][j][k] == 0, f"Exclude color {k+1} from cell ({i},{j})"

    status = prob.solve()

    if LpStatus[status] == "Optimal":
        fig, axs = plt.subplots(n, n, figsize=(n, n))

        # Iterate over each cell to plot the color proportions
        for i in range(n):
            for j in range(n):
                ax = axs[i, j]
                bottom = 0  # Start filling from the bottom of the cell
                # Retrieve and plot each color proportion
                for k in range(n):
                    value_k = value(color[i][j][k])
                    if value_k > 0:
                        ax.bar(0, value_k, width=1, bottom=bottom, color=plt.cm.tab10.colors[k])
                        bottom += value_k
                ax.set_xlim(-0.5, 0.5)
                ax.set_ylim(0, 1)
                ax.axis('off')

        plt.tight_layout()
        plt.show()
    else:
        print("The square is not fractionally completable.")

partial_square = [
    [0, 0, 1, 2, 5, 3, 4],
    [2, 0, 0, 3, 1, 4, 0],
    [4, 1, 0, 0, 2, 6, 3],
    [3, 5, 4, 0, 0, 2, 1],
    [1, 2, 3, 4, 0, 0, 0],
    [0, 4, 6, 1, 3, 0, 2],
    [0, 3, 2, 0, 4, 1, 7]
]
complete_or_fractionally_complete_latin_square(partial_square)


