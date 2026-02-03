import os
import uuid
from pathlib import Path
from .config import settings

def ensure_dirs():
    Path(settings.MEDIA_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.JOB_DIR).mkdir(parents=True, exist_ok=True)

def new_job_id() -> str:
    return str(uuid.uuid4())

def job_path(job_id: str) -> str:
    return os.path.join(settings.JOB_DIR, job_id)

def media_path(job_id: str) -> str:
    return os.path.join(settings.MEDIA_DIR, job_id)

def init_job_dirs(job_id: str):
    ensure_dirs()
    Path(job_path(job_id)).mkdir(parents=True, exist_ok=True)
    Path(media_path(job_id)).mkdir(parents=True, exist_ok=True)

def job_files(job_id: str):
    """
    Standardized filenames:
    - person.jpg
    - garment.jpg
    - result.png
    - status.json
    """
    jp = job_path(job_id)
    mp = media_path(job_id)
    return {
        "job_dir": jp,
        "media_dir": mp,
        "person": os.path.join(jp, "person.jpg"),
        "garment": os.path.join(jp, "garment.jpg"),
        "result": os.path.join(mp, "result.png"),
        "status": os.path.join(jp, "status.json"),
    }
