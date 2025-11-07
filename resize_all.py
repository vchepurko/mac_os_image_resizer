#!/usr/bin/env python3
"""
Resize all images in the current directory and subdirectories.
Skips already resized files (e.g., resized_1024_IMG_6244.jpg).
Usage:
  resize-all <max_size> [--dry-run]
"""

import os
import sys
import re
from PIL import Image

VALID_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".heic")

RE_RESIZED_PREFIX = re.compile(r'^resized_\d+_', re.IGNORECASE)
RE_WP_SIZED = re.compile(r'[-_]\d{2,5}x\d{2,5}(?=\.[a-zA-Z]+$)')

def is_resized_file(filename: str) -> bool:
    """Skip if already has resized_ prefix or WP size suffix."""
    return bool(RE_RESIZED_PREFIX.search(filename) or RE_WP_SIZED.search(filename))

def get_new_name(filename: str, max_size: int) -> str:
    """Add prefix resized_<size>_ to the original filename."""
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    base, ext = os.path.splitext(basename)
    ext = ext.lower()
    return os.path.join(dirname, f"resized_{max_size}_{base}{ext}")

def resize_image(path: str, max_size: int, dry_run: bool = False) -> tuple[bool, str]:
    try:
        ext = os.path.splitext(path)[1].lower()
        target_ext = ".jpg" if ext == ".heic" else ext

        with Image.open(path) as img:
            img.load()
            if target_ext in (".jpg", ".jpeg") and img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            orig_w, orig_h = img.size
            if max(orig_w, orig_h) <= max_size:
                return (False, f"skip (already <= {max_size}px)")

            img.thumbnail((max_size, max_size))
            new_path = get_new_name(path, max_size)

            if dry_run:
                return (True, f"DRY-RUN → would create: {os.path.basename(new_path)} ({orig_w}x{orig_h} → {img.size[0]}x{img.size[1]})")

            img.save(new_path, quality=88, optimize=True)
            return (True, f"{os.path.basename(new_path)} ({orig_w}x{orig_h} → {img.size[0]}x{img.size[1]})")

    except Exception as e:
        return (False, f"ERROR: {e}")

def main():
    if len(sys.argv) < 2:
        print("❌ Використання: resize-all <max_size> [--dry-run]")
        sys.exit(1)

    dry_run = ('--dry-run' in sys.argv)
    try:
        max_size = int(sys.argv[1])
    except ValueError:
        print("❌ max_size має бути числом.")
        sys.exit(1)

    print(f"🔍 Пошук зображень у: {os.getcwd()}")
    if dry_run:
        print("🧪 Режим: DRY-RUN (файли НЕ створюються)")

    found = 0
    processed = 0
    skipped = 0
    errors = 0

    for root, _, files in os.walk('.'):
        for name in files:
            lower = name.lower()
            if not lower.endswith(VALID_EXTS):
                continue
            found += 1
            if is_resized_file(lower):
                skipped += 1
                continue

            full_path = os.path.join(root, name)
            ok, msg = resize_image(full_path, max_size, dry_run=dry_run)
            rel = os.path.relpath(full_path)
            if ok:
                processed += 1
                print(f"{rel} → {msg}")
            else:
                if "ERROR" in msg:
                    errors += 1
                    print(f"{rel} → {msg}")
                else:
                    skipped += 1
                    # print(f"↩︎ {rel} → {msg}")

    print("\n— РЕЗЮМЕ —")
    print(f"  Знайдено файлів:      {found}")
    print(f"  Оброблено:            {processed}")
    print(f"  Пропущено:            {skipped}")
    print(f"  Помилок:              {errors}")
    if dry_run:
        print("  Примітка: DRY-RUN — нові файли не створювались.")

if __name__ == "__main__":
    main()