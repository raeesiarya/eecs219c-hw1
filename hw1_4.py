#! /usr/bin/python

#################################################################################
#                                                                               #
# Homework 1: 219C                                                              #
#                                                                               #
# Skeleton code with examples for Problem 4 (extra credits).                    #
#                                                                               #
# This uses the python pysat and sympy package.                                 #
#                                                                               #
# Authors: Shaokai Lin & Alejandro Sanchez                                      #
#                                                                               #
#################################################################################

from pysat.formula import CNF
from pysat.solvers import Solver
from sympy.logic.boolalg import And, Or, Not, Equivalent, Xor
from sympy import Symbol, to_cnf

################## Infrastructure code. Safe to ignore. ##################
def interpret_model(model, entities, num_steps):
    """
    Interpret the SAT solver's model output to map integers back to variable names,
    indicating the bank (west or east) based on the sign.
    
    :param model: The model output from the SAT solver.
    :param num_steps: The number of steps considered in the problem.
    :return: A dictionary with keys as steps and values as lists of entities on each bank.
    """
    # Mapping from integers back to variable names and steps
    # Assuming the mapping goes 1: A_0, 2: B_0, 3: C_0, ..., and so on
    variable_mapping = {}
    for step in range(num_steps):
        for i, entity in enumerate(entities, start=1):
            variable_mapping[i + step * len(entities)] = f'{entity}_{step}'
    
    # Interpret the model
    interpretation = {step: {'west': [], 'east': []} for step in range(num_steps)}
    for var in model:
        if var > 0:
            # Entity is on the west bank
            entity_step = variable_mapping[abs(var)]
            interpretation[int(entity_step.split('_')[1])]['west'].append(entity_step.split('_')[0])
        else:
            # Entity is on the east bank
            entity_step = variable_mapping[abs(var)]
            interpretation[int(entity_step.split('_')[1])]['east'].append(entity_step.split('_')[0])
    
    return interpretation

def check_success(interpretation, entities, num_steps):
    """
    Check if all entities are on the east bank at the last step.
    
    :param interpretation: The output from interpret_model function.
    :param num_steps: The number of steps considered in the problem.
    """
    last_step = num_steps - 1  # Indexing starts at 0, so last step is num_steps - 1
    
    # Check if all entities are on the east bank in the last step
    if all(entity in interpretation[last_step]['east'] for entity in entities):
        print("SUCCESS! Everybody arrives on the east bank!")
    else:
        print("But not everyone made it to the east bank. Try again. :)")
        
def is_valid_solution(interpretation, num_steps):
    """
    Check if the given interpretation of steps is a valid solution for the river
    crossing problem. 
    Note: This function must be revised if the entity names are changed.
    
    :param interpretation: The output from interpret_model function.
    :param num_steps: The number of steps considered in the problem.
    :return: True if the solution is valid, False otherwise.
    """
    for step in range(num_steps - 1):
        current_west = interpretation[step]['west']
        next_west = interpretation[step + 1]['west']
        current_east = interpretation[step]['east']
        next_east = interpretation[step + 1]['east']
        
        # Check for invalid alone situations
        if 'Goat' in next_west and 'Cabbage' in next_west and 'Sisyphus' not in next_west:
            print(f"Invalid move at step {step+1}: Goat and cabbage left alone without Sisyphus on the west bank.")
            return False
        if 'Goat' in next_east and 'Cabbage' in next_east and 'Sisyphus' not in next_east:
            print(f"Invalid move at step {step+1}: Goat and cabbage left alone without Sisyphus on the east bank.")
            return False
        if 'Goat' in next_west and 'Wolf' in next_west and 'Sisyphus' not in next_west:
            print(f"Invalid move at step {step+1}: Goat and wolf left alone without Sisyphus on the west bank.")
            return False
        if 'Goat' in next_east and 'Wolf' in next_east and 'Sisyphus' not in next_east:
            print(f"Invalid move at step {step+1}: Goat and wolf left alone without Sisyphus on the east bank.")
            return False
        
        # Check movement validity
        entities_moved_to_east = [entity for entity in current_west if entity not in next_west]
        entities_moved_to_west = [entity for entity in current_east if entity not in next_east]
        
        # Counting Sisyphus movement separately
        sisyphus_moves_to_east = 'Sisyphus' in entities_moved_to_east
        sisyphus_moves_to_west = 'Sisyphus' in entities_moved_to_west
        
        # Allow Sisyphus moving alone or with one entity
        if sisyphus_moves_to_east:
            entities_moved_to_east.remove('Sisyphus')
        if sisyphus_moves_to_west:
            entities_moved_to_west.remove('Sisyphus')

        # Checking if more than one entity (excluding Sisyphus) attempts to move
        if len(entities_moved_to_east) > 1 or len(entities_moved_to_west) > 1:
            print(f"Invalid move at step {step+1}: More than one entity moved.")
            return False

        # Ensuring Sisyphus is part of any move
        if len(entities_moved_to_east) > 0 and not sisyphus_moves_to_east:
            print(f"Invalid move at step {step+1}: Sisyphus did not move with the entity to the east.")
            return False
        if len(entities_moved_to_west) > 0 and not sisyphus_moves_to_west:
            print(f"Invalid move at step {step+1}: Sisyphus did not move with the entity to the west.")
            return False

    return True

def sympy_cnf_to_pysat_cnf(sympy_cnf, var_list):
    """
    Convert a SymPy CNF expression to a PySAT CNF clause list using a variable list
    for mapping, where the index corresponds to the PySAT integer ID.
    
    :param sympy_cnf: The CNF expression output by SymPy's to_cnf function.
    :param var_list: A list where the index is the PySAT integer and the element is the SymPy variable.
    :return: A list of lists where each inner list is a clause for PySAT.
    """
    pysat_clauses = []

    def walk_expression(expr):
        """
        Recursively walk through the SymPy expression to build clauses.
        """
        if isinstance(expr, And):
            # Handle conjunctions by iterating over arguments
            for arg in expr.args:
                result = walk_expression(arg)
                if isinstance(result[0], list):
                    pysat_clauses.extend(result)
                else:
                    pysat_clauses.append(result)
        elif isinstance(expr, Or):
            # Handle disjunctions by collecting literals into a single clause
            clause = []
            for arg in expr.args:
                if isinstance(arg, Not):
                    # Find the index of the negated variable and negate it
                    clause.append(-var_list.index(arg.args[0]) - 1)
                elif isinstance(arg, Symbol):
                    # Find the index of the positive variable
                    clause.append(var_list.index(arg) + 1)
                else:
                    raise ValueError(f"Unexpected expression type in Or: {type(arg)}")
            return clause
        elif isinstance(expr, Not):
            # Handle a single negated variable
            return [-var_list.index(expr.args[0]) - 1]
        elif isinstance(expr, Symbol):
            # Handle a single positive variable
            return [var_list.index(expr) + 1]
        else:
            raise ValueError(f"Unexpected expression type: {type(expr)}")
        return []

    # Start processing from the root of the expression
    walk_expression(sympy_cnf)

    return pysat_clauses

################## You can focus on the code below. ##################

# Globals need to be defined so helper functions can see them
cnf = CNF()
variables = {}
sympy_variables = []
entities = ['Goat', 'Wolf', 'Cabbage', 'Sisyphus']

# IMPORTANT: Helper function to get the variable
# Hint: The lines that set the "initial state" and "goal state" show how to use it.
def var(entity, step):
    _var = variables[f'{entity}_{step}']
    return sympy_variables[_var-1]

# IMPORTANT: Make sure to use this function to 
# add your constraint to a target CNF expression.
# Hint: The lines that set the "initial state" and "goal state" show how to use it.
# Fun: You can set sympy_simplify=False and print_cnf=True to appreciate how much
# work SymPy is doing for you...
def add_constraint(sympy_expr, sympy_simplify=True, print_cnf=False):
    sympy_cnf = to_cnf(sympy_expr, simplify=sympy_simplify)
    pysat_cnf = sympy_cnf_to_pysat_cnf(sympy_cnf, sympy_variables)
    if print_cnf: print(pysat_cnf)
    cnf.extend(pysat_cnf)

def solve_river_crossing(num_steps=8):
    """
    Main execution wrapper to allow for automated testing.

    Returns: result (bool), model (list), variables (dict)
    """
    global cnf, variables, sympy_variables, entities
    
    # Reset globals for fresh run
    cnf = CNF()

    # IMPORTANT: Create variables for each entity at each step
    # "True" represent the entity being on the west bank at step `t`,
    # "False" for the east bank.
    variables = {}
    sympy_variables = []
    entities = ['Goat', 'Wolf', 'Cabbage', 'Sisyphus']

    for t in range(num_steps):
        for entity in entities:
            var_name = f'{entity}_{t}'
            variables[var_name] = len(variables) + 1
            sympy_variables.append(Symbol(var_name))
        
    # Initial state: all entities on the west bank at step 0
    expr = True
    for entity in entities:
        expr = And(expr, var(entity, 0))
    add_constraint(expr)
        
    # Encode transitions and constraints for each step
    for t in range(num_steps-1):
        ### YOUR SOLUTION BEGINS ###
        # Hint: There should be around three main constraints, depending on your encoding. 
        pass
        ### YOUR SOLUTION ENDS ###
        
    # Goal state: everyone is on the east bank.
    # Hint: if you see "No solution exists," it helps to comment out constraints
    # like this one to debug your other constraints (unblocking the solver, so to speak).
    expr = True
    for entity in entities:
        expr = And(expr, Not(var(entity, num_steps-1)))
    add_constraint(expr)

    # Attempt to solve the SAT problem.
    solver = Solver(bootstrap_with=cnf)
    result = solver.solve()
    model = solver.get_model() if result else None
    
    # RETURN variables so tests can interpret the model correctly
    return result, model, variables



if __name__ == "__main__":
    # If the SAT encoding is correctly implemented, 
    # you don't need to change this number.
    num_steps = 8 # Number of steps considered
    
    result, model, vars_map = solve_river_crossing(num_steps)

    if result == True:
        # Interpret the model to construct the sequence of moves.
        interpretation = interpret_model(model, entities, num_steps)
        print("Solution found:")
        for step in interpretation:
            print(f'Step {step}: West Bank: {interpretation[step]["west"]}, East Bank: {interpretation[step]["east"]}')
        valid = is_valid_solution(interpretation, num_steps)
        if valid: check_success(interpretation, entities, num_steps)
        else: print("An invalid move detected. Please try again...")
    else:
        print("No solution exists. Please revise your encoding...")