# src/goppa_crypto.py

import numpy as np
import galois
from goppa_keygen import generate_keypair


def encrypt(message, public_key, GF, error_weight=None):
    """
    Encrypt a message using the public key.

    Args:
        message: A 1D Galois Field array representing the message vector of length k.
        public_key: The public key matrix (S * G * P) of shape (k, n).
        GF: The finite field.
        error_weight: The number of errors to introduce (default: 1 if not provided).

    Returns:
        ciphertext: The encrypted vector of length n.
        error_vector: The error vector added (for debugging).
    """
    k, n = public_key.shape
    if error_weight is None:
        error_weight = 1  # Default error weight

    # Initialize a zero error vector
    error_vector = GF.Zeros(n)

    # Randomly select positions to inject errors
    positions = np.random.choice(n, size=error_weight, replace=False)
    for pos in positions:
        # Ensure a nonzero error is added
        while True:
            error_value = GF.Random()
            if error_value != 0:
                break
        error_vector[pos] = error_value

    ciphertext = message @ public_key + error_vector
    return ciphertext, error_vector


def brute_force_decode(c_prime, G, GF, t):
    """
    Brute-force decode the message from c_prime given the generator matrix G.

    Args:
        c_prime: The vector after reversing disguising (ciphertext * P⁻¹), of length n.
        G: The generator matrix of shape (k, n).
        GF: The finite field.
        t: The error-correcting capacity.

    Returns:
        best_message: The message vector in GF^(k) that minimizes the Hamming distance.
    """
    k, n = G.shape
    best_message = None
    best_distance = np.inf

    # Iterate over all possible message vectors in GF^(k).
    # For small parameters, this brute-force approach is feasible.
    for indices in np.ndindex(*(GF.order,) * k):
        m_candidate = GF(indices)
        candidate_codeword = m_candidate @ G
        # Compute Hamming distance between candidate_codeword and c_prime
        distance = sum(1 for i in range(n) if candidate_codeword[i] != c_prime[i])
        if distance < best_distance:
            best_distance = distance
            best_message = m_candidate
        if distance == 0:
            break

    if best_distance > t:
        raise ValueError("Decoding failed: error weight exceeds correction capacity.")
    return best_message


def decrypt(ciphertext, private_key, GF, t=None):
    """
    Decrypt the ciphertext using the private key.

    Args:
        ciphertext: The ciphertext vector of length n.
        private_key: Dictionary containing components of the private key, including S, P, G, and g_poly.
        GF: The finite field.
        t: The error-correcting capacity (default: degree of g_poly).

    Returns:
        recovered_message: The decrypted message vector.
    """
    S = private_key["S"]
    P = private_key["P"]
    G = private_key["G"]

    # For a permutation matrix, the inverse is its transpose
    P_inv = P.T
    S_inv = S.inverse()

    # Reverse the disguising transformation
    c_prime = ciphertext @ P_inv

    if t is None:
        t = private_key["g_poly"].degree

    # Use brute-force decoding to recover the candidate message m' such that m' * G is close to c_prime
    m_candidate = brute_force_decode(c_prime, G, GF, t)

    # Recover the original message by applying S⁻¹
    recovered_message = m_candidate @ S_inv
    return recovered_message


if __name__ == "__main__":
    # For demonstration, generate a keypair with small parameters
    public_key, private_key = generate_keypair(m=2, t=1, n=4)
    GF = private_key["support"].field  # Extract the finite field from the support set

    # Determine message length k (should be n - t)
    k = public_key.shape[0]

    # Create a random message vector in GF^(k)
    message = GF.Random(k)
    print("Original Message:", message)

    # Encrypt the message with error weight 1
    ciphertext, error_vector = encrypt(message, public_key, GF, error_weight=1)
    print("Ciphertext:", ciphertext)
    print("Error Vector:", error_vector)

    # Decrypt the ciphertext
    recovered_message = decrypt(ciphertext, private_key, GF)
    print("Recovered Message:", recovered_message)
