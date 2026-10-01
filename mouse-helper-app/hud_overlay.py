"""
Cửa sổ hiển thị trạng thái khoá trục HUD nổi trên màn hình Ubuntu (hud_overlay.py)
Sử dụng GTK 3 thuần tuý với CSS Styling, không phụ thuộc vào gi-cairo.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from config import config

HUD_CSS = b"""
.hud-window {
    background-color: transparent;
}

.hud-pill {
    background-color: rgba(15, 23, 42, 0.94);
    border: 2px solid #00f0ff;
    border-radius: 20px;
    padding: 6px 14px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
}

.hud-text {
    color: #00f0ff;
    font-weight: bold;
    font-size: 12px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.hud-delta {
    color: #94a3b8;
    font-family: monospace;
    font-size: 11px;
}
"""

class HudOverlay(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.POPUP)

        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)

        # Style context
        self.get_style_context().add_class("hud-window")
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(HUD_CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        screen = Gdk.Screen.get_default()
        rgba_visual = screen.get_rgba_visual()
        if rgba_visual:
            self.set_visual(rgba_visual)

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Container
        self.hud_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.hud_box.get_style_context().add_class("hud-pill")

        self.lbl_text = Gtk.Label()
        self.lbl_text.get_style_context().add_class("hud-text")
        self.hud_box.pack_start(self.lbl_text, True, True, 0)

        self.lbl_delta = Gtk.Label()
        self.lbl_delta.get_style_context().add_class("hud-delta")
        self.hud_box.pack_start(self.lbl_delta, True, True, 0)

        self.add(self.hud_box)

    def update_state(self, telemetry):
        """Cập nhật dữ liệu từ MouseLockEngine."""
        GLib.idle_add(self._apply_telemetry, telemetry)

    def _apply_telemetry(self, t):
        is_locked = t.get("is_locked", False)
        if not is_locked or not config.get("show_hud", True) or not config.get("enabled", True):
            self.hide()
            return False

        axis = t.get("axis", "x")
        cur_x = t.get("cur_x", 0)
        cur_y = t.get("cur_y", 0)
        anchor_x = t.get("anchor_x", cur_x)
        anchor_y = t.get("anchor_y", cur_y)

        axis_label = "🔒 KHOÁ TRỤC X (NGANG)" if axis == "x" else "🔒 KHOÁ TRỤC Y (DỌC)"
        delta = (cur_x - anchor_x) if axis == "x" else (cur_y - anchor_y)
        sign = "+" if delta >= 0 else ""

        self.lbl_text.set_text(axis_label)
        self.lbl_delta.set_text(f"Δ: {sign}{int(delta)}px")

        # Đặt vị trí cửa sổ kế cận con trỏ chuột
        win_x = cur_x + 22
        win_y = cur_y + 22
        if win_x + 240 > self.screen_width:
            win_x = cur_x - 240
        if win_y + 40 > self.screen_height:
            win_y = cur_y - 40

        self.move(win_x, win_y)
        self.show_all()
        return False
