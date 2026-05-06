import requests
import pytest

BASE_URL = "https://petstore.swagger.io/v2/pet"

@pytest.fixture
def create_pet():
    # Create a pet to update
    pet_data = {
        "id": 1,
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "name": "Buddy",
        "photoUrls": ["url1", "url2"],
        "tags": [{"id": 1, "name": "tag1"}],
        "status": "available"
    }
    response = requests.post(BASE_URL, json=pet_data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"
    yield pet_data
    # Cleanup: delete the pet after the test
    cleanup_response = requests.delete(f"{BASE_URL}/{pet_data['id']}")
    assert cleanup_response.status_code == 200, f"Failed to delete pet: {cleanup_response.text}"

def test_update_pet_success(create_pet):
    updated_pet_data = {
        "id": create_pet['id'],
        "category": create_pet['category'],
        "name": "Buddy Update",
        "photoUrls": create_pet['photoUrls'],
        "tags": create_pet['tags'],
        "status": "sold"
    }

    response = requests.put(BASE_URL, json=updated_pet_data)
    assert response.status_code == 200, f"Failed to update pet: {response.text}"
    response_data = response.json()
    assert response_data['name'] == updated_pet_data['name'], f"Expected name to be '{updated_pet_data['name']}', got '{response_data['name']}'"
    assert response_data['status'] == updated_pet_data['status'], f"Expected status to be '{updated_pet_data['status']}', got '{response_data['status']}'"

def test_update_pet_not_found():
    updated_pet_data = {
        "id": 9999,  # Non-existing pet ID
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "name": "Buddy Update",
        "photoUrls": ["url1", "url2"],
        "tags": [{"id": 1, "name": "tag1"}],
        "status": "sold"
    }

    response = requests.put(f"{BASE_URL}", json=updated_pet_data)  # Use the correct endpoint here
    assert response.status_code == 404, f"Expected 404 for non-existing pet, got {response.status_code}: {response.text}"

def test_update_pet_invalid():
    invalid_pet_data = {
        "id": 1,
        "name": "",  # Invalid name
        "status": "available"
    }

    response = requests.put(f"{BASE_URL}", json=invalid_pet_data)  # Use the correct endpoint here
    assert response.status_code == 400, f"Expected 400 for invalid pet data, got {response.status_code}: {response.text}"

def test_update_pet_method_not_allowed():
    response = requests.put(BASE_URL, json={})  # Use PUT instead of POST
    assert response.status_code == 405, f"Expected 405 for wrong method, got {response.status_code}: {response.text}"