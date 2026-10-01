"""
Module động cơ khoá trục di chuyển chuột phần cứng (mouse_lock_engine.py)
Giao tiếp trực tiếp với X11 Server thông qua python-xlib và pynput.
"""

import time
import threading
from pynput import keyboard
from Xlib import display, X

from config import config

class MouseLockEngine:
    def __init__(self, telemetry_callback=None):
        self.telemetry_callback = telemetry_callback
        self.running = False
        
        # Trạng thái khoá
        self.is_modifier_pressed = False
        self.is_locked = False
        self.anchor_x = None
        self.anchor_y = None
        self.current_x = 0
        self.current_y = 0
        self.auto_axis = None
        
        # Kết nối X11 Display
        self.x_display = None
        self.x_root = None
        self._init_x11()

        # Keyboard listener
        self.kb_listener = None
        self.worker_thread = None

    def _init_x11(self):
        try:
            self.x_display = display.Display()
            self.x_root = self.x_display.screen().root
        except Exception as e:
            print(f"[Engine] Lỗi khởi tạo kết nối X11: {e}")

    def is_target_key(self, key):
        """Kiểm tra phím có khớp với cấu hình phím bổ trợ hay không."""
        target = config.get("modifier_key", "shift").lower()
        
        if target == "shift":
            return key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r)
        elif target == "alt":
            return key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)
        elif target == "ctrl":
            return key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r)
        return False

    def on_key_press(self, key):
        if not config.get("enabled", True):
            return

        if self.is_target_key(key):
            if not self.is_modifier_pressed:
                self.is_modifier_pressed = True
                # Lấy toạ độ chuột hiện tại làm điểm neo
                self.acquire_anchor()

    def on_key_release(self, key):
        if self.is_target_key(key):
            self.is_modifier_pressed = False
            self.is_locked = False
            self.anchor_x = None
            self.anchor_y = None
            self.auto_axis = None
            self.notify_telemetry()

    def acquire_anchor(self):
        """Ghi nhận toạ độ bắt đầu khoá trục."""
        if not self.x_root:
            return
        try:
            ptr = self.x_root.query_pointer()
            self.anchor_x = ptr.root_x
            self.anchor_y = ptr.root_y
            self.current_x = ptr.root_x
            self.current_y = ptr.root_y
            self.is_locked = True
            self.auto_axis = None
            self.notify_telemetry()
        except Exception as e:
            print(f"[Engine] Lỗi lấy điểm neo: {e}")

    def notify_telemetry(self):
        if self.telemetry_callback:
            axis_mode = config.get("axis_mode", "x")
            effective_axis = self.auto_axis if axis_mode == "auto" else axis_mode
            self.telemetry_callback({
                "is_pressed": self.is_modifier_pressed,
                "is_locked": self.is_locked,
                "axis": effective_axis,
                "cur_x": self.current_x,
                "cur_y": self.current_y,
                "anchor_x": self.anchor_x,
                "anchor_y": self.anchor_y
            })

    def run_clamp_loop(self):
        """Vòng lặp tốc độ cao (~200Hz) ghì chặt toạ độ chuột vật lý của OS."""
        print("[Engine] Bắt đầu vòng lặp khoá trục chuột...")
        
        while self.running:
            if not config.get("enabled", True):
                time.sleep(0.05)
                continue

            if self.is_modifier_pressed and self.x_root:
                try:
                    ptr = self.x_root.query_pointer()
                    cur_x, cur_y = ptr.root_x, ptr.root_y
                    self.current_x = cur_x
                    self.current_y = cur_y

                    if self.anchor_x is None or self.anchor_y is None:
                        self.anchor_x = cur_x
                        self.anchor_y = cur_y

                    axis_mode = config.get("axis_mode", "x")
                    
                    # Xử lý chế độ Tự động (Auto Ortho Snap)
                    if axis_mode == "auto":
                        if self.auto_axis is None:
                            dx = abs(cur_x - self.anchor_x)
                            dy = abs(cur_y - self.anchor_y)
                            threshold = config.get("auto_threshold", 6)
                            if dx >= threshold or dy >= threshold:
                                self.auto_axis = "x" if dx >= dy else "y"
                        effective_axis = self.auto_axis or "x"
                    else:
                        effective_axis = axis_mode

                    need_warp = False
                    target_x = cur_x
                    target_y = cur_y

                    if effective_axis == "x":
                        # KHOÁ TRỤC X: Giữ cố định Y tại anchor_y, cho phép X tự do
                        if cur_y != self.anchor_y:
                            target_x = cur_x
                            target_y = self.anchor_y
                            need_warp = True
                    elif effective_axis == "y":
                        # KHOÁ TRỤC Y: Giữ cố định X tại anchor_x, cho phép Y tự do
                        if cur_x != self.anchor_x:
                            target_x = self.anchor_x
                            target_y = cur_y
                            need_warp = True

                    if need_warp:
                        self.x_root.warp_pointer(int(target_x), int(target_y))
                        self.x_display.sync()
                        self.current_x = target_x
                        self.current_y = target_y

                    self.notify_telemetry()
                except Exception as e:
                    # Tự khôi phục kết nối X11 nếu đứt đoạn
                    self._init_x11()
                    time.sleep(0.02)

                time.sleep(0.005) # 200 Hz
            else:
                # Khi không giữ Shift, ngủ nhẹ để tiết kiệm CPU
                time.sleep(0.015)

    def start(self):
        """Khởi động engine."""
        self.running = True
        
        # Bắt đầu luồng khoá chuột
        self.worker_thread = threading.Thread(target=self.run_clamp_loop, daemon=True)
        self.worker_thread.start()

        # Bắt đầu lắng nghe bàn phím
        self.kb_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.kb_listener.start()
        print("[Engine] Engine khoá trục chuột đã sẵn sàng.")

    def stop(self):
        """Dừng engine."""
        self.running = False
        if self.kb_listener:
            self.kb_listener.stop()
        print("[Engine] Engine đã dừng.")
