from pysat.formula import CNF
from pysat.solvers import Solver


def create_and_solve_psi():
    """
    Part 1: Create a specific CNF formula and solve it.

    Returns:
        tuple: (psi, model)
        - psi (CNF): The PySAT CNF object.
        - model (list): A list of integers representing the satisfying assignment.
    """
    # TODO: Initialize your CNF formula here
    psi = CNF()

    psi.append([-1, 2])
    psi.append([-2, 3])
    psi.append([-3, 4])

    solver = Solver(bootstrap_with=psi)
    sat = solver.solve()

    model = solver.get_model() if sat else []

    solver.delete()

    return psi, model


def modify_and_check(psi):
    """
    Part 2: Modify an existing formula and check satisfiability.

    Args:
        psi (CNF): The formula object from Part 1.

    Returns:
        tuple: (psi, is_satisfiable)
        - psi: The modified CNF object (with the new clause).
        - is_satisfiable: Boolean (True if satisfiable, False otherwise).
    """
    psi.append([-4, -1])

    solver = Solver(bootstrap_with=psi)
    is_satisfiable = solver.solve()

    solver.delete()

    return psi, is_satisfiable


def add_assumptions(psi):
    """
    Part 3: Incremental SAT solving.

    Args:
        psi (CNF): The formula object from Part 2.

    Returns:
        tuple: (status, result)
        - status (bool): True if satisfiable, False if unsatisfiable.
        - result (list): The model (if status is True) or the unsatisfiable core (if status is False).
    """
    solver = Solver(bootstrap_with=psi)

    # Assumptions: (x1 ∧ x2 ∧ x3 ∧ x4)
    status = solver.solve(assumptions=[1, 2, 3, 4])
    result = solver.get_model() if status else solver.get_core()

    solver.delete()

    return status, result


if __name__ == "__main__":
    # You can use this block to test your code locally
    print("--- Testing Part 1 ---")
    my_psi, my_model = create_and_solve_psi()
    print(f"Clauses: {my_psi.clauses}")
    print(f"Model: {my_model}")

    print("\n--- Testing Part 2 ---")
    my_psi, is_sat = modify_and_check(my_psi)
    print(f"Modified Clauses: {my_psi.clauses}")
    print(f"Is Satisfiable?: {is_sat}")

    print("\n--- Testing Part 3 ---")
    status, result = add_assumptions(my_psi)
    if status:
        print(f"Satisfiable with Model: {result}")
    else:
        print(f"Unsatisfiable with Core: {result}")
