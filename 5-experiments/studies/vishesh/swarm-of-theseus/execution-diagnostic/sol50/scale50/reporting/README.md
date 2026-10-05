# Saved-data visualization only

These scripts render the public aggregate S50-AUDIT.json and S50-EVENTS.json. They make no model calls and read no credentials, owner prompts or private experimental responses. They are outside the frozen experimental executable closure.

Run with Python 3, matplotlib and Pillow:

```
python reporting/render_plot.py
python reporting/render_animation.py
python reporting/render_replay.py
```

The PNG reports all assigned terminal cases; the 700-event replay and sampled GIF show only observed events. One world and one shared ancestor remain explicit. The position circles do not encode measured communication edges. No intermediate behavioral score is interpolated. Font fallback may change pixel layout across operating systems while retaining measured data.
