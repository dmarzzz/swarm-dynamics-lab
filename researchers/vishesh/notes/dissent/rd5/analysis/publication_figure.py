"""Pad a saved scientific figure to publication width without altering its data pixels."""
import argparse
from PIL import Image
p = argparse.ArgumentParser()
p.add_argument('source')
p.add_argument('output')
a = p.parse_args()
im = Image.open(a.source).convert('RGB')
canvas = Image.new('RGB', (max(1600, im.width), im.height), '#101720')
canvas.paste(im, ((canvas.width-im.width)//2, 0))
canvas.save(a.output)
