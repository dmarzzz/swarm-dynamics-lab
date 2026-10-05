"""Fit the film to its narration, then lay the narration on the recorded picture.

    python3 narrate.py time [--film long]         # scene seconds in index.html <- clip lengths in _out/vo/durations.json
    node record.mjs _out/picture.mp4              # silent picture at those timings
    python3 narrate.py mix _out/picture.mp4 _out/swarm-of-theseus-demo.mp4

Each scene lasts as long as its clip plus a little air, never less than the floor its picture needs.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
FILM = sys.argv[sys.argv.index('--film') + 1] if '--film' in sys.argv else 'short'
VO = HERE / '_out' / ('vo' if FILM == 'short' else 'vo-' + FILM)
NARRATION = HERE / ('narration.json' if FILM == 'short' else f'narration-{FILM}.json')
LEAD, TAIL = 0.25, 0.20                       # silence before the voice starts in a scene, and after it ends
HOLD = {'sybil': 0.3, 'twoclose': 3.0}                         # extra seconds after the voice, where the last beat needs time on screen
FLOOR = {'theseus50': 18, 'highlights': 5, 'why': 10, 'frame': 16, 'tracks': 9, 'stack': 12, 'roadmap1': 8, 'roadmap2': 8, 'roadmap3': 8, 'more': 7.0, 'team': 3.5, 'define': 5, 'questions': 7, 'method': 5, 'lab': 9, 'sybil': 18, 'result3': 18, 'theseus': 18, 'next': 12}


def plan():
    d = json.loads((VO / 'durations.json').read_text())
    order = [s['scene'] for s in json.loads(NARRATION.read_text())['segments']]
    out, t = [], 0.0
    for scene in order:
        dur = round(max(FLOOR.get(scene, 4), d[scene] + LEAD + TAIL + HOLD.get(scene, 0)) * 30) / 30      # whole frames
        out.append({'scene': scene, 'start': round(t, 4), 'dur': round(dur, 4), 'clip': d[scene]})
        t += dur
    return out, t


def time():
    scenes, total = plan()
    page = HERE / 'index.html'
    s = page.read_text()
    a = s.index(f'    {FILM}: ['); b = s.index('    ],\n', a)
    lines = ''.join(f"      ['{x['scene']}', {x['dur']:.4f}],\n" for x in scenes)
    page.write_text(s[:a] + f'    {FILM}: [\n' + lines + s[b:])
    for x in scenes: print(f"{x['scene']:10s} start {x['start']:7.2f}  scene {x['dur']:6.2f}  voice {x['clip']:6.2f}")
    print(f'total {total:.2f} s')


def mix(picture, out):
    scenes, total = plan()
    inputs, graph = [], []
    for i, x in enumerate(scenes):
        inputs += ['-i', str(VO / f"{x['scene']}.wav")]
        graph.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={round((x['start'] + LEAD) * 1000)}:all=1[a{i}]")
    graph.append(''.join(f'[a{i}]' for i in range(len(scenes))) + f'amix=inputs={len(scenes)}:normalize=0,apad=whole_dur={total:.3f}[m]')
    raw = Path(out).with_suffix('.narration.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', ';'.join(graph), '-map', '[m]', '-t', f'{total:.3f}', str(raw)], check=True)
    probe = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                           check=True, capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex('{'):probe.rindex('}') + 1])
    norm = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', picture, '-i', str(raw), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', norm,
                    '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-t', f'{total:.3f}', '-movflags', '+faststart', out], check=True)
    raw.unlink()
    print(f'wrote {out}: {total:.1f} s, narration {m["input_i"]} LUFS before levelling')


if __name__ == '__main__':
    if sys.argv[1] == 'time': time()
    elif sys.argv[1] == 'mix': mix(sys.argv[2], sys.argv[3])
    else: raise SystemExit(__doc__)
