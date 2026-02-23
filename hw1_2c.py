import math

from dd import autoref as _bdd


def nlogn_pigeonhole(n):
    print(f"[O(n log n) Pigeonhole encoding for n={n}]")

    bdd = _bdd.BDD()

    holes = n - 1
    bits = math.ceil(math.log2(holes))

    for i in range(n):
        for b in range(bits):
            bdd.declare(f"p{i}_b{b}")

    def pigeon_bits(i):
        return [bdd.var(f"p{i}_b{b}") for b in range(bits)]

    formula = bdd.true

    for i in range(n):
        valid = bdd.false

        # allow only values 0..holes-1
        for h in range(holes):
            assignment = bdd.true
            for b in range(bits):
                bit = (h >> b) & 1
                v = bdd.var(f"p{i}_b{b}")
                assignment &= v if bit else ~v
            valid |= assignment

        formula &= valid

    for i in range(n):
        for j in range(i + 1, n):
            equal = bdd.true
            for b in range(bits):
                xi = bdd.var(f"p{i}_b{b}")
                xj = bdd.var(f"p{j}_b{b}")

                # bit equality
                equal &= (xi & xj) | (~xi & ~xj)

            # forbid equality
            formula &= ~equal

    if formula == bdd.false:
        print("UNSAT proven with O(n log n) encoding.")
    else:
        print("Unexpected SAT result.")

    return formula


if __name__ == "__main__":
    nlogn_pigeonhole(4)
