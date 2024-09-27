from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt


def complete_or_integrally_complete_latin_square(partial_square):
    """
    Function to check if a partial Latin square can be completed integrally.
    """
    n = len(partial_square)
    solver = pywraplp.Solver.CreateSolver('CBC')

    if not solver:
        print("Solver not created.")
        return False

    color = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                color[(i, j, k)] = solver.BoolVar(f'color_{i}_{j}_{k}')

    # Each cell must contain exactly one color
    for i in range(n):
        for j in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for k in range(n)]) == 1)

    # Each color must appear exactly once in each row
    for k in range(n):
        for i in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for j in range(n)]) == 1)

    # Each color must appear exactly once in each column
    for k in range(n):
        for j in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for i in range(n)]) == 1)

    for i in range(n):
        for j in range(n):
            if partial_square[i][j] != 0:
                k = partial_square[i][j] - 1
                solver.Add(color[(i, j, k)] == 1)
                for k_prime in range(n):
                    if k_prime != k:
                        solver.Add(color[(i, j, k_prime)] == 0)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        fig, axs = plt.subplots(n, n, figsize=(n, n))
        for i in range(n):
            for j in range(n):
                ax = axs[i, j]
                bottom = 0
                for k in range(n):
                    value_k = color[(i, j, k)].solution_value()
                    if value_k > 0:
                        ax.bar(0, value_k, width=1, bottom=bottom, color=plt.cm.tab10.colors[k])
                        bottom += value_k
                    ax.set_xlim(-0.5, 0.5)
                    ax.set_ylim(0, 1)
                    ax.axis('off')
        
        plt.tight_layout()
        plt.show()
        return True
    else:
        return False


def complete_or_fractionally_complete_latin_square(partial_square):
    """
    Function to check if a partial Latin square can be fractionally completed.
    """
    n = len(partial_square)
    solver = pywraplp.Solver.CreateSolver('GLOP')

    if not solver:
        print("Solver not created.")
        return False

    color = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                color[(i, j, k)] = solver.NumVar(0, 1, f'color_{i}_{j}_{k}')

    # Each cell must contain exactly one color
    for i in range(n):
        for j in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for k in range(n)]) == 1)

    # Each color must appear exactly once in each row
    for k in range(n):
        for i in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for j in range(n)]) == 1)

    # Each color must appear exactly once in each column
    for k in range(n):
        for j in range(n):
            solver.Add(solver.Sum([color[(i, j, k)] for i in range(n)]) == 1)

    for i in range(n):
        for j in range(n):
            if partial_square[i][j] != 0:
                k = partial_square[i][j] - 1
                solver.Add(color[(i, j, k)] == 1)
                for k_prime in range(n):
                    if k_prime != k:
                        solver.Add(color[(i, j, k_prime)] == 0)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        fig, axs = plt.subplots(n, n, figsize=(n, n))
        for i in range(n):
            for j in range(n):
                ax = axs[i, j]
                bottom = 0
                for k in range(n):
                    value_k = color[(i, j, k)].solution_value()
                    if value_k > 0:
                        ax.bar(0, value_k, width=1, bottom=bottom, color=plt.cm.tab10.colors[k])
                        bottom += value_k
                ax.set_xlim(-0.5, 0.5)
                ax.set_ylim(0, 1)
                ax.axis('off')

        plt.tight_layout()
        plt.show()
        return True
    else:
        return False


def check_latin_square_completability(partial_square):
    if complete_or_integrally_complete_latin_square(partial_square):
        print("The partial Latin square is integrally completable!")
    elif complete_or_fractionally_complete_latin_square(partial_square):
        print("The partial Latin square is fractionally completable!")
    else:
        print("The partial Latin square is not completable in any form.")


def input_partial_latin_square():
    """
    Function to input the partial Latin square from the console.
    """
    n = int(input("Enter the dimension (n) of the Latin square: "))
    
    print(f"Enter the partial Latin square with rows one by one:")
    partial_square = []
    
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != n:
            raise ValueError(f"Each row must have {n} elements.")
        partial_square.append(row)
    
    return partial_square

partial_square = input_partial_latin_square()
check_latin_square_completability(partial_square)
