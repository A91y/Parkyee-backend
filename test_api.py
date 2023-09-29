# import requests
# # from get_csrftoken import get_csrftoken
# # Define the API endpoint URL
# api_url = 'http://127.0.0.1:8000/parking/'

# # Set up authentication headers (token-based authentication)
# headers = {
#     'Authorization': 'Token 0e470c78413a2b49ac608c09dcdf5f93e6b6bd64',  # Replace with your authentication token
#     'Content-Type': 'application/json',
#     # 'X-CSRFToken': get_csrftoken(),
# }

# # GET request example
# # response = requests.get(api_url)
# response = requests.get(api_url, headers=headers)

# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print(f"Error: {response.status_code}")

# # POST request example
# data_to_post = {
#     'available': 10,
#     'parking': r'http://127.0.0.1:8000/parking/1/',
# }

# # response = requests.post(api_url, json=data_to_post)
# response = requests.post(api_url, json=data_to_post, headers=headers)

# if response.status_code == 201:  # Assuming 201 means successful creation
#     data = response.json()
#     print(data + "\n" + response.text)
# else:
#     print(f"Error: {response.status_code}")

import requests

# Set the base URL of your Django API
base_url = 'http://127.0.0.1:8000/parkingavailability/1/'  # Replace with your API URL
# base_url = 'http://127.0.0.1:8000/parking/1/'  # Replace with your API URL

# Define the token
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1ODUyNTkwLCJpYXQiOjE2OTU4NDg5OTAsImp0aSI6IjVhOTgxMzc5MDdkNTQwN2JiZDUwNDJjNTQxOTI3M2NjIiwidXNlcl9pZCI6M30.cp_wrKqNi8bMIbIUz-48AfWrvN7HqaYQDXzN5WmsiiU'
headers = {
    'Authorization': f'Bearer {token}',
}
# headers = {
#     'Authorization': f'Bearer 1efd8ada517d856524b4c451f2fa367ac99b3919',
# }

# Test GET request
def test_get():
    response = requests.get(f'{base_url}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("GET Request Successful")
        print(data)
    else:
        print(f'Error: {response.status_code} - {response.text}')

# Test POST request
def test_post():
    data_to_post = {
        # 'field1': 'value1',
        # 'field2': 'value2',
        'available': 21,
        'parking': r'http://127.0.0.1:8000/parking/1/',
        
        # "url": "http://127.0.0.1:8000/parking/1/?format=api",
        # "name": "AyPark",
        # "address": "CV Raman",
        # "phone": "121212121",
        # "website": "https://example.com",
        # "image": "https://example.com/image.jpg",
        # "price": "12",
        # "description": "Something.......",
        # "latitude": "23.1",
        # "longitude": "24.2",
        # "max_capacity": 20,
        # "availability_count": 10,
        # "created_at": "2023-09-27T19:11:01.779534Z",
        # "last_updated_at": "2023-09-27T19:27:03.009700Z"
}
    

    response = requests.put(f'{base_url}', json=data_to_post, headers=headers)

    if response.status_code == 201:
        created_data = response.json()
        print("POST Request Successful")
        print(created_data)
    else:
        print(f'Error: {response.status_code}')

# Run the tests
if __name__ == "__main__":
    test_get()
    test_post()
