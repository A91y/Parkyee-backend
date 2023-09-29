import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/parkingavailability/'

# get csrf token from request
response = requests.get(api_url)
print(response.cookies)
csrftoken = response.cookies['csrftoken']
print(csrftoken)
