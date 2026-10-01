#!/usr/bin/env bash
# Khởi chạy ứng dụng Mouse Helper (Ubuntu Native Desktop App)
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================="
echo "    KHỞI CHẠY MOUSE HELPER (UBUNTU NATIVE DESKTOP APP)    "
echo "=========================================================="

# Kiểm tra thư viện
python3 -c "import Xlib, pynput, gi; gi.require_version('Gtk', '3.0')" 2>/dev/null || {
    echo "Đang cài đặt thư viện cần thiết..."
    pip install python-xlib pynput --break-system-packages
}

echo "Khởi động ứng dụng..."
python3 main_gui.py
