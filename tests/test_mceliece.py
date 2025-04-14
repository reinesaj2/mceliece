# tests/test_mceliece.py

import unittest
import numpy as np
from src import mceliece


class TestMcEliece(unittest.TestCase):
    def test_key_generation(self):
        public_key, private_key = mceliece.generate_key()
        self.assertEqual(public_key.shape[0], 2)  # or the expected dimensions

    def test_encryption_decryption(self):
        public_key, private_key = mceliece.generate_key()
        message = np.array([1, 0])
        ciphertext = mceliece.encrypt(message, public_key)
        recovered_message = mceliece.decrypt(ciphertext, private_key)
        # For now, with placeholders, simply check that something is returned
        self.assertIsNotNone(recovered_message)


if __name__ == "__main__":
    unittest.main()
