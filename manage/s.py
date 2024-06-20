from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Body
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import mysql.connector
import logging
import time
import hashlib
import os
import requests
import sys

app = FastAPI()
base_dir = Path("submission")

app.mount("/static", StaticFiles(directory="../user/fe"), name="fe")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_config = {
    "user": "root",
    "password": "12345",
    "host": "localhost",
    "database": "files"
}

def get_db_conn():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to the database: {err}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")

#def hfc(content):
#    return hashlib.sha256(content).hexdigest()

@app.post("/submission/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not base_dir.exists():
        base_dir.mkdir()

    ext = file.filename.split('.')[-1]
    subdir = base_dir / ext
    if not subdir.exists():
        subdir.mkdir()

    client_ip = request.client.host

    file_path = subdir / (client_ip + ".py")
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        timestamp = int(time.time())

        cursor.execute(
            "INSERT INTO submission (username, password, created_at, updated_at, status) VALUES (%s, %s, %s, %s, %s)",
            (client_ip, db_config['password'], timestamp, timestamp, "SUBMITTED")
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
        with open("../user/fe/index.html", "r", encoding="utf-8") as f:
            content = f.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uvicorn s:app <ip> <port>")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    uvicorn.run(app, host=ip, port=port)
