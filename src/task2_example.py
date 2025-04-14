# src/task2_example.py

import numpy as np
import sys
import os

# Adjust path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Reuse the decryption simulation logic from task1 or redefine if needed
# For simplicity, we copy it here. In a larger project, this might be in a shared utils module.
from src.mceliece import key_generation, encrypt
from src.task1_example import decrypt_simulation # Reuse the simulation logic

def main():
    print("=== McEliece Example Task 2 ===")

    # Parameters (different from Task 1)
    k = 3  # message length
    n = 5  # codeword length
    t = 1  # error correction capability (can be > 1 if decoder supported)
    seed = 123 # Different seed for reproducibility

    print(f"Parameters: k={k}, n={n}, t={t}, seed={seed}\n")

    # 1. Key Generation
    print("--- Key Generation ---")
    public_key, private_key = key_generation(k, n, t, seed=seed)
    print(f"Private G:\n{private_key['G']}")
    print(f"Private S:\n{private_key['S']}")
    print(f"Private P:\n{private_key['P']}")
    print(f"Public G' = S*G*P:\n{public_key['G_prime']}")
    print(f"Error capability t: {public_key['t']}\n")

    # 2. Encryption
    print("--- Encryption ---")
    message = np.array([[1, 0, 1]]) # Example message (1xk), different from Task 1
    print(f"Original Message m: {message}")

    ciphertext, error_vector = encrypt(message, public_key, seed=seed+1) # Use diff seed for error
    print(f"Error Vector e (weight {t}): {error_vector}")
    # Calculate intermediate c' = m * G'
    c_prime = (message @ public_key['G_prime']) % 2
    print(f"Intermediate c' = m*G': {c_prime}")
    print(f"Final Ciphertext y = c' + e: {ciphertext}\n")

    # 3. Decryption (Simulation)
    # We reuse the decrypt_simulation function defined in task1_example
    # It simulates decoding using the known error vector
    recovered_message = decrypt_simulation(ciphertext, error_vector, private_key, message)

    # Final Check
    print("\n--- Verification ---")
    print(f"Original Message:    {message}")
    print(f"Recovered Message:   {recovered_message}")

    if np.array_equal(message, recovered_message):
        print("SUCCESS: Decryption correctly recovered the original message!")
    else:
        print("FAILURE: Decryption did not recover the original message.")

if __name__ == "__main__":
    main()
