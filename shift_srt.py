import re
from pathlib import Path
import sys

TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")

def to_millis(h, m, s, ms):
    return ((int(h) * 3600 + int(m) * 60 + int(s)) * 1000) + int(ms)

def from_millis(total_ms):
    if total_ms < 0:
        total_ms = 0
    h = total_ms // 3600000
    total_ms %= 3600000
    m = total_ms // 60000
    total_ms %= 60000
    s = total_ms // 1000
    ms = total_ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def shift_srt_text(srt_text, offset_ms):
    def repl(match):
        h, m, s, ms = match.groups()
        original = to_millis(h, m, s, ms)
        return from_millis(original + offset_ms)
    return TIME_RE.sub(repl, srt_text)

def main():
    srt_path = input("Path to .srt file: ").strip().strip('"')
    path = Path(srt_path)

    if not path.exists():
        print("File not found.")
        sys.exit(1)
    if path.suffix.lower() != ".srt":
        print("Please provide a .srt file.")
        sys.exit(1)

    seconds = float(input("Offset seconds: ").strip())
    milliseconds = float(input("Offset milliseconds: ").strip())

    offset_ms = int(round(seconds * 1000 + milliseconds))

    original = path.read_text(encoding="utf-8", errors="replace")
    updated = shift_srt_text(original, offset_ms)

    out_path = path.with_name(path.stem + f"_shifted_{offset_ms}ms" + path.suffix)
    out_path.write_text(updated, encoding="utf-8", errors="replace")
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
