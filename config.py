"""Cấu hình tập trung. Mọi giá trị đều ghi đè được bằng biến môi trường."""
import os
from pathlib import Path

import torch

ROOT = Path(os.environ.get("APP_ROOT", Path(__file__).resolve().parent))
DATA_DIR = ROOT / "data"
ART_DIR = ROOT / "artifacts"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

YOLO_WEIGHTS = os.environ.get("YOLO_WEIGHTS", str(ART_DIR / "detector" / "yolo11n.pt"))
DETECT_CONFIDENCE = float(os.environ.get("DETECT_CONFIDENCE", "0.25"))
DETECT_IOU = float(os.environ.get("DETECT_IOU", "0.45"))
DETECT_MAX_DETECTIONS = int(os.environ.get("DETECT_MAX_DETECTIONS", "100"))
CLIP_MODEL = os.environ.get("CLIP_MODEL", "openai/clip-vit-base-patch32")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
LLM_MODEL = os.environ.get(
    "LLM_MODEL",
    "Qwen/Qwen2.5-1.5B-Instruct" if DEVICE == "cuda" else "Qwen/Qwen2.5-0.5B-Instruct",
)

ENABLED_MODELS = {
    model.strip()
    for model in os.environ.get("ENABLED_MODELS", "classifier,detector,retrieval,llm").split(",")
    if model.strip()
}
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "8"))
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:8501").split(",")


def resolve_path(path: str) -> Path:
    """Chuyển đường dẫn tương đối thành đường dẫn theo thư mục ứng dụng."""
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate
