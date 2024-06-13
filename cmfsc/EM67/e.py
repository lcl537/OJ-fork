from fastapi import FastAPI, HTTPException
from pathlib import Path
import subprocess
import logging

app = FastAPI()
base_dir = Path("new")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/execute/{filename}")
async def execute_code(filename: str):
    file_path = base_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        result = subprocess.run(["python3", str(file_path)], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            status = "CORRECT"  # Assuming we have a way to verify correctness
        else:
            status = "INCORRECT"
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": status
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Execution timed out")
    except Exception as e:
        logger.error(f"Error executing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="118.89.82.251", port=21)
