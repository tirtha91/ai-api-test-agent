from parser import load_spec, extract_endpoints
from agent import generate_test_code, review_and_improve, fix_failed_test
from generator import save_test_file
import subprocess


def run_tests():
    result = subprocess.run(
        ["pytest", "tests/"],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr


def main():
    spec = load_spec("api_spec_PetStore.json")
    endpoints = extract_endpoints(spec)

    for ep in endpoints[:2]:  # keep small for testing
        print(f"🚀 Generating test for {ep['path']}...")

        # Step 1: Generate initial test
        code = generate_test_code(ep)

        # Step 2: Improve initial test
        improved_code = review_and_improve(code)

        # Step 3: Save test file
        save_test_file(ep["name"], improved_code)

        # Step 4: Execution + Retry Loop
        max_retries = 2
        attempt = 0

        while attempt <= max_retries:
            print(f"\n▶️ Running tests (Attempt {attempt + 1})...")
            output, error = run_tests()

            print(output)

            if "FAILED" not in output and "ERROR" not in output: 
                print("✅ Tests passed!")
                break

            if attempt == max_retries:
                print("❌ Max retry limit reached. Tests still failing.")
                break

            print("❌ Test failed. Sending to AI for fix...")

            # Step 5: Fix using AI
            fixed_code = fix_failed_test(improved_code, output)

            # Step 6: Overwrite test file
            save_test_file(ep["name"], fixed_code)

            # Update code for next iteration
            improved_code = fixed_code

            attempt += 1


if __name__ == "__main__":
    main()