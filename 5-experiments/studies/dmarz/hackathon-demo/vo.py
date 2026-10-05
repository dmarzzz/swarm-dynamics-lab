"""Speak narration.json: one wav per scene with Kokoro (mlx-audio), plus durations.json.

    VIRTUAL_ENV=_out/venv-vo _out/venv-vo/bin/python vo.py [--speed 1.0] [--only sybil,next] [--budget 114]

Environment: uv venv _out/venv-vo && uv pip install --python _out/venv-vo/bin/python mlx-audio "misaki[en]" + en_core_web_sm.
With --budget, speeds 1.0, 1.08, 1.15 are tried in turn until the summed speech is under the budget.
"""
import argparse
import json
import wave
from pathlib import Path

HERE = Path(__file__).parent
MODEL = 'mlx-community/Kokoro-82M-bf16'
SPEEDS = [1.0, 1.08, 1.15]


def seconds(path):
    with wave.open(str(path)) as w: return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / '_out' / 'vo')); ap.add_argument('--only', default='')
    ap.add_argument('--speed', type=float, default=None); ap.add_argument('--budget', type=float, default=114.0)
    args = ap.parse_args()
    script = json.loads((HERE / 'narration.json').read_text())
    voice, segs = script['voice'], script['segments']
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, args.only.split(',')))
    # espeak-ng keeps its data path in a 160-char buffer and exits the process when the path is longer, which this
    # venv's site-packages path is. phonemizer resolves symlinks, so copy the data to a shorter real path in the venv.
    import shutil, sys
    import espeakng_loader
    import misaki.espeak  # sets the long path on import; override it below
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    data = espeakng_loader.get_data_path()
    if len(data) > 140:
        short = Path(sys.prefix) / 'esd'
        if not short.exists(): shutil.copytree(data, short)
        EspeakWrapper.set_data_path(str(short))
    from mlx_audio.tts.generate import generate_audio
    from mlx_audio.tts.utils import load_model
    model = load_model(MODEL)
    for speed in ([args.speed] if args.speed else SPEEDS):
        for s in segs:
            key = s['scene']
            if only and key not in only: continue
            clip = out / f'{key}.wav'
            for old in out.glob(f'{key}_*.wav'): old.unlink()
            generate_audio(text=s['text'], model=model, voice=voice, lang_code='a', speed=speed, output_path=str(out),
                           file_prefix=key, audio_format='wav', join_audio=True, verbose=False)
            made = sorted(out.glob(f'{key}*.wav'), key=lambda p: p.stat().st_mtime)[-1]
            if made != clip: made.replace(clip)
            print(f'{key}: {seconds(clip):.2f} s', flush=True)
        durations = {s['scene']: round(seconds(out / f"{s['scene']}.wav"), 3) for s in segs}
        total = sum(durations.values())
        durations.update({'_engine': 'kokoro (mlx-audio, ' + MODEL + ')', '_voice': voice, '_speed': speed, '_total': round(total, 3)})
        (out / 'durations.json').write_text(json.dumps(durations, indent=1) + '\n')
        print(f'speed {speed}: total speech {total:.1f} s (budget {args.budget})', flush=True)
        if total < args.budget: break


if __name__ == '__main__':
    main()
