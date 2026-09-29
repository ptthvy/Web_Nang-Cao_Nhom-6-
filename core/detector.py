from collections import Counter

from PIL import Image
from ultralytics import YOLO

from config import DETECT_CONFIDENCE, DETECT_IOU, DETECT_MAX_DETECTIONS, DEVICE, YOLO_WEIGHTS


class ObjectDetector:
    def __init__(self, weights: str = YOLO_WEIGHTS):
        self.model = YOLO(weights)
        self.device = 0 if DEVICE == "cuda" else "cpu"

    def detect(
        self,
        image: Image.Image,
        conf: float = DETECT_CONFIDENCE,
        iou: float = DETECT_IOU,
        max_det: int = DETECT_MAX_DETECTIONS,
    ):
        result = self.model.predict(
            image.convert("RGB"), conf=conf, iou=iou, max_det=max_det, device=self.device, verbose=False
        )[0]
        boxes = result.boxes
        detections = [
            {"label": result.names[int(c)], "score": round(float(s), 4), "box_xyxy": [round(v, 1) for v in b]}
            for b, s, c in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist())
        ]
        annotated = Image.fromarray(result.plot()[..., ::-1])  # plot() trả BGR → đổi sang RGB
        summary = dict(Counter(d["label"] for d in detections))
        return {"detections": detections, "summary": summary}, annotated