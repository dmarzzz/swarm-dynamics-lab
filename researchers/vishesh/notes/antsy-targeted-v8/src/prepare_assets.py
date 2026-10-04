"""Download official checker model files without loading a model or receipt."""

import argparse, hashlib, io, json, urllib.request, zipfile
from pathlib import Path

MODELS = {
    "craft_mlt_25k.pth": (
        "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip",
        "2f8227d2def4037cdb3b34389dcf9ec1",
    ),
    "latin_g2.pth": (
        "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/latin_g2.zip",
        "469869130aad1a34e8f9086f4262bc59",
    ),
}


def main(dest):
    dest.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (url, md5) in MODELS.items():
        p = dest / name
        if p.exists():
            data = p.read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=120) as response:
                archive = response.read(200 * 1024 * 1024)
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                data = z.read(name)
        if hashlib.md5(data).hexdigest() != md5:
            raise ValueError("official_checksum_mismatch")
        if not p.exists():
            p.write_bytes(data)
        manifest[name] = {
            "official_url": url,
            "md5": md5,
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--models", type=Path, required=True)
    a = p.parse_args()
    main(a.models)
