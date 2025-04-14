# src/task1_example.py

from mceliece import generate_key, encrypt, decrypt
import numpy as np


def task1_example():
    print("=== Task 1: McEliece Example 1 ===")
    public_key, private_key = generate_key()

    # Example binary message (ensure its dimension aligns with key dimensions)
    message = np.array([1, 0])
    print("Original Message:", message)

    ciphertext = encrypt(message, public_key)
    print("Ciphertext:", ciphertext)

    recovered_message = decrypt(ciphertext, private_key)
    print("Recovered Message:", recovered_message)


if __name__ == "__main__":
    task1_example()
