import requests

def upload_files(url, path):
    with open(path, "rb") as f:
        response = requests.post(url, files={"file": f})
        if response.status_code == 200:
            print('success')
            print(response)
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
            print(f"文件 {f} 的ID是: {file_id}")
        except requests.exceptions.RequestException as e:
            print(f"上传文件 {f} 时出错: {e}")

if __name__ == "__main__":
    s = requests.session()
    s.keep_alive = False
    main()
