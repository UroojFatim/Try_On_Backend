FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git curl \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

WORKDIR /app

# Install API deps
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# (Optional) Install torch + vision inside container (choose versions matching your GPU/CUDA)
# NOTE: You might prefer installing these inside StableVITON repo itself.
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Copy app
COPY app /app/app

# ---- StableVITON repo placement ----
# Put StableVITON code at /opt/stableviton
# You can either:
# 1) COPY it into the image, or
# 2) git clone during build (private repos need tokens)
#
# Example clone (public):
# RUN git clone <STABLEVITON_REPO_URL> /opt/stableviton
#
# For now, we expect you to mount it or bake it in.

# Data dirs
RUN mkdir -p /data/jobs /data/media
ENV MEDIA_DIR=/data/media JOB_DIR=/data/jobs DEVICE=cuda BASE_URL=http://localhost:8000

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
