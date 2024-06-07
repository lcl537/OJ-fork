from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

UPLOAD_DIRECTORY = "./uploads"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    with open(file_location, "r") as f:
        print("\nCode content\n")
        print(f.read())

    return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

