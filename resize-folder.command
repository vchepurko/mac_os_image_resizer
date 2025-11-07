#!/bin/bash
# === resize-folder.command ===
cd "$(dirname "$0")"

folder=$(osascript -e 'set f to choose folder with prompt "Оберіть папку для обробки:"' -e 'POSIX path of f')
if [ -z "$folder" ]; then
  echo "❌ Папку не обрано."
  exit 1
fi

size=$(osascript -e 'text returned of (display dialog "Введіть максимальний розмір (px):" default answer "1024")')
if [ -z "$size" ]; then
  echo "❌ Розмір не вказано."
  exit 1
fi

cd "$folder"
python3 "$(dirname "$0")/resize_all.py" "$size"
read -p "✅ Готово. Натисніть Enter, щоб закрити..."