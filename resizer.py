#!/usr/bin/env python3
"""
resize_image.py — масштабує зображення до max_px (по довшій стороні)
і зберігає копію з суфіксом _<max_px> перед розширенням.

Використання:
    python resize_image.py input.jpg 800
    python resize_image.py "path/to/img with space.png" 1200
"""

import sys
import os
from PIL import Image, ImageOps

def build_output_path(inp_path: str, max_px: int) -> str:
    d, fname = os.path.split(inp_path)
    base, ext = os.path.splitext(fname)
    # нормалізуємо розширення (залишаємо оригінальне)
    out_name = f"{base}_{max_px}{ext}"
    out_path = os.path.join(d, out_name)

    # якщо файл існує — додати лічильник
    if os.path.exists(out_path):
        i = 2
        while True:
            cand = os.path.join(d, f"{base}_{max_px}-{i}{ext}")
            if not os.path.exists(cand):
                return cand
            i += 1
    return out_path

def main():
    if len(sys.argv) < 3:
        print("Помилка: потрібні аргументи <шлях_до_файлу> <max_px>")
        sys.exit(1)

    inp_path = sys.argv[1]
    try:
        max_px = int(sys.argv[2])
        if max_px <= 0:
            raise ValueError
    except ValueError:
        print("Помилка: <max_px> має бути додатним цілим числом.")
        sys.exit(1)

    if not os.path.isfile(inp_path):
        print(f"Помилка: файл не знайдено: {inp_path}")
        sys.exit(1)

    # Відкриваємо зображення та застосовуємо EXIF-орієнтацію
    with Image.open(inp_path) as im:
        im = ImageOps.exif_transpose(im)
        orig_w, orig_h = im.size

        # Якщо вже менше/рівне max — все одно збережемо копію (часто зручно)
        scale = min(max_px / orig_w, max_px / orig_h, 1.0) if max(orig_w, orig_h) > max_px else min(max_px / max(orig_w, orig_h), 1.0)
        new_w = max(1, int(round(orig_w * scale)))
        new_h = max(1, int(round(orig_h * scale)))

        # Масштабування з якісним ресемплінгом
        if (new_w, new_h) != (orig_w, orig_h):
            im = im.resize((new_w, new_h), Image.LANCZOS)

        out_path = build_output_path(inp_path, max_px)

        # Параметри збереження
        fmt = (im.format or '').upper()
        save_kwargs = {}

        # Спроба зберегти EXIF (зазвичай працює для JPEG)
        exif = im.info.get("exif")
        if exif:
            save_kwargs["exif"] = exif

        if fmt in ("JPG", "JPEG"):
            # Якість і прогресивне збереження
            save_kwargs.update(dict(quality=90, optimize=True, progressive=True))
        elif fmt == "PNG":
            save_kwargs.update(dict(optimize=True))
        elif fmt == "WEBP":
            # Збереження прозорості/якості
            save_kwargs.update(dict(quality=90, method=6))

        # Якщо формат невідомий — збережемо під тим самим розширенням
        im.save(out_path, **save_kwargs)
        print(f"Готово: {out_path} ({orig_w}x{orig_h} -> {new_w}x{new_h})")

if __name__ == "__main__":
    main()
