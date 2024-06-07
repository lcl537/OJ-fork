# server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn

app = FastAPI()
base_dir = Path("upload")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not base_dir.exists():
        base_dir.mkdir()

    ext = file.filename.split('.')[-1]
    subdir = base_dir / ext
    if not subdir.exists():
        subdir.mkdir()

    file_path = subdir / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload a Code File</h1>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

