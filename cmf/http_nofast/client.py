import os
import requests

# 服务器的 URL
url = 'http://127.0.0.1:8000/upload'
filename = "/home/ec2-user/OJ/cmf_network/test.rb"

def send_file(filename):
    filesize = os.path.getsize(filename)

    with open(filename, 'rb') as file:
        response = requests.post(url, files={"file": (os.path.basename(filename), file)})
        if response.status_code == 200:
            print("File sent successfully")
        else:
            print(f"Failed to send file. Status code: {response.status_code}")

if __name__ == "__main__":
    send_file(filename)
    print(f"Send Ruby code file")
