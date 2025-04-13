import requests

url = "http://127.0.0.1:8000/api/simplify_pdf"
file_path = "/Users/saidev/Desktop/ex1.pdf"

with open(file_path, "rb") as f:
    resp = requests.post(url, files={"file": f})

print("Status code:", resp.status_code)
print("Response JSON:", resp.json())