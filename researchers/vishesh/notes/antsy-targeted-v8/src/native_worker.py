"""Pixel-only worker; raw OCR output is private. Inspect never constructs an engine."""

import argparse, hashlib, importlib.metadata, importlib.util, json, os, platform, random, sys
from pathlib import Path
from fields import extract
from adapter import easyocr_words

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def inspect(engine, models):
    packages = {
        d.metadata["Name"].lower().replace("_", "-"): d.version
        for d in importlib.metadata.distributions()
        if d.metadata["Name"]
    }
    if engine == "P":
        import cv2
        from rapidocr import RapidOCR

        pkg = Path(importlib.util.find_spec("rapidocr").origin).parent
        hashes = {p.name: sha(p) for p in sorted((pkg / "models").glob("*.onnx"))}
        expected = json.loads(
            (ROOT.parent / "antsy-diversity-v7/spec/model-hashes.json").read_text()
        )
        if hashes != expected:
            raise ValueError("rapid_model_drift")
        for line in (
            (ROOT.parent / "antsy-diversity-v7/requirements.txt")
            .read_text()
            .splitlines()
        ):
            name, version = line.split("==")
            if importlib.metadata.version(name) != version:
                raise ValueError("rapid_version_drift")
    else:
        import easyocr, torch, torchvision

        if packages.get("opencv-python"):
            raise ValueError("overlapping_opencv_distributions")
        for line in (ROOT / "requirements-checker.txt").read_text().splitlines():
            name, version = line.split("==")
            if importlib.metadata.version(name) != version:
                raise ValueError("checker_version_drift")
        expected = {
            "craft_mlt_25k.pth": "2f8227d2def4037cdb3b34389dcf9ec1",
            "latin_g2.pth": "469869130aad1a34e8f9086f4262bc59",
        }
        hashes = {}
        for name, md5 in expected.items():
            data = (models / name).read_bytes()
            if hashlib.md5(data).hexdigest() != md5:
                raise ValueError("official_model_checksum_mismatch")
            hashes[name] = hashlib.sha256(data).hexdigest()
    return {
        "engine": engine,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
        "models": hashes,
    }


def run(engine, image, models):
    random.seed(0)
    import numpy as np

    np.random.seed(0)
    if engine == "C":
        import torch, cv2, easyocr

        torch.manual_seed(0)
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        cv2.setNumThreads(1)
        reader = easyocr.Reader(
            ["en", "id"],
            gpu=False,
            model_storage_directory=str(models),
            user_network_directory=str(models / "user"),
            detect_network="craft",
            recog_network="latin_g2",
            download_enabled=False,
            verbose=False,
            quantize=False,
            detector=False,
        )
        # EasyOCR 1.7.2 stores Reader.quantize as a one-element tuple. Set the
        # actual detector option explicitly before constructing that component.
        reader.quantize = False
        reader.setDetector("craft")
        words = easyocr_words(
            reader.readtext(
                str(image),
                decoder="greedy",
                batch_size=1,
                workers=0,
                detail=1,
                paragraph=False,
            )
        )
    else:
        sys.path.append(str(ROOT.parent / "antsy-diversity-v7/src"))
        spec = importlib.util.spec_from_file_location(
            "old_worker", ROOT.parent / "antsy-diversity-v7/src/worker.py"
        )
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        words = old.run(image, "rapidocr", 6)["raw_words"]
    return {"candidate": extract(words), "raw_words": words}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["P", "C"], required=True)
    p.add_argument("--models", type=Path, required=True)
    p.add_argument("--image", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--inspect", action="store_true")
    a = p.parse_args()
    if a.inspect:
        print(json.dumps(inspect(a.engine, a.models), sort_keys=True))
    else:
        if a.image is None or a.out is None or a.out.exists():
            raise ValueError("unique_pixel_output_required")
        a.out.write_text(json.dumps(run(a.engine, a.image, a.models)))
