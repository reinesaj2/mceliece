# src/goppa_keygen.py

import numpy as np
import galois

def generate_goppa_polynomial(m: int, t: int):
    """
    Generate a random irreducible polynomial of degree t over GF(2^m).

    Args:
        m: The extension degree of GF(2^m)
        t: Degree of the Goppa polynomial (and the error-correcting capacity)

    Returns:
        g_poly: A Goppa polynomial over GF(2^m)
        GF: The finite field GF(2^m)
    """
    GF = galois.GF(2**m)
    # Generate a random irreducible polynomial of degree t
    g_poly = galois.irreducible_poly(GF, t)
    return g_poly, GF

def select_support_set(GF, n: int):
    """
    Select a support set L of size n from GF (all elements must be distinct).

    Args:
        GF: The finite field in use.
        n: The desired length of the code (n <= order of GF)

    Returns:
        An array of n distinct elements from GF.
    """
    if n > GF.order:
        raise ValueError("n must be less than or equal to the order of the finite field.")
    # Randomly select n distinct elements
    support = GF.Random(n)
    return support

def generate_parity_check_matrix(g_poly, support, GF):
    """
    Construct the parity-check matrix H for a Goppa code given a Goppa polynomial and support set L.

    Args:
        g_poly: The Goppa polynomial.
        support: Array containing the support set L.
        GF: The finite field of definition.

    Returns:
        A numpy array representing the parity-check matrix H.
    """
    n = len(support)
    t = g_poly.degree
    H = np.zeros((t, n), dtype=object)
    for j in range(n):
        # Evaluate g_poly at each support element
        g_val = g_poly(support[j])
        inv_g = 1 / g_val  # GF inversion (assumes g_val != 0)
        # Construct the column vector for the j-th support element
        for i in range(t):
            H[i, j] = support[j]**i * inv_g
    return H

def compute_generator_matrix(H, GF):
    """
    Compute the generator matrix G from the parity-check matrix H by finding its null space over GF.

    Args:
        H: The parity-check matrix as a numpy array.
        GF: The finite field.

    Returns:
        G: The generator matrix corresponding to H.
    """
    # Convert H to a Galois field array for proper finite field operations
    H_gf = galois.FieldArray(H, field=GF)
    
    # Use the null_space method of the FieldArray to compute the null space of H
    # The null_space method returns a basis for the null space with basis vectors as rows.
    G = H_gf.null_space()
    
    return G

def generate_keypair(m=4, t=2, n=16):
    """
    Generate a McEliece keypair using a genuine Goppa code.

    Args:
        m: Extension degree, determining the finite field GF(2^m)
        t: Error correction capacity (degree of the Goppa polynomial)
        n: Length of the code (n should be <= GF(2^m).order)

    Returns:
        public_key: The generator matrix (or its transformed version)
        private_key: A dictionary with components of the private key including g_poly, support, H, and G.
    """
    g_poly, GF = generate_goppa_polynomial(m, t)
    support = select_support_set(GF, n)
    H = generate_parity_check_matrix(g_poly, support, GF)
    G = compute_generator_matrix(H, GF)
    private_key = {
        "g_poly": g_poly,
        "support": support,
        "H": H,
        "G": G
    }
    public_key = G  # Later enhanced by applying random transformations S and P.
    return public_key, private_key

if __name__ == "__main__":
    pub, priv = generate_keypair()
    print("Public Key (Generator Matrix):", pub)
    print("Private Key Components:", priv)