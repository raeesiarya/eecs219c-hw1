from pysat.formula import CNF
from pysat.solvers import Solver
import time
import matplotlib.pyplot as plt


def pigeonhole(n: int):
    """
    Generates the CNF formula for the Pigeon-hole principle problem.

    The problem asks to place n pigeons into n-1 holes such that no hole
    contains more than one pigeon. This is inherently unsatisfiable.

    Args:
        n (int): The number of pigeons (implies n-1 holes).
    Returns:
        formula (CNF): A PySAT CNF formula representing the problem.
    """

    # TODO: Implement this function. Currently, this is a placeholder.
    # You must return a CNF object representing the encoding of the formula.
    formula = CNF()

    holes = n - 1

    # helper mapping
    def var(i, j):
        return i * holes + j + 1

    for i in range(n):
        clause = [var(i, j) for j in range(holes)]
        formula.append(clause)

    for k in range(holes):
        for i in range(n):
            for j in range(i + 1, n):
                formula.append([-var(i, k), -var(j, k)])

    return formula


# Example of plotting runtimes
def loop_n_times(n):
    i = 0
    while i < n:
        i += 1
    return i


if __name__ == "__main__":
    formula = pigeonhole(4)
    print(formula)

    ## Code for plotting
    n_values = range(4, 16)
    runtimes = []
    for n in n_values:
        start = time.time()
        loop_n_times(n)
        end = time.time()

        runtimes.append(end - start)

    plt.plot(n_values, runtimes, marker="o")
    plt.xlabel("n")
    plt.ylabel("Runtime (seconds)")
    plt.title("Function Runtime for Varying Values of n")
    plt.grid(True)
    plt.show()
