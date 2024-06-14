from fastapi import FastAPI, HTTPException， UploadFile, File
from pathlib import Path
import subprocess
import logging
import uvicorn

app = FastAPI()
base_dir = Path("new")
answer_file = Path("/root/OJ/cmfsc/answer.txt")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/receive_code/")
async def receive_code(file: UploadFile = File(...)):
    file_path = base_dir / file.filename
    
    try:
        if not base_dit.exists():
            base_dir.mkdir()
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        logger.error(f"Error saving received file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving received file: {e}")

    return {"status": "received"}

@app.get("/execute/{filename}")
async def execute_code(filename: str):
    file_path = base_dir / filename
    stdout_path = base_dir / f"{filename}.stdout"
    stderr_path = base_dir / f"{filename}.stderr"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        result = subprocess.run(["python3", str(file_path)], capture_output=True, text=True, timeout=10)
        with open(stdout_path, "w") as f:
            f.write(result.stdout)
        with open(stderr_path, "w") as f:
            f.write(result.stderr)
        
        status = "PROCESSING"
        if result.stderr:
            status = "ERROR"
        else:
            diff_result = subprocess.run(
                ["diff", str(stdout_path), str(answer_file)],
                capture_output=True,
                text=True
            )
            if diff_result.returncode == 0:
                status = "CORRECT"
            else:
                status = "INCORRECT"
        updated_status(filename, status)
        '''return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": status
        }'''
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Execution timed out")
    except Exception as e:
        logger.error(f"Error executing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing file: {e}")

def update_status(filename, status):
    manage_server_ip = "管理服务器的IP地址"
    file_id = filename.split(".")[0]
    url = f"http://{manage_server_ip}/update_status/{file_id}"
    payload = {
        "status": status
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to update status: {response.content}")
    else:
        logger.info(f"Status updated to {status} for file id {file_id}")

if __name__ == "__main__":
    uvicorn.run(app, host="118.89.82.251", port=21)
