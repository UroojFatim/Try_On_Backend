import os
from .config import settings

def run_stableviton_tryon(person_path: str, garment_path: str, out_path: str):
    """
    Implement your StableVITON inference here.

    This skeleton supports two patterns:

    A) Direct Python import if you vendor StableVITON code into the container.
    B) CLI call (subprocess) if the repo provides an inference script.

    Output must be written to `out_path` (PNG recommended).
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # -------------------------
    # OPTION B (recommended skeleton): call external inference script
    # -------------------------
    # Example (YOU MUST ADAPT paths/args to StableVITON repo):
    #
    #   python /opt/stableviton/infer.py \
    #     --person /data/jobs/<job>/person.jpg \
    #     --garment /data/jobs/<job>/garment.jpg \
    #     --output /data/media/<job>/result.png \
    #     --device cuda
    #
    import subprocess

    cmd = [
        "python",
        "/opt/stableviton/infer.py",  # <-- you will create/adapt this
        "--person", person_path,
        "--garment", garment_path,
        "--output", out_path,
        "--device", settings.DEVICE,
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "StableVITON inference failed.\n"
            f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
        )

    if not os.path.exists(out_path):
        raise FileNotFoundError(f"Inference finished but output not found: {out_path}")
