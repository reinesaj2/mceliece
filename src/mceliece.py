# src/mceliece.py

import numpy as np


def _generate_random_invertible_matrix(n, rng):
    """Generates a random n x n invertible matrix over GF(2)."""
    while True:
        matrix = rng.integers(0, 2, size=(n, n))
        if np.linalg.det(matrix) % 2 != 0:
            return matrix


def _generate_random_permutation_matrix(n, rng):
    """Generates a random n x n permutation matrix."""
    identity = np.identity(n, dtype=int)
    return rng.permutation(identity)


def _compute_inverse_matrix(matrix):
    """Computes the inverse of a matrix over GF(2)."""
    n = matrix.shape[0]
    identity = np.identity(n, dtype=int)
    
    # Use Gaussian elimination to find the inverse
    # Augment the matrix with the identity matrix
    aug_matrix = np.hstack((matrix, identity))
    
    for i in range(n):
        # Find pivot
        pivot = i
        while pivot < n and aug_matrix[pivot, i] == 0:
            pivot += 1
        if pivot == n:
            raise ValueError("Matrix is not invertible") # Should not happen if generated correctly
        
        # Swap rows
        aug_matrix[[i, pivot]] = aug_matrix[[pivot, i]]
        
        # Eliminate other rows
        for j in range(n):
            if i != j and aug_matrix[j, i] == 1:
                aug_matrix[j] = (aug_matrix[j] + aug_matrix[i]) % 2
                
    # The right half is now the inverse
    inverse = aug_matrix[:, n:]
    return inverse


def _decode_simple(G, y_prime, t, rng):
    """
    Simulates decoding for a simple code G, assuming it can correct t errors.
    For real McEliece, this uses an efficient decoder for the specific code family (e.g., Goppa).
    Here, we find the codeword c = mSG such that HammingDistance(y_prime, c) <= t.
    This is simplified: we assume the original mSG is the *closest* codeword.
    In a real scenario, the private G has structure enabling efficient search.
    For this example, we'll cheat slightly by knowing the structure implicitly.

    A more realistic simulation for *any* G would involve calculating syndromes
    or using more complex decoding algorithms (like Syndrome Decoding or Guava in Sage),
    but that adds significant complexity beyond the scope of illustrating the McEliece *structure*.

    This placeholder finds the codeword c in the codespace of G closest to y_prime.
    WARNING: This is computationally expensive and not how real McEliece works,
             but suffices to demonstrate the unscrambling principle.
             For a small example, we can sometimes infer the intended codeword
             if the error vector is known or if the codespace is very small.

    Let's simplify further for demonstration: assume y_prime = mSG + e_prime.
    If we *knew* e_prime, we could find mSG = y_prime - e_prime.
    The actual decoder for G finds e_prime (or equivalently mSG).

    Since we don't have a real decoder for an arbitrary G, we'll simulate
    finding the *intended* mSG based on how we construct the example later.
    This function will be less general and more tied to the example construction.
    We will refine this when implementing the examples.

    For now, let's return a placeholder or raise NotImplementedError.
    We'll fill this in properly when we call it from the decrypt function
    in the context of the specific example.
    """
    # Placeholder: In a real decoder for G, we'd find mS*G from y_prime.
    # Since we don't have that, we will handle the "decoding" logic
    # more directly within the decrypt function for this example,
    # using knowledge of the constructed error.
    raise NotImplementedError("Generic decoding simulation is complex. Implement within decrypt context.")


def key_generation(k, n, t, seed=None):
    """
    Generates McEliece public and private keys.

    Args:
        k (int): Dimension of the code (message length).
        n (int): Length of the codewords.
        t (int): Error correction capability of the code.
        seed (int, optional): Seed for the random number generator. Defaults to None.

    Returns:
        tuple: (public_key, private_key)
               public_key: Dictionary {'G_prime': G_prime, 't': t}
               private_key: Dictionary {'S': S, 'G': G, 'P': P, 'S_inv': S_inv, 'P_inv': P_inv}
    """
    rng = np.random.default_rng(seed)

    # 1. Generate the private Generator matrix G for a code (k x n)
    #    In real McEliece, this G belongs to a family with efficient decoding (e.g., Goppa).
    #    For this example, we generate a random G.
    #    WARNING: A random G usually doesn't have an efficient decoding algorithm.
    #             This is purely for demonstrating the scrambling mechanism.
    #             We assume 't' is achievable by this hypothetical code G.
    G = rng.integers(0, 2, size=(k, n))
    # TODO: Ensure G has rank k? For simplicity, assume it does for now.

    # 2. Generate a random invertible scrambling matrix S (k x k)
    S = _generate_random_invertible_matrix(k, rng)
    S_inv = _compute_inverse_matrix(S) # Precompute for decryption

    # 3. Generate a random permutation matrix P (n x n)
    P = _generate_random_permutation_matrix(n, rng)
    P_inv = P.T # Inverse of a permutation matrix is its transpose

    # 4. Compute the public key G_prime = S * G * P (modulo 2)
    G_prime = (S @ G @ P) % 2

    public_key = {'G_prime': G_prime, 't': t}
    private_key = {'S': S, 'G': G, 'P': P, 'S_inv': S_inv, 'P_inv': P_inv}

    return public_key, private_key


def encrypt(message, public_key, seed=None):
    """
    Encrypts a message using the McEliece public key.

    Args:
        message (np.ndarray): The message vector (1 x k) of 0s and 1s.
        public_key (dict): The public key dictionary containing G_prime and t.
        seed (int, optional): Seed for the random number generator. Defaults to None.

    Returns:
        np.ndarray: The ciphertext vector y (1 x n).
    """
    rng = np.random.default_rng(seed)
    G_prime = public_key['G_prime']
    t = public_key['t']
    k = G_prime.shape[0] # Public key G' is k x n
    n = G_prime.shape[1]

    if message.shape != (1, k):
        raise ValueError(f"Message must be a 1x{k} numpy array.")
    if not np.all(np.logical_or(message == 0, message == 1)):
         raise ValueError("Message must contain only 0s and 1s.")

    # 1. Compute intermediate ciphertext c_prime = message * G_prime (mod 2)
    c_prime = (message @ G_prime) % 2

    # 2. Generate a random error vector e of length n with weight t
    error_vector = np.zeros(n, dtype=int)
    error_indices = rng.choice(n, t, replace=False)
    error_vector[error_indices] = 1
    error_vector = error_vector.reshape(1, n) # Ensure shape is 1xn

    # 3. Compute final ciphertext y = c_prime + e (mod 2)
    y = (c_prime + error_vector) % 2

    # Return the error vector as well for demonstration/decoding simulation purposes
    # In a real system, the error vector is NOT returned.
    return y, error_vector


def decrypt(ciphertext, private_key):
    """
    Decrypts a ciphertext using the McEliece private key.

    Args:
        ciphertext (np.ndarray): The ciphertext vector y (1 x n).
        private_key (dict): The private key dictionary containing S, G, P, S_inv, P_inv.

    Returns:
        np.ndarray: The decrypted message vector (1 x k).
    """
    S_inv = private_key['S_inv']
    G = private_key['G'] # The private generator matrix
    P_inv = private_key['P_inv']
    # We also need t and the *actual* efficient decoding algorithm for G.

    # 1. Undo the permutation: y_prime = y * P_inv (mod 2)
    y_prime = (ciphertext @ P_inv) % 2

    # 2. Decode y_prime to find mSG using the secret decoder for G.
    #    y_prime = mSG + e_prime, where e_prime = e * P_inv has weight t.
    #    The decoder should remove e_prime to find mSG.
    #
    #    SIMULATION: Since we used a random G and don't have its specific decoder,
    #    we cannot implement the true decoding step generically here.
    #    In a real system, this step uses the structure of G (e.g., Patterson algorithm for Goppa).
    #
    #    WORKAROUND for EXAMPLE: Assume the 'decode' step magically recovers mSG.
    #    In the example scripts, we might pass the known error vector 'e' to decrypt
    #    to simulate this perfectly, or implement a brute-force nearest codeword search
    #    if k and n are tiny. Let's assume for now the ideal decoder recovers mSG.
    #    We need information (like the original error vector e' or the message mS)
    #    that only the specific decoder for G would provide.

    #    Let's define mSG_recovered conceptually. How do we get it?
    #    If we passed the original 'e' to decrypt for simulation:
    #       e_prime = (e @ P_inv) % 2
    #       mSG_recovered = (y_prime - e_prime + 2) % 2 # Add 2 for correct modulo arithmetic
    #    This bypasses the actual decoding algorithm but shows the structure.

    # Placeholder for the result of the decoding step:
    # mSG_recovered = _decode_simple(G, y_prime, t, ???) # Requires t and potentially rng state or error knowledge

    # For now, raise error, requiring the example script to handle the "decoding" simulation.
    raise NotImplementedError(
        "Decryption requires the specific decoding algorithm for the private G "
        "or simulation knowledge (like the error vector) not available in this generic function."
        " The calling example script needs to handle the decoding simulation."
        )

    # 3. Recover the original message: m = (mSG) * S_inv (mod 2)
    #    This step requires recovering mS from mSG first.
    #    If G is in systematic form G = [I_k | Q], then the first k bits of mSG are mS.
    #    If G is not systematic, we need its inverse or pseudo-inverse.
    #    Assume G is k x n with k <= n. We need a way to get mS from mSG.
    #    If G had a right inverse G_right_inv (n x k), then mSG * G_right_inv = mS.
    #    Calculating a right inverse also involves techniques like Gaussian elimination.

    #    Let's assume we recovered mS (the first k bits if G was systematic).
    #    mS_recovered = mSG_recovered[:, :G.shape[0]] # Simplistic assumption

    #    message_recovered = (mS_recovered @ S_inv) % 2

    # return message_recovered


if __name__ == "__main__":
    # For quick testing of this module
    pub, priv = key_generation(3, 5, 1)
    m = np.array([1, 0, 1])
    c, e = encrypt(m, pub)
    r = decrypt(c, priv)
    print("Message:", m, "Ciphertext:", c, "Recovered:", r)
