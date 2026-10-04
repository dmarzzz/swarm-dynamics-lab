"""One pixel-only OCR worker. No dataset annotations or evaluator input."""

import argparse, csv, io, json, os, subprocess
from pathlib import Path
from core import extract, spatial_lines


def run(image, engine, psm):
    words = []
    if engine == "tesseract":
        r = subprocess.run(
            [
                "tesseract",
                str(image),
                "stdout",
                "-l",
                "ind+eng",
                "--psm",
                str(psm),
                "tsv",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=40,
            env=dict(os.environ, OMP_THREAD_LIMIT="1"),
        )
        for w in csv.DictReader(
            io.StringIO(r.stdout), delimiter="\t", quoting=csv.QUOTE_NONE
        ):
            if w.get("text", "").strip() and float(w["conf"]) >= 0:
                x, y, width, h = (int(w[k]) for k in ["left", "top", "width", "height"])
                words.append(
                    {
                        "text": w["text"],
                        "confidence": float(w["conf"]) / 100,
                        "x": x,
                        "y": y + h / 2,
                        "h": h,
                        "box": [x, y, width, h],
                    }
                )
    else:
        import cv2

        cv2.setNumThreads(1)
        from rapidocr import RapidOCR

        ocr = RapidOCR(
            params={
                "Global.log_level": "error",
                "EngineConfig.onnxruntime.intra_op_num_threads": 1,
                "EngineConfig.onnxruntime.inter_op_num_threads": 1,
            }
        )
        r = ocr(str(image))
        if r.txts is not None:
            for box, txt, confidence in zip(r.boxes, r.txts, r.scores):
                xs = [float(p[0]) for p in box]
                ys = [float(p[1]) for p in box]
                x = min(xs)
                y = min(ys)
                w = max(xs) - x
                h = max(ys) - y
                words.append(
                    {
                        "text": txt,
                        "confidence": float(confidence),
                        "x": x,
                        "y": y + h / 2,
                        "h": h,
                        "box": [round(x), round(y), round(w), round(h)],
                    }
                )
    lines = spatial_lines(words)
    return {"candidate": extract(lines), "raw_words": words}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--image", type=Path, required=True)
    p.add_argument("--engine", choices=["tesseract", "rapidocr"], required=True)
    p.add_argument("--psm", type=int, default=6)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    a.out.write_text(json.dumps(run(a.image, a.engine, a.psm)))
