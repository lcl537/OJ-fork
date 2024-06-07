import requests

def upload_files(url, path):
    with open(path, "rb") as f:
        response = requests.post(url, files={"file": f})
        return response

def main():
    url = "http://127.0.0.1:8000/upload/"
    path = ["./tc/test.rb", "./tc/sc.c"]
    
    for f in path:
        response = upload_files(url, f)
        print(response.json())

if __name__ == "__main__":
    main()
