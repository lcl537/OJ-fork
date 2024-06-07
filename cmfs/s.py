from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import mysql.connector
import logging
import time
import datetime

app = FastAPI()
base_dir = Path("upload")

app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_config = {
    "user": "root",
    "password": "H2b2g58431*",
    "host": "localhost",
    "database": "file_upload"
}

def get_db_conn():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to the database: {err}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not base_dir.exists():
        base_dir.mkdir()

    ext = file.filename.split('.')[-1]
    subdir = base_dir / ext
    if not subdir.exists():
        subdir.mkdir()

    file_path = subdir / (file.filename.rsplit(".", 1)[0] + ".py")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

        #timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        timestamp = int(time.time())
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO files (filename, user, pw, created_at, updated_at, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (file.filename, db_config['user'], db_config['password'], timestamp, timestamp, "SUBMITTED")
        )
        conn.commit()
        file_id = cursor.lastrowid
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        logger.error(f"Error inserting file metadata into database: {e}")
        raise HTTPException(status_code=500, detail=f"Error inserting file metadata into database: {e}")

    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        print("\n" + "="*40 + "\n")
        print(f"文件名: {file.filename}")
        print("-" * 40 + "\n")
        print(file_content)
        print("="*40 + "\n")

    return {"id": file_id, "status": "SUBMITTED"}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("./static/index.html", "r", encoding="utf-8") as f:
            content = f.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
