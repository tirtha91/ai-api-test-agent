import requests
import pytest

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture
def create_pet():
    # Create pet data for testing
    pet_data = {
        "id": 1,
        "name": "Fido",
        "photoUrls": [],
        "status": "available"
    }
    # Attempt to create the pet
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)
    # Ensure the pet was created successfully
    assert response.status_code == 200, "Failed to create pet"
    yield pet_data  # Yield pet data for test

    # Clean up - delete the pet after test
    requests.delete(f"{BASE_URL}/pet/{pet_data['id']}")

def test_get_pet_by_id_positive(create_pet):
    # Given a pet ID that exists
    pet_id = create_pet['id']  # Use ID from the fixture

    # When I request the pet by ID
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    # Then the response status code should be 200
    assert response.status_code == 200, "Expected status code 200"
    
    # And the response body should contain expected fields
    data = response.json()
    assert data['id'] == pet_id, f"Expected pet ID {pet_id}, got {data['id']}"
    assert data['name'] == create_pet['name'], f"Expected pet name {create_pet['name']}, got {data['name']}"
    assert 'status' in data, "Response should contain 'status' field"

def test_get_pet_by_id_negative():
    # Given a pet ID that does not exist
    pet_id = 999999  # This ID should not exist

    # When I request the pet by ID
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    # Then the response status code should be 404
    assert response.status_code == 404, "Expected status code 404"
    
    # Optionally, we can also check the response body for error message
    assert response.json().get('message') == "Pet not found", "Expected error message not found"