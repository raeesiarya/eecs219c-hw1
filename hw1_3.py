"""
Symbolic Learning via Boolean Satisfiability (SAT)
===================================================
Skeleton code for binary digit classification (0 vs 1) using a SAT solver.

You will implement a Boolean formula that classifies 8x8 binarized images of handwritten digits by framing the learning process as a SAT problem.

The formula processes each image row-by-row using a 4-bit state vector
V_{i,j} = [v^0, v^1, v^2, v^3] that is updated as a "scanner" reads
pixels left to right.  A Z3 SAT solver finds a universal set of Boolean
parameters (operators, initial conditions, final selection) that correctly
classifies every training image.
"""


# ========================================================================
# DO NOT MODIFY: Data Loading and Constraint Generation
# ========================================================================

import numpy as np
import z3
from sklearn.datasets import load_digits
from z3 import *
import matplotlib.pyplot as plt
import os
import numpy as np


# ============================================================================
# Data Loading & Preprocessing  (provided – do NOT modify)
# ============================================================================

def binarize_input(images: np.ndarray, threshold: float) -> np.ndarray:
    """Binarize pixel values: 1 if pixel >= threshold, else 0."""
    return np.where(images < threshold, 0, 1)




def save_images_to_disk(imagesm, label, folder_name="digit_images"):
    # Create the directory if it doesn't already exist
    # Convert binary (0/1) to 8-bit grayscale (0/255)
    # Using .astype(np.uint8) is good practice for image data
    images = (imagesm * 255).astype(np.uint8)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created directory: {folder_name}")


    for i in range(len(images)):
        # Construct a unique filename
        filename = f"{label}_{i}.png"
        filepath = os.path.join(folder_name, filename)

        plt.figure() # Start a new clean figure
        plt.imshow(images[i], cmap='gray')
        plt.title(f"Digit {i}")
        plt.axis('off') # Hide the 0-7 coordinates
        plt.savefig(filepath)
        plt.close() # CRITICAL: Free up memory

        # Save the 8x8 array as an image
        # cmap='gray_r' ensures 1s are black and 0s are white
        # plt.imsave(filepath, images[i])
        # plt.imsave(filepath, images[i], cmap='gray', format='png')
    print(f"Successfully saved {len(images)} images to '{folder_name}'.")


def load_dataset():
    """
    Load the sklearn digits dataset, filter to digits 0 and 1,
    binarize the images, and return train/test splits.

    Returns
    -------
    zeros_train, zeros_test : np.ndarray binarized 8x8 images of digit 0
    ones_train,  ones_test  : np.ndarray binarized 8x8 images of digit 1
    """
    digits = load_digits()
    X = digits.images          # shape (N, 8, 8)
    y = digits.target

    #filter the images with label 0 and label 1
    images_zeros = X[y == 0]
    images_ones  = X[y == 1]

    #we remove some corner-cases noisy images
    indices_to_remove = [14, 15, 17, 19, 22, 58, 130, 132, 135, 143, 144, 146, 147, 148, 149, 150, 152, 154, 155]
    images_ones = np.delete(images_ones, indices_to_remove, axis=0)

    #choose the threshold to be one-fourth
    max_brightness = max(np.max(images_zeros), np.max(images_ones))
    threshold = max_brightness / 4

    images_zeros = binarize_input(images_zeros, threshold)
    images_ones  = binarize_input(images_ones,  threshold)

    # For this problem we use the full set as both train and test.
    return images_zeros, images_ones


# ========================================================================
# END OF DO NOT MODIFY
# ========================================================================


# ============================================================================
# TODO  Q3 (i)  –  Initial Conditions
# ============================================================================

def initial_condition(zeros_train, ones_train):
    """
    Generate a conjunction of constraints enforcing that
    all initial state bits are equal to a single learnable constant.

    This function introduces a single global Boolean variable and enforces the constraint 
    that every initial state bit v_{i,0}^k must be the value of that variable.
    This applies across all training images (both 0s and 1s), all rows within those images, 
    and all state bits (k=0 to 3).

    Parameters
    ----------
    zeros_train : numpy.ndarray or list
        Training data for digit '0'. Structure is expected to be (num_samples, num_rows, num_cols).
    ones_train : numpy.ndarray or list
        Training data for digit '1'. Structure is expected to be (num_samples, num_rows, num_cols).

    Returns
    -------
    z3.BoolRef
        A Z3 conjunction (And) of constraints. This expression forces every initial state variable `v_{...}` to be equal to a common-value.
    """

    # >>> YOUR CODE HERE <<<
    
    # Placeholder example to demonstrate Z3 syntax (Replace this with your logic):
    a = z3.Bool("BEST")
    course_code = 219
    b = z3.Bool(f"EECS{course_code}C")
    formulae = [a, z3.Implies(z3.Bool("EECS219C"), z3.Bool("BEST")), a != b]
    return z3.And(formulae)
    
    raise NotImplementedError


# ============================================================================
# TODO  Q3 (ii) & (iii)  –  Update Rules
# ============================================================================
def update_rules(zeros_train, ones_train):
    """
    Generate a conjunction of constraints governing the state transition from column j to j+1.

    Parameters
    ----------
    zeros_train : numpy.ndarray
        Training data for digit '0'.
    ones_train : numpy.ndarray
        Training data for digit '1'.
    
    Returns
    -------
    z3.BoolRef
        A Z3 conjunction (And) of constraints.
    """

    # >>> YOUR CODE HERE <<<
    raise NotImplementedError


# ============================================================================
# TODO  Q3 (iv)  –  Final Selection
# ============================================================================

def final_selection(zeros_train, ones_train):
    """
    Generate Z3 constraints to aggregate the final states of all rows and select the classification output.

    Parameters
    ----------
    zeros_train : numpy.ndarray
        Training data for digit '0'.
    ones_train : numpy.ndarray
        Training data for digit '1'.

    Returns
    -------
    z3.BoolRef
        A Z3 conjunction (And) of constraints.
    """
    # >>> YOUR CODE HERE <<<
    raise NotImplementedError



# ============================================================================
# Training loop  (Needs Some Modification)
# ============================================================================

def train():
    """Invoke Z3 to `learn' parameters that classify all training images."""

    # ========================================================================
    # DO NOT MODIFY: Data Loading and Constraint Generation
    # ========================================================================
    zeros_train, ones_train = load_dataset()

    # Constructing the solver
    solver = Solver()

    # 1. Add Initial Condition Constraints
    formula_encoding_initial_condition = initial_condition(zeros_train, ones_train)
    solver.add(formula_encoding_initial_condition)

    # 2. Add Rule Constraints
    formula_encoding_update_rule = update_rules(zeros_train, ones_train)
    solver.add(formula_encoding_update_rule)

    # 3. Add Final Selection Constraints
    formula_encoding_final_selection = final_selection(zeros_train, ones_train)
    solver.add(formula_encoding_final_selection)

    # Check for satisfiability
    result = solver.check()
    print(f"Result: {result}")
    # ========================================================================
    # END OF DO NOT MODIFY
    # ========================================================================

    if result == z3.sat:
        # ====================================================================
        # TODO Q6: Extract and Print Learned Parameters
        # ====================================================================
        # Use model.eval() to output the assigned values for:
        # 1. The initial condition constant
        # 2. The update rule operators (AND vs OR)
        # 3. The final selection bit index
        
        model = solver.model()
        print("\n=== Learned Parameters ===")
        
        # >>> YOUR CODE HERE <<<
        # Example: print("Init Constant:", model.eval(z3.Bool("your_var_name")))

    else:
        print("Uh oh! No satisfying assignment found.")


if __name__ == "__main__":
    train()
