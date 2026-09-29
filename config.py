"""Cấu hình dùng chung cho các module AI."""
import os
from pathlib import Path

import torch

ROOT = Path(os.environ.get("APP_ROOT", Path(__file__).resolve().parent))
ART_DIR = ROOT / "artifacts"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
YOLO_WEIGHTS = os.environ.get("YOLO_WEIGHTS", str(ART_DIR / "detector" / "best.pt"))
DETECT_CONFIDENCE = float(os.environ.get("DETECT_CONFIDENCE", "0.25"))
DETECT_IOU = float(os.environ.get("DETECT_IOU", "0.45"))
DETECT_MAX_DETECTIONS = int(os.environ.get("DETECT_MAX_DETECTIONS", "100"))
