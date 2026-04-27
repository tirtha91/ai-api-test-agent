import json

def load_spec(path):
    with open(path) as f:
        return json.load(f)

def extract_endpoints(spec):
    endpoints = []
    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            endpoints.append({
                "name": path.replace("/", "_").replace("{", "").replace("}", ""),
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "responses": list(details.get("responses", {}).keys())
            })
    return endpoints