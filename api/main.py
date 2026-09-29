"""API cho chức năng phân loại ảnh."""
import io
import time

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from core.classifier import ImageClassifier

app = FastAPI(title="AI Web Apps")
classifier: ImageClassifier | None = None


async def read_image(file: UploadFile) -> Image.Image:
    try:
        return Image.open(io.BytesIO(await file.read())).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="Tệp tải lên không phải là ảnh hợp lệ.") from exc


def get_classifier() -> ImageClassifier:
    global classifier
    if classifier is None:
        classifier = ImageClassifier()
    return classifier


@app.post("/api/classify")
async def classify(file: UploadFile = File(...), top_k: int = Form(3)):
    """Trả về ba nhãn hoa có độ tin cậy cao nhất."""
    started_at = time.perf_counter()
    result = get_classifier().predict(await read_image(file), top_k=max(1, min(top_k, 5)))
    return {**result, "latency_ms": round((time.perf_counter() - started_at) * 1000, 1)}
