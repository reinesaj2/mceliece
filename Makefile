# Makefile for McEliece Project

# Default Python interpreter
PYTHON = python3

# Default target: show help
help: 
	@echo "McEliece Project Makefile" 
	@echo "-------------------------" 
	@echo "Available targets:" 
	@echo "  install       Install dependencies from requirements.txt" 
	@echo "  example1      Run Task 1 example (src/task1_example.py)" 
	@echo "  example2      Run Task 2 example (src/task2_example.py)" 
	@echo "  test          Run unit tests (tests/test_mceliece.py)" 
	@echo "  notebook      Start Jupyter Notebook server in notebooks/ directory (requires jupyter)" 
	@echo "  clean         Remove Python cache files" 
	@echo "" 

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

# Run Task 1 Example
example1:
	@echo "Running Task 1 Example..."
	$(PYTHON) src/task1_example.py

# Run Task 2 Example
example2:
	@echo "Running Task 2 Example..."
	$(PYTHON) src/task2_example.py

# Run Tests
test:
	@echo "Running Unit Tests..."
	$(PYTHON) -m unittest discover tests

# Run Jupyter Notebook (optional, requires jupyter installed)
notebook:
	@echo "Starting Jupyter Notebook in ./notebooks/ ..."
	@echo "Ensure you have jupyter installed ('pip install notebook')"
	cd notebooks && jupyter notebook

# Clean Python cache files
clean:
	@echo "Cleaning Python cache files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Phony targets (targets that don't represent files)
.PHONY: help install example1 example2 test notebook clean
