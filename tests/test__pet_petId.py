import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture
def create_pet():
    # Create a pet for the positive test
    pet_data = {
        "id": 1,
        "name": "Fido",
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)
    # Ensure the pet was created successfully
    assert response.status_code == 200, "Failed to create pet"
    yield pet_data['id']
    
    # Clean up after test if needed (e.g., delete the pet)
    cleanup_response = requests.delete(f"{BASE_URL}/pet/{pet_data['id']}")
    assert cleanup_response.status_code == 200, "Failed to delete pet"

def test_get_pet_positive(create_pet):
    # Use the created pet ID for the positive test
    pet_id = create_pet
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    
    # Validate status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Validate basic response body
    response_data = response.json()
    assert response_data.get('id') == pet_id, "Pet ID does not match"
    assert response_data.get('name') == "Fido", "Pet name does not match"
    assert response_data.get('status') == "available", "Pet status does not match"

def test_get_pet_negative():
    # Use a non-existing pet ID for the negative test
    pet_id = 99999
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    
    # Validate status code
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"

    # Validate that the response body is as expected for a not found pet
    response_data = response.json()
    assert 'message' in response_data, "Expected message key not found in response"
    assert response_data.get('message') == "Pet not found", "Unexpected message in response"