from dd import autoref as _bdd
import matplotlib.pyplot as plt
import time


def pigeonhole(n):
    "TODO: Implement your solution to the problem here."
    bdd = _bdd.BDD()

    holes = n - 1

    # Declare variables
    names = []
    for i in range(n):
        for j in range(holes):
            name = f"x_{i}_{j}"
            names.append(name)
            bdd.declare(name)

    vars = {name: bdd.var(name) for name in names}

    formula = bdd.true

    for i in range(n):
        clause = bdd.false
        for j in range(holes):
            clause |= vars[f"x_{i}_{j}"]
        formula &= clause

    for k in range(holes):
        for i in range(n):
            for j in range(i + 1, n):
                xi = vars[f"x_{i}_{k}"]
                xj = vars[f"x_{j}_{k}"]
                formula &= ~(xi & xj)

    # Check UNSAT
    if formula == bdd.false:
        print("UNSAT proven via BDD reduction.")
    else:
        print("Unexpected result.")

    return bdd, formula


if __name__ == "__main__":
    n_values = range(2, 10)  # increase until memory explodes
    runtimes = []
    node_counts = []

    for n in n_values:
        start = time.perf_counter()
        bdd, formula = pigeonhole(n)
        end = time.perf_counter()

        runtime = end - start
        runtimes.append(runtime)
        node_counts.append(len(bdd))

        print(
            f"n={n}, UNSAT? {formula == bdd.false}, "
            f"time={runtime:.4f}s, nodes={len(bdd)}"
        )

        # Optional cleanup
        bdd.collect_garbage()

    # Plot runtime
    plt.figure()
    plt.plot(n_values, runtimes, marker="o")
    plt.xlabel("n")
    plt.ylabel("Runtime (seconds)")
    plt.title("BDD Construction Time vs n")
    plt.grid(True)
    plt.show()

    # Plot node count
    plt.figure()
    plt.plot(n_values, node_counts, marker="o")
    plt.xlabel("n")
    plt.ylabel("Number of BDD nodes")
    plt.title("BDD Size vs n")
    plt.grid(True)
    plt.show()
