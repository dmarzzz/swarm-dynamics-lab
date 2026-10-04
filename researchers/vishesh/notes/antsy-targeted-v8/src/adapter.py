"""Normalize documented EasyOCR detail=1 rows, without importing/loading a model."""

import math


def easyocr_words(observations):
    words = []
    for box, text, confidence in observations:
        if len(box) != 4 or any(len(point) != 2 for point in box):
            raise ValueError("quadrilateral required")
        xs = [float(p[0]) for p in box]
        ys = [float(p[1]) for p in box]
        confidence = float(confidence)
        if (
            not all(math.isfinite(v) for v in xs + ys + [confidence])
            or not 0 <= confidence <= 1
        ):
            raise ValueError("invalid coordinates or score")
        if not isinstance(text, str):
            raise ValueError("text required")
        x = min(xs)
        y = min(ys)
        w = max(xs) - x
        h = max(ys) - y
        if w <= 0 or h <= 0:
            raise ValueError("non-positive box")
        if text.strip():
            words.append(
                {
                    "text": text,
                    "x": x,
                    "y": y + h / 2,
                    "h": h,
                    "box": [x, y, w, h],
                    "confidence": confidence,
                }
            )
    return words
