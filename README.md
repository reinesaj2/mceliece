# McEliece Cryptosystem Project

Welcome to the McEliece Cryptosystem project, an exploration of a post-quantum public-key cryptosystem based on error-correcting codes. This project demonstrates the McEliece scheme through small, concrete examples and is designed to provide both theoretical background and practical hands-on experience.

## Project Objectives

- **Understand the McEliece scheme:** Learn how the public-key cryptosystem works and why it remains secure even against quantum attacks.
- **Explore Error-Correcting Codes:** Study the principles behind Goppa codes and their use in secure encryption.
- **Contrast with Classical Cryptosystems:** Compare McEliece with RSA, ElGamal, and ECC.
- **Hands-on Examples:** Follow through two complete examples that cover key generation, encryption, and decryption.

## Directory Structure

```
McEliece_Project/
├── README.md                 
├── LICENSE                   
├── requirements.txt          
├── Makefile                  
├── docs/
│   ├── project_overview.md   
│   └── examples_explanation.md   
├── src/
│   ├── __init__.py           
│   ├── mceliece.py           
│   ├── task1_example.py      
│   └── task2_example.py      
├── notebooks/
│   └── McEliece_Tutorial.ipynb   
├── tests/
│   └── test_mceliece.py      
└── data/
    └── sample_messages.txt   
```

## Getting Started

1. **Installation:**  
   Install the necessary dependencies listed in `requirements.txt`. If you're using SageMath, ensure it's properly configured.
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Running Examples:**  
   - **Task 1 Example:**  
     Run the first example:
     ```bash
     python src/task1_example.py
     ```
   - **Task 2 Example:**  
     Run the second example:
     ```bash
     python src/task2_example.py
     ```

3. **Interactive Exploration:**  
   Open the `notebooks/McEliece_Tutorial.ipynb` in your Jupyter/SageMath environment to interactively explore the McEliece cryptosystem.

4. **Testing:**  
   Execute the unit tests with:
   ```bash
   python -m unittest discover tests
   ```

## Additional Resources

- **Documentation:**  
  Detailed theory and step-by-step explanations are available in the `docs` folder.
- **License:**  
  Review the `LICENSE` file for information about the project’s terms.
