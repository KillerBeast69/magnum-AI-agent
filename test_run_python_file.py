from functions.run_python_file import run_python_file

print("--- Test 1: Main Usage Instructions ---")
print(run_python_file("calculator", "main.py"))
print("\n")

print("--- Test 2: Run Calculation ---")
# Note: args must be a list
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("\n")

print("--- Test 3: Run Tests ---")
print(run_python_file("calculator", "tests.py"))
print("\n")

print("--- Test 4: Security Violation ---")
print(run_python_file("calculator", "../main.py"))
print("\n")

print("--- Test 5: Non-existent File ---")
print(run_python_file("calculator", "nonexistent.py"))
print("\n")

print("--- Test 6: Not a Python File ---")
print(run_python_file("calculator", "lorem.txt"))
print("\n")