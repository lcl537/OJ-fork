import requests
import sys

def upload_files(url, path):
    with open(path, "rb") as f:
        response = requests.post(url, files={"file": f})
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

def main(ip, port):
    url = f"http://{ip}:{port}/submission/"
    path = ["./test_code/test.rb", "./test_code/sc.c"]
    
    for f in path:
        try:
            response = upload_files(url, f)
            file_id = response.json().get("id")
            print(f"File {f} ID: {file_id}")
        except requests.exceptions.RequestException as e:
            print(f"Upload file {f} error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 c.py <ip> <port>")
        sys.exit(1)

    ip = sys.argv[1]
    port = sys.argv[2]

    main(ip, port)
