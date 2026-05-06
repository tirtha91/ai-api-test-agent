import os
import re

def clean_code(code):
    # Remove ```python or ```
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)

    # Trim whitespace
    return code.strip()


def save_test_file(name, code):
    os.makedirs("tests", exist_ok=True)

    safe_name = name.replace("{", "").replace("}", "")
    file_path = f"tests/test_{safe_name}.py"

    # 🔥 Clean code before saving
    cleaned_code = clean_code(code)

    with open(file_path, "w") as f:
        f.write(cleaned_code)

    print(f"💾 Saved: {file_path}")