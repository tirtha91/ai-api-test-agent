import requests
import pytest
import os  # Added import for os module

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture
def create_pet():
    # Create a pet to be used for the positive test
    pet_data = {
        "id": 123,
        "name": "Fluffy",
        "photoUrls": [],
        "tags": [{"id": 1, "name": "happy"}],
        "status": "available"
    }

    # Create the pet in the API
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)
    assert response.status_code == 200, "Failed to create pet"
    yield pet_data  # Yielding pet data to the test case

    # Cleanup: Delete the pet after the test
    delete_response = requests.delete(f"{BASE_URL}/pet/{pet_data['id']}")
    assert delete_response.status_code == 200, "Failed to delete pet"

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
    
    response = requests.put(f"{BASE_URL}/pet", json=updated_pet_data)  # Corrected endpoint
    assert response.status_code == 404, f"Expected 404 for non-existing pet, got {response.status_code}: {response.text}"

def test_update_pet_invalid():
    invalid_pet_data = {
        "id": 123,  # Using the ID of the pet we create for the test
        "name": "",  # Invalid name
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }

    response = requests.put(f"{BASE_URL}/pet", json=invalid_pet_data)  # Corrected endpoint
    assert response.status_code == 400, f"Expected 400 for invalid pet data, got {response.status_code}: {response.text}"

def test_update_pet_method_not_allowed():
    response = requests.put(f"{BASE_URL}/pet", json={})  # Changed method to PUT
    assert response.status_code == 405, f"Expected 405 for wrong method, got {response.status_code}: {response.text}"

def test_find_pets_by_status_negative():
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "invalid_status"})  # Corrected URL with params
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

def test_upload_image_positive(create_pet):
    pet_id = create_pet['id']
    test_image_path = 'test_image.jpg'
    assert os.path.exists(test_image_path), f"Test image {test_image_path} does not exist."
    
    with open(test_image_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(f"{BASE_URL}/pet/{pet_id}/uploadImage", files=files)

    assert response.status_code == 200, "Upload Image failed"
    response_json = response.json()
    assert 'message' in response_json, "Response message not found"
    assert response_json['message'].startswith('Uploaded file details'), "Unexpected upload response message"

def test_upload_image_negative():
    pet_id = 99999  # A deliberately invalid pet ID
    test_image_path = 'test_image.jpg'
    assert os.path.exists(test_image_path), f"Test image {test_image_path} does not exist."
    
    with open(test_image_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(f"{BASE_URL}/pet/{pet_id}/uploadImage", files=files)

    assert response.status_code == 404, f"Expected status 404 for non-existing pet upload, got {response.status_code}"

def test_find_pets_by_tags_positive(create_pet):
    response = requests.get(f"{BASE_URL}/pet/findByTags", params={"tags": "happy"})
    
    assert response.status_code == 200, "Unexpected status code"
    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) > 0, "Expected at least one pet to be found"
    assert response_json[0]["name"] == create_pet["name"], "Pet name does not match"

def test_find_pets_by_tags_negative():
    response = requests.get(f"{BASE_URL}/pet/findByTags", params={"tags": "nonexistent"})
    
    assert response.status_code == 200, "Unexpected status code"
    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) == 0, "Expected an empty list for non-existent tags"