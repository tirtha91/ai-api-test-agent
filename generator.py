import os

def save_test_file(name, code):
    os.makedirs("tests", exist_ok=True)
    file_path = f"tests/test_{name}.py"

    with open(file_path, "w") as f:
        f.write(code)

    print(f"Saved: {file_path}")