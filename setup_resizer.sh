#!/bin/bash
# ==========================================
# 🛠️  Installer for image resizer tool
# Author: Vitaliy Chepurko edition
# ==========================================

set -e

echo "🔍 Перевірка Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 не знайдено. Встанови Python 3 і спробуй знову."
    exit 1
fi
echo "Python знайдено: $(python3 --version)"

# === Встановлюємо залежності ===
echo "📦 Встановлюємо Pillow..."
python3 -m pip install --upgrade pip >/dev/null 2>&1
python3 -m pip install pillow --user >/dev/null 2>&1
echo "Pillow готовий."

# === Створюємо виконуваний файл ===
INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/resize"
SCRIPT_PATH="$(pwd)/resizer.py"

mkdir -p "$INSTALL_DIR"

cat <<EOF > "$TARGET"
#!/bin/bash
python3 "$SCRIPT_PATH" "\$@"
EOF

chmod +x "$TARGET"
echo "Створено: $TARGET"


# === Додаємо resize-all ===
TARGET_ALL="$INSTALL_DIR/resize-all"
SCRIPT_ALL_PATH="$(pwd)/resize_all.py"

cat <<EOF > "$TARGET_ALL"
#!/bin/bash
python3 "$SCRIPT_ALL_PATH" "\$@"
EOF

chmod +x "$TARGET_ALL"
echo "Створено: $TARGET_ALL (рекурсивний режим)"

# === Додаємо у PATH (для zsh і bash) ===
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Додаємо $INSTALL_DIR у PATH..."
    if [[ -n "$ZSH_VERSION" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "Додано у $SHELL_RC"
else
    echo "$INSTALL_DIR вже є у PATH"
fi

# === Перевірка PATH ===
echo "Оновлюємо PATH..."
export PATH="$INSTALL_DIR:$PATH"

# === Тест виконання ===
echo "🧪 Тест: resize --help"
if "$TARGET" --help >/dev/null 2>&1; then
    echo "Успіх! Тепер можна використовувати:"
    echo "resize IMG_6241.JPG 1024"
else
    echo "Перезапусти термінал або введи:"
    echo "source ~/.zshrc"
fi

