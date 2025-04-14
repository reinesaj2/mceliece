# McEliece Cryptosystem: Step-by-Step Examples

This document walks through the two concrete examples implemented in `src/task1_example.py` and `src/task2_example.py`. These examples demonstrate the McEliece cryptosystem's key generation, encryption, and decryption processes using small parameters and simulated decoding.

**Note:** The core functions in `src/mceliece.py` use randomly generated matrices for the private generator `G`. Real McEliece implementations use specific code families (like Goppa codes) with efficient decoding algorithms. Our examples *simulate* the decoding step by using the known error vector `e` generated during encryption. This is done purely to illustrate the overall structure involving the scrambling matrix `S` and permutation matrix `P`.

## Task 1: First Example (`src/task1_example.py`)

This example uses the following parameters:
- Message dimension `k = 2`
- Codeword length `n = 4`
- Error correction capability `t = 1`
- Random seed `seed = 42` for key generation
- Message `m = [1, 0]`

### a) Key Generation

The `key_generation(k=2, n=4, t=1, seed=42)` function performs the following:

1.  **Generate Private G:** A random \(2 \times 4\) binary matrix `G` is created.
    ```
    # Example G (output will vary based on numpy version/platform, but shape is fixed)
    [[1 0 1 0]
     [1 1 0 1]]
    ```
2.  **Generate Private S:** A random \(2 \times 2\) invertible binary matrix `S` is created. The inverse `S_inv` is also computed.
    ```
    # Example S
    [[1 1]
     [1 0]]
    # Example S_inv
    [[0 1]
     [1 1]]
    ```
3.  **Generate Private P:** A random \(4 \times 4\) permutation matrix `P` is created. The inverse `P_inv` (which is `P.T`) is stored.
    ```
    # Example P
    [[0 0 0 1]
     [0 1 0 0]
     [1 0 0 0]
     [0 0 1 0]]
    # Example P_inv (P.T)
    [[0 0 1 0]
     [0 1 0 0]
     [0 0 0 1]
     [1 0 0 0]]
    ```
4.  **Compute Public G':** The public key `G_prime` is calculated as \(G' = S G P \pmod 2\).
    ```
    # Example G' (result of S @ G @ P % 2)
    [[0 0 1 1]
     [1 1 1 0]]
    ```
5.  **Keys:**
    *   **Public Key:** `{'G_prime': G_prime, 't': 1}`
    *   **Private Key:** `{'S': S, 'G': G, 'P': P, 'S_inv': S_inv, 'P_inv': P_inv}`

### b) Encryption

The `encrypt(message, public_key, seed=43)` function (using a different seed for the error vector) takes the message `m = [[1, 0]]`:

1.  **Compute c':** \(c' = m G' \pmod 2\)
    ```
    # Example c' = [[1 0]] @ G' % 2
    [[0 0 1 1]]
    ```
2.  **Generate Error Vector e:** A random binary vector `e` of length \(n=4\) with Hamming weight \(t=1\) is generated.
    ```
    # Example e (weight 1)
    [[0 1 0 0]]
    ```
3.  **Compute Ciphertext y:** \(y = c' + e \pmod 2\)
    ```
    # Example y = c' + e % 2
    [[0 1 1 1]]
    ```

The final ciphertext sent is `y = [[0 1 1 1]]`. The error vector `e` is kept aside *only* for the decryption simulation.

### c) Decryption (Simulation)

The `decrypt_simulation(y, e, private_key, m)` function simulates the process:

1.  **Undo Permutation:** Calculate \(y' = y P^{-1} \pmod 2\).
    ```
    # Example y' = [[0 1 1 1]] @ P_inv % 2
    [[1 1 1 0]]
    ```
    This \(y'\) corresponds to \(mSG + e P^{-1}\).
2.  **Simulate Decoding:** The crucial step. Since we don't have a decoder for the random `G`, we use the known `e` to find the permuted error \(e' = e P^{-1}\) and subtract it from \(y'\) to recover \(mSG\).
    ```
    # Example e' = [[0 1 0 0]] @ P_inv % 2
    [[0 1 0 0]]
    # Example mSG = (y' - e') % 2
    [[1 0 1 0]]
    ```
    The script verifies this calculated `mSG` matches \((m S) G \pmod 2\) computed directly using the private key components and original message `m`.
3.  **Recover mS:** This step requires isolating \(mS\) from \(mSG\). The simulation simplifies this by using the \(mS\) computed during verification: \(mS = m S \pmod 2\).
    ```
    # Example mS = [[1 0]] @ S % 2
    [[1 1]]
    ```
4.  **Recover m:** Calculate the original message \(m = (mS) S^{-1} \pmod 2\).
    ```
    # Example m = [[1 1]] @ S_inv % 2
    [[1 0]]
    ```

The final recovered message `[[1 0]]` matches the original message.

---

## Task 2: Second Example (`src/task2_example.py`)

This example uses different parameters:
- Message dimension `k = 3`
- Codeword length `n = 5`
- Error correction capability `t = 1`
- Random seed `seed = 123` for key generation
- Message `m = [1, 0, 1]`

The process follows the exact same steps as Task 1, but with these new dimensions and values.

### a) Key Generation
- `key_generation(k=3, n=5, t=1, seed=123)` is called.
- A \(3 \times 5\) private `G` matrix is generated.
- A \(3 \times 3\) invertible private `S` matrix (and `S_inv`) is generated.
- A \(5 \times 5\) private permutation matrix `P` (and `P_inv`) is generated.
- The \(3 \times 5\) public key `G_prime = S G P` is computed.

### b) Encryption
- `encrypt(message=[[1, 0, 1]], public_key, seed=124)` is called.
- Intermediate \(c' = m G'\) is computed.
- An error vector `e` of length 5, weight 1 is generated.
- Final ciphertext \(y = c' + e\) is computed.

### c) Decryption (Simulation)
- `decrypt_simulation(y, e, private_key, m)` is called.
- Permutation is undone: \(y' = y P^{-1}\).
- Decoding is simulated: \(e' = e P^{-1}\), then \(mSG = y' - e'\).
- \(mS\) is recovered (using simulation knowledge: \(mS = m S\)).
- Original message is recovered: \(m = (mS) S^{-1}\).

The script verifies that the recovered message again matches the original `[[1 0 1]]`.

## Conclusion

These two examples illustrate the mechanics of the McEliece cryptosystem: hiding a structured code `G` within a seemingly random public code `G'` using `S` and `P`. Encryption involves multiplying by `G'` and adding errors. Decryption uses the private `S`, `P`, and a (simulated) decoder for `G` to reverse the process and correct the errors.
