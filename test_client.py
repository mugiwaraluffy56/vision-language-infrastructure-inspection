import requests
import sys

def test_inspect(image_path):
    url = "http://localhost:8000/inspect"
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('sample.jpg', f, 'image/jpeg')}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            print("Success!")
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <image_path>")
    else:
        test_inspect(sys.argv[1])
