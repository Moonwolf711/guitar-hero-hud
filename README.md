# Guitar Hero HUD

A simple 2D Pygame implementation of a Guitar Hero-style Heads-Up Display (HUD) that processes WAV audio files for note timing simulation.

## Features
- 4 colored lanes (A/S/D/F)
- Falling notes with hit detection and scoring
- Combo multiplier
- Placeholder WAV beat detection / simulation
- Optional audio playback if example.wav is present

## Requirements
- Python 3.7+
- Pygame: `pip install pygame`

## Running
```bash
python guitar_hero_hud.py
```

Place an `example.wav` file in the same directory for audio and better beat timing (currently falls back to simulated pattern).

## Controls
- A / S / D / F: hit notes in the corresponding lane
- Close window to quit

## Notes
This is a demo/educational project. Beat detection is simulated; for real onset detection consider libraries like librosa.
