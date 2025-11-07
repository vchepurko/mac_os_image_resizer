#!/bin/bash
# === resize-one.command ===
cd "$(dirname "$0")"

# Вибір файлу
file=$(osascript -e 'set f to choose file with prompt "Оберіть зображення для зміни розміру:"' -e 'POSIX path of f')
if [ -z "$file" ]; then
  echo "Файл не обрано."
  exit 1
fi

# Запит розміру
size=$(osascript -e 'text returned of (display dialog "Введіть максимальний розмір (px):" default answer "1024")')
if [ -z "$size" ]; then
  echo "Розмір не вказано."
  exit 1
fi

python3 resizer.py "$file" "$size"
read -p "Готово. Натисніть Enter, щоб закрити..."