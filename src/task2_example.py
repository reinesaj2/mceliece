# src/task2_example.py

from mceliece import generate_key, encrypt, decrypt
import numpy as np


def task2_example():
    print("=== Task 2: McEliece Example 2 ===")
    public_key, private_key = generate_key()

    # Example binary message
    message = np.array([0, 1])
    print("Original Message:", message)

    ciphertext = encrypt(message, public_key)
    print("Ciphertext:", ciphertext)

    recovered_message = decrypt(ciphertext, private_key)
    print("Recovered Message:", recovered_message)


if __name__ == "__main__":
    task2_example()
