import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture(scope="module")
def create_pet():
    # Create a pet for the positive test case
    pet_data = {
        "id": 1,
        "name": "Fluffy",
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "photoUrls": ["http://example.com/photo1.jpg"],
        "tags": [{"id": 1, "name": "cute"}],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"  # Ensure the pet is created successfully
    return pet_data["id"]

def test_get_pet_positive(create_pet):
    pet_id = create_pet
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    assert response.status_code == 200, f"Failed to retrieve pet: {response.text}"
    pet = response.json()
    assert pet['id'] == pet_id, "Pet ID does not match"
    assert pet['name'] == "Fluffy", "Pet name does not match"
    assert pet['status'] == "available", "Pet status is not available"

def test_get_pet_negative():
    invalid_pet_id = 99999  # Assuming this ID does not exist
    response = requests.get(f"{BASE_URL}/pet/{invalid_pet_id}")

    assert response.status_code == 404, f"Expected 404 for non-existent pet ID but got {response.status_code}: {response.text}"