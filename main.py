from parser import load_spec, extract_endpoints
from agent import generate_test_code, review_and_improve
from generator import save_test_file

def main():
    spec = load_spec("api_spec.json")
    endpoints = extract_endpoints(spec)

    for ep in endpoints[:3]:
        print(f"🚀 Generating test for {ep['path']}...")

        code = generate_test_code(ep)
        improved_code = review_and_improve(code)

        save_test_file(ep["name"], improved_code)

if __name__ == "__main__":
    main()