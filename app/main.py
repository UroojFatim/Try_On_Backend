from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask
import os
import shutil

from .config import settings
from .storage import init_job_dirs, job_files, new_job_id
from .worker import write_status, read_status, process_job

app = FastAPI(title="Try-On API (StableVITON)")

# CORS: allow your Next.js domain(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set to ["http://localhost:3000", "https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated media
os.makedirs(settings.MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

def _check_file_size(upload: UploadFile):
    # UploadFile doesn't provide size directly reliably; we enforce in save step by limiting content length if needed.
    # Keeping minimal here; you can enforce via proxy/nginx too.
    return

def _save_upload_to(path: str, upload: UploadFile):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

@app.post("/tryon")
async def create_tryon_job(
    person: UploadFile = File(...),
    garment: UploadFile = File(...),
):
    if person.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="person must be an image (jpg/png/webp)")
    if garment.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="garment must be an image (jpg/png/webp)")

    job_id = new_job_id()
    init_job_dirs(job_id)
    files = job_files(job_id)

    write_status(job_id, "queued", "Job created")

    # Save images
    _save_upload_to(files["person"], person)
    _save_upload_to(files["garment"], garment)

    # Kick off background processing (simple single-instance approach)
    task = BackgroundTask(process_job, job_id, settings.BASE_URL)
    return {
        "job_id": job_id,
        "status_url": f"/tryon/{job_id}",
        "message": "queued",
    }, task

@app.get("/tryon/{job_id}")
def get_job_status(job_id: str):
    st = read_status(job_id)
    if not st:
        raise HTTPException(status_code=404, detail="job_id not found")
    return st

@app.get("/health")
def health():
    return {"ok": True, "device": settings.DEVICE}
