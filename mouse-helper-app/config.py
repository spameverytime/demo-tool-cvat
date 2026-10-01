"""
Module quản lý cấu hình cho ứng dụng Mouse Helper (Ubuntu Native App).
"""

import json
import os
import threading

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

DEFAULT_CONFIG = {
    "enabled": True,
    "axis_mode": "x",        # 'x' (Ngang), 'y' (Dọc), 'auto' (Tự động nhận diện hướng)
    "modifier_key": "shift", # 'shift', 'alt', 'ctrl'
    "auto_threshold": 6,     # Số pixel di chuyển ban đầu để chốt trục trong chế độ auto
    "show_hud": True,        # Hiển thị đường dóng trực quan
    "guide_color": "#00f0ff" # Màu tia laser huỳnh quang
}

class AppConfig:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = dict(DEFAULT_CONFIG)
        self.load()

    def load(self):
        with self.lock:
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        saved = json.load(f)
                        self.data.update(saved)
                except Exception as e:
                    print(f"[Config] Lỗi khi nạp file cài đặt: {e}")

    def save(self):
        with self.lock:
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[Config] Lỗi khi lưu file cài đặt: {e}")

    def get(self, key, default=None):
        with self.lock:
            return self.data.get(key, default)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
        self.save()

    def update(self, partial_dict):
        with self.lock:
            self.data.update(partial_dict)
        self.save()

# Instance toàn cục
config = AppConfig()
