from dd import autoref as _bdd


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

    return formula


if __name__ == "__main__":
    pigeonhole(6)
