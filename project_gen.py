import itertools


def is_valid_partial_latin_square(square, n):
    """
    Check if the current square is a valid partial Latin square.
    """
    for i in range(n):
        row_vals = [x for x in square[i] if x is not None]
        if len(row_vals) != len(set(row_vals)):
            return False
        col_vals = [square[j][i] for j in range(n) if square[j][i] is not None]
        if len(col_vals) != len(set(col_vals)):
            return False
    return True


def generate_partial_latin_squares(n, s):
    """
    Generate all partial Latin squares of size n*n with order s.
    """
    if s > n * n:
        raise ValueError("Order s cannot be greater than n*n")

    positions = list(itertools.product(range(n), range(n)))

    for filled_positions in itertools.combinations(positions, s):
        for values in itertools.product(range(1, n + 1), repeat=s):
            square = [[None for _ in range(n)] for _ in range(n)]
            valid = True
            for pos, val in zip(filled_positions, values):
                square[pos[0]][pos[1]] = val
                if not is_valid_partial_latin_square(square, n):
                    valid = False
                    break
            if valid:
                yield square


def print_square(square):
    for row in square:
        print(' '.join(str(x) if x is not None else '.' for x in row))


n = 5  # Size of the Latin square (n x n)
s = 13  # Order of the partial Latin square (number of filled cells)

print(f"Partial Latin Squares of size {n}x{n} with order {s}:\n")
i = 1
for square in generate_partial_latin_squares(n, s):
    print(f"Partial Latin Square {i}:")
    print_square(square)
    print()
    i += 1




