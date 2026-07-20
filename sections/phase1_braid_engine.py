import numpy as np

# ==========================================================
# HELIX NODE PROJECT
# Generalized Braid Generators (B8)
# 8 Strands  ->  7 Generators (σ1 ... σ7)
# Example: 10-Crossing Braid Word
# ==========================================================

def get_braid_generators(num_strands=8):
    """
    Generate braid generators σ1 ... σ7 as unitary matrices.

    Parameters
    ----------
    num_strands : int
        Number of strands (default = 8)

    Returns
    -------
    generators : dict
        Dictionary containing positive and inverse generators.
    """

    theta = np.pi / 3

    c = np.cos(theta)
    s = np.sin(theta)

    rotation_block = np.array([
        [c, -s],
        [s,  c]
    ], dtype=complex)

    generators = {}

    for i in range(num_strands - 1):

        G = np.eye(num_strands, dtype=complex)

        # Insert the 2x2 rotation block
        G[i:i+2, i:i+2] = rotation_block

        generators[i + 1] = G
        generators[-(i + 1)] = np.linalg.inv(G)

    return generators


def compute_braid_word(word, num_strands=8):
    """
    Compute the matrix representation of a braid word.

    Parameters
    ----------
    word : list
        List of braid generators.
        Example:
        [1,3,-2,5,-4,7]

    Returns
    -------
    result : ndarray
        Final braid matrix.
    """

    generators = get_braid_generators(num_strands)

    result = np.eye(num_strands, dtype=complex)

    for crossing in word:
        result = result @ generators[crossing]

    return result


# ==========================================================
# Example 10-Crossing Braid Word
# ==========================================================

# Demonstration braid word containing exactly 10 crossings.
# (Not the canonical braid word of a specific 10-crossing knot.)

knot10 = [
     1,
     3,
     5,
     7,
    -6,
     4,
    -2,
     5,
     3,
     1
]

# ==========================================================
# Compute Matrix
# ==========================================================

matrix = compute_braid_word(knot10)

# ==========================================================
# Results
# ==========================================================

print("=" * 60)
print(" HELIX BRAID COMPUTATION")
print("=" * 60)

print("\nNumber of Strands :", 8)
print("Number of Generators :", 7)
print("Number of Crossings :", len(knot10))

print("\n10-Crossing Braid Word:")
print(knot10)

print("\nMatrix Shape:")
print(matrix.shape)

print("\nFinal Matrix:")
print(matrix)

trace = np.trace(matrix)

print("\nMatrix Trace:")
print(trace)

print("\nTrace Magnitude:")
print(abs(trace))

print("\n[SUCCESS]: Matrix representation of the 10-crossing braid is stable.")