import requests
import pytest
import os  # Import os for file existence checks

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture(scope="module")
def create_pet():
    # Create a pet to use for the positive test
    data = {
        "id": 1,
        "name": "Doggie",
        "photoUrls": [],  # Ensure photoUrls is present as an empty list
        "tags": [],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"  # Ensure the pet is created successfully
    yield data["id"]  # Return the pet ID for use in tests
    # Cleanup code can go here if needed (not implemented here)

def test_find_pets_by_status_positive(create_pet):
    response = requests.get(f"{BASE_URL}/pet/findByStatus?status=available")
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    pets = response.json()
    assert isinstance(pets, list), "Response is not a list"
    assert len(pets) > 0, "No pets found with the expected status"

def test_find_pets_by_status_negative():
    response = requests.get(f"{BASE_URL}/pet/findByStatus?status=invalid_status")
    
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert "error" in response.json(), "Error message is not present in the response"

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
    
    response = requests.put(f"{BASE_URL}/pet", json=updated_pet_data)  # Endpoint for updating a pet
    assert response.status_code == 404, f"Expected 404 for non-existing pet, got {response.status_code}: {response.text}"

def test_update_pet_invalid():
    invalid_pet_data = {
        "id": 1,
        "name": "",  # Invalid name
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    
    response = requests.put(f"{BASE_URL}/pet", json=invalid_pet_data)  # Endpoint for updating a pet
    assert response.status_code == 400, f"Expected 400 for invalid pet data, got {response.status_code}: {response.text}"

def test_update_pet_method_not_allowed():
    response = requests.put(BASE_URL, json={})  # Corrected to use PUT
    assert response.status_code == 405, f"Expected 405 for wrong method, got {response.status_code}: {response.text}"

def test_upload_image_positive(create_pet):
    # Use the pet_id from fixture
    pet_id = create_pet
    
    # Ensure the test image exists
    test_image_path = 'test_image.jpg'
    assert os.path.exists(test_image_path), f"Test image {test_image_path} does not exist."
    
    # Upload an image
    with open(test_image_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(f"{BASE_URL}/pet/{pet_id}/uploadImage", files=files)
    
    assert response.status_code == 200, "Upload Image failed"
    response_json = response.json()
    assert 'message' in response_json, "Response message not found"
    assert response_json['message'].startswith('Uploaded file details'), "Unexpected upload response message"

def test_upload_image_negative():
    # Attempt to upload an image for a non-existing pet
    pet_id = 99999  # A deliberately invalid pet ID
    
    # Ensure the test image exists
    test_image_path = 'test_image.jpg'
    assert os.path.exists(test_image_path), f"Test image {test_image_path} does not exist."
    
    with open(test_image_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(f"{BASE_URL}/pet/{pet_id}/uploadImage", files=files)

    assert response.status_code == 404, f"Expected status 404 for non-existing pet upload, got {response.status_code}"