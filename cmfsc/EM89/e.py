from fastapi import FastAPI, HTTPException
from pathlib import Path
import subprocess
import logging
import requests
import json
import os

app = FastAPI()
base_dir = Path("new")
answer_file = Path("answer.txt")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/execute/{id}")
async def execute_code(id: str):
    file_path = base_dir / f"{id}.py"
    stdout_path = base_dir / f"{id}.stdout"
    stderr_path = base_dir / f"{id}.stderr"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        result = subprocess.run(
            ["python3", str(file_path)], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        with open(stdout_path, "w") as f:
            f.write(result.stdout)
        with open(stderr_path, "w") as f:
            f.write(result.stderr)
        
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

        update_status(id, status)
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Execution timed out")
    except Exception as e:
        logger.error(f"Error executing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing file: {e}")

def update_status(id, status):
    manage_server_ip = "管理服务器的IP地址"
    url = f"http://{manage_server_ip}/update_status/{id}"
    payload = {
        "status": status
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.patch(url, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to update status: {response.content}")
    else:
        logger.info(f"Status updated to {status} for file id {id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

