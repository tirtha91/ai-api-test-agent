import pytest
import requests
import os

BASE_URL = "https://petstore.swagger.io/v2"

def create_pet():
    pet_data = {
        "id": 1,
        "name": "Fluffy",
        "photoUrls": [],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)
    return response.status_code, pet_data["id"]

def delete_pet(pet_id):
    response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response.status_code == 200, f"Failed to delete pet with id {pet_id}"

def test_upload_image_positive():
    # Create a pet first
    status_code, pet_id = create_pet()
    assert status_code == 200, "Failed to create pet"

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

    # Clean up: Delete the pet after the test
    delete_pet(pet_id)

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