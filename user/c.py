import requests

def upload_files(url, path):
    with open(path, "rb") as f:
        response = requests.post(url, files={"file": f})
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

def main():
    url = "http://0.0.0.0:8000/upload/"
    path = ["./tc/test.rb", "./tc/sc.c"]
    
    for f in path:
        try:
            response = upload_files(url, f)
            file_id = response.json().get("id")
            print(f"File {f} ID: {file_id}")
        except requests.exceptions.RequestException as e:
            print(f"Upload file {f} error: {e}")

if __name__ == "__main__":
    main()
