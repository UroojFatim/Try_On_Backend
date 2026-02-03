import json
import time
from typing import Literal, Optional
from .storage import job_files
from .viton_infer import run_stableviton_tryon

Status = Literal["queued", "running", "done", "error"]

def write_status(job_id: str, status: Status, message: str = "", result_url: Optional[str] = None):
    files = job_files(job_id)
    payload = {
        "job_id": job_id,
        "status": status,
        "message": message,
        "result_url": result_url,
        "updated_at": int(time.time()),
    }
    with open(files["status"], "w", encoding="utf-8") as f:
        json.dump(payload, f)

def read_status(job_id: str):
    files = job_files(job_id)
    try:
        with open(files["status"], "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def process_job(job_id: str, base_url: str):
    files = job_files(job_id)
    write_status(job_id, "running", "Starting try-on...")

    try:
        # === Core inference call ===
        run_stableviton_tryon(
            person_path=files["person"],
            garment_path=files["garment"],
            out_path=files["result"],
        )

        result_url = f"{base_url}/media/{job_id}/result.png"
        write_status(job_id, "done", "Success", result_url=result_url)

    except Exception as e:
        write_status(job_id, "error", f"Failed: {type(e).__name__}: {str(e)}")
        raise
