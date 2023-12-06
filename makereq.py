import requests
import json

url= "http://184.148.224.37:41303/process"

data = {
    'speaker': 'michael', # avaialable speakers michael, matilda, bella
    'text': 'An Interior Department spokesperson told The Hill the department has no new personnel announcements to make.'
}

json_data = json.dumps(data)

headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json_data, headers=headers)
# Check the response
if response.status_code == 200:
    # processed_data = response.json()  # Get the processed data from the response
    # print("Processed Message:", processed_data.get('processed_message'))
    with open('processed_audio2.mp3', 'wb') as f:
        f.write(response.content)
else:
    print("Error:", response.json())

# import os

# def get_file_paths(directory_path):
#     try:
#         file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
#         return file_paths
#     except OSError as e:
#         print(f"Error: {e}")
#         return []

# # Example usage:
# directory_path = '/coquio_ttsx_vish_coqui/api/code/voices/matilda'  # Replace this with the actual directory path
# folders = get_file_paths(directory_path)
# print(folders)