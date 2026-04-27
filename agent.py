import os
from openai import OpenAI

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

BASE_URL = "https://petstore.swagger.io/v2"


def generate_test_code(endpoint):
    prompt = f"""
You are a senior QA automation engineer.

Generate Pytest API test cases using the requests library.

API Details:
- Base URL: {BASE_URL}
- Path: {endpoint['path']}
- Method: {endpoint['method']}
- Description: {endpoint['summary']}
- Expected Status Codes: {endpoint['responses']}

Instructions:
- Replace any path parameters (e.g., {{id}}) with sample values like 1
- Use BASE_URL properly in the request
- Generate:
  1. One positive test
  2. One negative test
- For positive tests:
  - If data dependency exists, create test data first (e.g., POST before GET)
- Validate:
  - Status codes
  - Basic response body
- Use clean pytest format
- Ensure the code is directly executable
- Do NOT use placeholders like "example.com"

Output only valid Python code.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def review_and_improve(code):
    review_prompt = f"""
You are a senior QA reviewer.

Improve the following pytest API test code:

- Fix any syntax errors
- Ensure it runs without modification
- Improve assertions
- Ensure BASE_URL is correctly used
- Remove any invalid assumptions
- Make the test robust

Return only improved Python code.

Code:
{code}
"""

    improved = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": review_prompt}]
    )

    return improved.choices[0].message.content