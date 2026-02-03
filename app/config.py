from pydantic import BaseModel
import os

class Settings(BaseModel):
    MEDIA_DIR: str = os.getenv("MEDIA_DIR", "/data/media")
    JOB_DIR: str = os.getenv("JOB_DIR", "/data/jobs")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    DEVICE: str = os.getenv("DEVICE", "cuda")  # "cuda" or "cpu"
    MAX_IMAGE_MB: int = int(os.getenv("MAX_IMAGE_MB", "15"))

settings = Settings()
