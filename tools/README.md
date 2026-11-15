# tools

- `episodes/epNNN.py` — one file per video: whiteboard/handout entries `B` and lecture segments `S` (empty for videos without burned-in subtitles).
- `build.py` — regenerates `../index.html` from `template.html` and the episode files: `python3 tools/build.py`.
- `capture.js` — helper pasted into the YouTube page to sample burned-in subtitles and whiteboard frames for reading.
