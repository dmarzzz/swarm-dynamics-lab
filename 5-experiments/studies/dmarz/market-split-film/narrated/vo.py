"""Speak the narration: one clip per script segment, with a local neural voice (Kokoro through mlx-audio).

Kokoro has fixed named speakers, so every clip has the same voice. Run it on Apple silicon with a Python that has
mlx-audio, misaki[en] and the spaCy model en_core_web_sm:

    VIRTUAL_ENV=<venv> <venv>/bin/python researchers/dmarz/notes/market-split-film/narrated/vo.py \
      --out data/market-split-film/narrated/vo [--only P5,P6]

Writes <key>.wav per segment and durations.json. A segment whose clip already exists is kept unless named in --only.
To use a recorded human voice instead, drop <key>.wav files of any length into the folder and rerun with no model:
the film's timeline is derived from the clip lengths.
"""
import argparse
import json
import wave
from pathlib import Path

HERE = Path(__file__).parent


def seconds(path):
    with wave.open(str(path)) as w: return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); ap.add_argument('--only', default='')
    ap.add_argument('--script', default=str(HERE / 'script.json'), help='another film can reuse this with its own script')
    args = ap.parse_args()
    script = json.loads(Path(args.script).read_text())
    voice, segs = script['voice'], [s for s in script['segments'] if s['say']]
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, args.only.split(',')))
    from mlx_audio.tts.generate import generate_audio
    from mlx_audio.tts.utils import load_model
    todo = [s for s in segs if s['key'] in only or not (out / f"{s['key']}.wav").exists()]
    model = load_model(voice['model']) if todo else None
    for s in todo:
        clip = out / f"{s['key']}.wav"
        for old in out.glob(f"{s['key']}_*.wav"): old.unlink()
        generate_audio(text=s['say'], model=model, voice=voice['speaker'], lang_code=voice['lang_code'], speed=voice['speed'],
                       output_path=str(out), file_prefix=s['key'], audio_format='wav', join_audio=True, verbose=False)
        made = sorted(out.glob(f"{s['key']}*.wav"), key=lambda p: p.stat().st_mtime)[-1]
        if made != clip: made.replace(clip)
        print(f"{s['key']}: {seconds(clip):.2f} s", flush=True)
    durations = {s['key']: round(seconds(out / f"{s['key']}.wav"), 3) for s in segs}
    (out / 'durations.json').write_text(json.dumps(durations, indent=1) + '\n')
    print(f'total speech {sum(durations.values()):.1f} s')


if __name__ == '__main__':
    main()
