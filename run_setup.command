#!/bin/bash
cd "$(dirname "$0")"
echo "Запуск, встановлення..."
chmod +x setup_resizer.sh
./setup_resizer.sh
read -p "Готово! Натисніть Enter, щоб закрити..."