"""API cho chức năng phân loại ảnh."""
import io
import time

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from core.classifier import ImageClassifier
from core.detector import ObjectDetector

app = FastAPI(title="AI Web Apps")
classifier: ImageClassifier | None = None
detector: ObjectDetector | None = None


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


def get_detector() -> ObjectDetector:
    global detector
    if detector is None:
        detector = ObjectDetector()
    return detector


@app.post("/api/classify")
async def classify(file: UploadFile = File(...), top_k: int = Form(3)):
    """Trả về ba nhãn hoa có độ tin cậy cao nhất."""
    started_at = time.perf_counter()
    result = get_classifier().predict(await read_image(file), top_k=max(1, min(top_k, 5)))
    return {**result, "latency_ms": round((time.perf_counter() - started_at) * 1000, 1)}


@app.post("/api/detect")
async def detect(file: UploadFile = File(...), conf: float = Form(0.25)):
    model = get_detector()
    t0 = time.perf_counter()
    result, annotated = model.detect(await read_image(file), conf=min(max(conf, 0.05), 0.95))
    return {**result, "image": _to_base64(annotated), "latency_ms": round((time.perf_counter() - t0) * 1000, 1)}