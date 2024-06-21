from fastapi import FastAPI, HTTPException
import subprocess
import requests
import uvicorn
from pathlib import Path

app = FastAPI()

CODE_DIR = Path("./msfiles")
ANSWER_FILE = Path("./answer.txt")
MANAGE_SERVER_URL = "http://0.0.0.0:8000/submission"

@app.post("/execute/")
async def execute_code():
    code_file = CODE_DIR / "new_code.py"

    if not code_file.exists():
        raise HTTPException(status_code=404, detail="No code file found")

    result = subprocess.run(["python3", str(code_file)], capture_output=True, text=True)

    output = result.stdout
    error = result.stderr

    status = "ERROR" if error else "CORRECT" if output.strip() == ANSWER_FILE.read_text().strip() else "INCORRECT"

    response = requests.patch(MANAGE_SERVER_URL, json={"status": status})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to report status to manage server")

    return {"status": status, "output": output, "error": error}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uvicorn e:app <ip> <port>")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    uvicorn.run(app, host=ip, port=port)
