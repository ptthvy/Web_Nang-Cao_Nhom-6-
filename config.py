"""Cấu hình dùng chung cho chức năng phân loại ảnh."""
import os
from pathlib import Path

import torch

ROOT = Path(os.environ.get("APP_ROOT", Path(__file__).resolve().parent))
ART_DIR = ROOT / "artifacts"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
