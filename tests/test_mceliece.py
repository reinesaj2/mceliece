# tests/test_mceliece.py

import unittest
import numpy as np
import sys
import os

# Adjust path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mceliece import key_generation, encrypt
# Import the simulation logic for testing the full cycle
from src.task1_example import decrypt_simulation


class TestMcEliece(unittest.TestCase):
    def test_key_generation_dimensions(self):
        """Test if key generation produces matrices of correct dimensions."""
        k, n, t = 3, 7, 1
        public_key, private_key = key_generation(k, n, t, seed=1)
        
        # Public key checks
        self.assertIn('G_prime', public_key)
        self.assertIn('t', public_key)
        self.assertEqual(public_key['G_prime'].shape, (k, n))
        self.assertEqual(public_key['t'], t)
        self.assertTrue(np.issubdtype(public_key['G_prime'].dtype, np.integer))

        # Private key checks
        self.assertIn('S', private_key)
        self.assertIn('G', private_key)
        self.assertIn('P', private_key)
        self.assertIn('S_inv', private_key)
        self.assertIn('P_inv', private_key)
        
        self.assertEqual(private_key['S'].shape, (k, k))
        self.assertEqual(private_key['G'].shape, (k, n))
        self.assertEqual(private_key['P'].shape, (n, n))
        self.assertEqual(private_key['S_inv'].shape, (k, k))
        self.assertEqual(private_key['P_inv'].shape, (n, n))
        
        # Check matrix properties (basic)
        self.assertTrue(np.issubdtype(private_key['S'].dtype, np.integer))
        self.assertTrue(np.issubdtype(private_key['G'].dtype, np.integer))
        self.assertTrue(np.issubdtype(private_key['P'].dtype, np.integer))
        # Check P is a permutation matrix (rows/cols sum to 1)
        self.assertTrue(np.all(private_key['P'].sum(axis=0) == 1))
        self.assertTrue(np.all(private_key['P'].sum(axis=1) == 1))
        # Check S is invertible (verify S * S_inv = I mod 2)
        identity_k = np.identity(k, dtype=int)
        self.assertTrue(np.array_equal((private_key['S'] @ private_key['S_inv']) % 2, identity_k))
        # Check P inverse is transpose
        self.assertTrue(np.array_equal(private_key['P_inv'], private_key['P'].T))

    def test_encrypt_output_shape(self):
        """Test if encryption produces ciphertext of correct shape."""
        k, n, t = 2, 5, 1
        public_key, _ = key_generation(k, n, t, seed=2)
        message = np.array([[1, 0]])
        ciphertext, error_vector = encrypt(message, public_key, seed=3)
        
        self.assertEqual(ciphertext.shape, (1, n))
        self.assertEqual(error_vector.shape, (1, n))
        self.assertTrue(np.issubdtype(ciphertext.dtype, np.integer))
        self.assertTrue(np.issubdtype(error_vector.dtype, np.integer))
        # Check error vector weight
        self.assertEqual(np.sum(error_vector), t)

    def test_encryption_decryption_cycle(self):
        """Test the full encrypt-decrypt cycle using the simulation."""
        k, n, t = 4, 8, 1
        seed = 100
        public_key, private_key = key_generation(k, n, t, seed=seed)
        
        # Test with a few messages
        messages = [
            np.array([[1, 0, 0, 0]]),
            np.array([[0, 1, 0, 1]]),
            np.array([[1, 1, 1, 1]]),
            np.array([[0, 0, 0, 0]])
        ]
        
        for i, message in enumerate(messages):
            with self.subTest(msg=f"Testing message: {message}", i=i):
                # Encrypt
                ciphertext, error_vector = encrypt(message, public_key, seed=seed + i + 1)
                
                # Decrypt using simulation
                recovered_message = decrypt_simulation(ciphertext, error_vector, private_key, message)
                
                # Verify
                self.assertTrue(np.array_equal(message, recovered_message),
                                f"Failed for message {message}. Got {recovered_message}")

    def test_invalid_message_encryption(self):
        """Test encryption fails for invalid message shapes or content."""
        k, n, t = 3, 5, 1
        public_key, _ = key_generation(k, n, t, seed=4)

        # Incorrect shape
        invalid_message_shape = np.array([[1, 0]]) # Should be 1x3
        with self.assertRaises(ValueError):
            encrypt(invalid_message_shape, public_key)

        # Incorrect content (not binary)
        invalid_message_content = np.array([[1, 0, 2]])
        with self.assertRaises(ValueError):
             encrypt(invalid_message_content, public_key)


if __name__ == "__main__":
    unittest.main()
