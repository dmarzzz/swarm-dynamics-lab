"""Measured cumulative trajectory, not a simulated swarm animation."""

from PIL import Image, ImageDraw
from qualification import summarize, MODES


def render(out, records, journal):
    frames = []
    for n in range(len(records) + 1):
        s = summarize(records[:n], journal)
        im = Image.new("RGB", (1600, 900), "#101b29")
        d = ImageDraw.Draw(im)
        d.text(
            (50, 40),
            f"Antsy v8 | observed qualification trajectory | {n}/20 receipts",
            fill="white",
            font_size=32,
        )
        d.text(
            (50, 100),
            "Correct (green), wrong (red), referred (gray); unscorable separately. No independence claim.",
            fill="white",
            font_size=24,
        )
        for k, mode in enumerate(MODES):
            a = s["arms"][mode]
            y = 200 + k * 110
            d.text((50, y), mode, fill="white", font_size=25)
            x = 400
            for key, color in [
                ("correct", "#45cba1"),
                ("wrong", "#fa6767"),
                ("refer", "#8090a0"),
            ]:
                width = a[key] * 48
                if width:
                    d.rectangle((x, y, x + width, y + 45), fill=color)
                x += width
            d.text(
                (400, y + 50),
                f"correct {a['correct']} | wrong {a['wrong']} | refer {a['refer']}",
                fill="white",
                font_size=20,
            )
        d.text(
            (50, 810),
            f"Scorable: {s['scorable']}/{n}; future/uncompleted: {20 - n}. Costs are cold-worker measurements.",
            fill="white",
            font_size=24,
        )
        frames.append(im)
    frames[-1].save(out / "final_frame.png")
    frames[0].save(
        out / "observed-replay.gif",
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0,
    )
