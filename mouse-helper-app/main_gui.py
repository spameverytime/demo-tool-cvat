"""
Giao diện đồ hoạ chính ứng dụng Mouse Helper (Ubuntu Native Desktop App - GTK 3)
Cho phép điều khiển và khoá cứng toạ độ chuột vật lý trên toàn bộ hệ điều hành Ubuntu.
Thuần GTK 3 Widgets & CSS, hoạt động tin cậy 100% không phụ thuộc cairo binding.
"""

import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from config import config
from mouse_lock_engine import MouseLockEngine
from hud_overlay import HudOverlay

APP_CSS = b"""
window {
    background-color: #0b1120;
    color: #f8fafc;
}

headerbar {
    background-color: #0f172a;
    border-bottom: 1px solid #1e293b;
    color: #ffffff;
}

.card {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}

.card-title {
    font-size: 13px;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 8px;
}

.stat-box {
    background-color: #030712;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 12px 16px;
}

.stat-label {
    color: #94a3b8;
    font-size: 11px;
}

.stat-val {
    color: #f8fafc;
    font-family: monospace;
    font-size: 14px;
    font-weight: bold;
}

.stat-val-locked {
    color: #00f0ff;
    font-family: monospace;
    font-size: 15px;
    font-weight: bold;
}

.test-pad {
    background-color: #030712;
    border: 2px dashed #0284c7;
    border-radius: 10px;
    padding: 24px;
}

.test-hint {
    color: #cbd5e1;
    font-size: 12px;
}

.btn-primary {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: white;
    font-weight: bold;
    border-radius: 6px;
    border: none;
    padding: 8px 16px;
}

radiobutton {
    font-size: 13px;
    color: #e2e8f0;
}
"""

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Mouse Helper - Ortho Axis Lock (Ubuntu Native)")
        self.set_default_size(720, 580)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Áp dụng Custom CSS
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(APP_CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Khởi tạo HUD Overlay
        self.hud = HudOverlay()

        # Khởi tạo Engine điều khiển chuột
        self.engine = MouseLockEngine(telemetry_callback=self.on_telemetry_update)

        self._build_ui()
        self.engine.start()

        self.connect("destroy", self.on_window_destroy)

    def _build_ui(self):
        # 1. HeaderBar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Mouse Helper (Ubuntu Native)"
        header.props.subtitle = "Khoá cứng trục di chuyển chuột phần cứng trên Ubuntu"
        self.set_titlebar(header)

        # Master Switch trên Header
        self.master_switch = Gtk.Switch()
        self.master_switch.set_active(config.get("enabled", True))
        self.master_switch.connect("notify::active", self.on_master_switch_changed)
        header.pack_end(self.master_switch)

        lbl_switch = Gtk.Label(label="Trạng thái: ")
        header.pack_end(lbl_switch)

        # 2. Main Container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        main_box.set_margin_top(18)
        main_box.set_margin_bottom(18)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        self.add(main_box)

        # Hàng 1: Hai Card cạnh nhau (Phương khoá trục & Phím kích hoạt)
        row_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        main_box.pack_start(row_top, False, False, 0)

        # Card 1: Phương Khoá Trục
        card_axis = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card_axis.get_style_context().add_class("card")
        row_top.pack_start(card_axis, True, True, 0)

        lbl_axis = Gtk.Label(label="🎯 PHƯƠNG KHOÁ TRỤC (KHI GIỮ SHIFT)")
        lbl_axis.set_halign(Gtk.Align.START)
        lbl_axis.get_style_context().add_class("card-title")
        card_axis.pack_start(lbl_axis, False, False, 0)

        current_mode = config.get("axis_mode", "x")
        self.radio_x = Gtk.RadioButton.new_with_label_from_widget(None, "Trục X (Chỉ di chuyển ngang)")
        self.radio_y = Gtk.RadioButton.new_with_label_from_widget(self.radio_x, "Trục Y (Chỉ di chuyển dọc)")
        self.radio_auto = Gtk.RadioButton.new_with_label_from_widget(self.radio_x, "Tự động (Theo hướng ban đầu)")

        if current_mode == "x": self.radio_x.set_active(True)
        elif current_mode == "y": self.radio_y.set_active(True)
        else: self.radio_auto.set_active(True)

        self.radio_x.connect("toggled", self.on_axis_radio_toggled, "x")
        self.radio_y.connect("toggled", self.on_axis_radio_toggled, "y")
        self.radio_auto.connect("toggled", self.on_axis_radio_toggled, "auto")

        card_axis.pack_start(self.radio_x, False, False, 0)
        card_axis.pack_start(self.radio_y, False, False, 0)
        card_axis.pack_start(self.radio_auto, False, False, 0)

        # Card 2: Cài Đặt Phím & HUD
        card_key = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card_key.get_style_context().add_class("card")
        row_top.pack_start(card_key, True, True, 0)

        lbl_key_title = Gtk.Label(label="⚙️ PHÍM KÍCH HOẠT & HIỂN THỊ")
        lbl_key_title.set_halign(Gtk.Align.START)
        lbl_key_title.get_style_context().add_class("card-title")
        card_key.pack_start(lbl_key_title, False, False, 0)

        box_select = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lbl_sel = Gtk.Label(label="Phím kích hoạt:")
        box_select.pack_start(lbl_sel, False, False, 0)

        self.combo_key = Gtk.ComboBoxText()
        self.combo_key.append("shift", "Phím Shift (Mặc định)")
        self.combo_key.append("alt", "Phím Alt")
        self.combo_key.append("ctrl", "Phím Ctrl")
        self.combo_key.set_active_id(config.get("modifier_key", "shift"))
        self.combo_key.connect("changed", self.on_modifier_key_changed)
        box_select.pack_end(self.combo_key, True, True, 0)
        card_key.pack_start(box_select, False, False, 0)

        self.chk_hud = Gtk.CheckButton(label="Hiển thị thẻ trạng thái HUD nổi trên màn hình")
        self.chk_hud.set_active(config.get("show_hud", True))
        self.chk_hud.connect("toggled", self.on_hud_toggled)
        card_key.pack_start(self.chk_hud, False, False, 0)

        # Card 3: Bảng Thông Số Thời Gian Thực (Telemetry)
        card_telemetry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card_telemetry.get_style_context().add_class("card")
        main_box.pack_start(card_telemetry, False, False, 0)

        lbl_tele_title = Gtk.Label(label="📊 THÔNG SỐ CON TRỎ CHUỘT THỜI GIAN THỰC")
        lbl_tele_title.set_halign(Gtk.Align.START)
        lbl_tele_title.get_style_context().add_class("card-title")
        card_telemetry.pack_start(lbl_tele_title, False, False, 0)

        stat_grid = Gtk.Grid()
        stat_grid.set_column_spacing(24)
        stat_grid.set_row_spacing(8)
        stat_grid.get_style_context().add_class("stat-box")

        lbl_t1 = Gtk.Label(label="Toạ độ chuột OS:")
        lbl_t1.get_style_context().add_class("stat-label")
        lbl_t1.set_halign(Gtk.Align.START)
        self.lbl_pos_val = Gtk.Label(label="X: 0, Y: 0")
        self.lbl_pos_val.get_style_context().add_class("stat-val")
        self.lbl_pos_val.set_halign(Gtk.Align.START)

        lbl_t2 = Gtk.Label(label="Trạng thái phím:")
        lbl_t2.get_style_context().add_class("stat-label")
        lbl_t2.set_halign(Gtk.Align.START)
        self.lbl_key_val = Gtk.Label(label="ĐANG THẢ (Tự do)")
        self.lbl_key_val.get_style_context().add_class("stat-val")
        self.lbl_key_val.set_halign(Gtk.Align.START)

        lbl_t3 = Gtk.Label(label="Khoá phần cứng:")
        lbl_t3.get_style_context().add_class("stat-label")
        lbl_t3.set_halign(Gtk.Align.START)
        self.lbl_lock_val = Gtk.Label(label="TỰ DO (2 chiều)")
        self.lbl_lock_val.get_style_context().add_class("stat-val")
        self.lbl_lock_val.set_halign(Gtk.Align.START)

        stat_grid.attach(lbl_t1, 0, 0, 1, 1)
        stat_grid.attach(self.lbl_pos_val, 1, 0, 1, 1)
        stat_grid.attach(lbl_t2, 2, 0, 1, 1)
        stat_grid.attach(self.lbl_key_val, 3, 0, 1, 1)
        stat_grid.attach(lbl_t3, 4, 0, 1, 1)
        stat_grid.attach(self.lbl_lock_val, 5, 0, 1, 1)

        card_telemetry.pack_start(stat_grid, False, False, 0)

        # Card 4: Khu vực Thử Nghiệm Tương Tác
        card_test = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card_test.get_style_context().add_class("test-pad")
        main_box.pack_start(card_test, True, True, 0)

        lbl_test_title = Gtk.Label(label="🧪 KHU VỰC THỬ NGHIỆM THỰC TẾ")
        lbl_test_title.set_halign(Gtk.Align.START)
        lbl_test_title.get_style_context().add_class("card-title")
        card_test.pack_start(lbl_test_title, False, False, 0)

        lbl_guide = Gtk.Label()
        lbl_guide.set_markup(
            "<span color='#cbd5e1'>"
            "1. <b>Thử nghiệm bình thường:</b> Di chuyển chuột tự do qua lại trên màn hình.\n"
            "2. <b>Thử nghiệm khoá trục:</b> <b>NHẤN &amp; GIỮ phím Shift</b> và di chuyển chuột.\n"
            "   👉 Chuột vật lý của bạn sẽ bị <b>ghì chặt hoàn toàn theo phương ngang (X)</b> hoặc <b>phương dọc (Y)</b>!\n"
            "   👉 Dù bạn cố di chuột chéo hay lắc tay lên/xuống, con trỏ trên màn hình vẫn chỉ trượt thẳng tắp!\n"
            "3. <b>Thao tác mọi nơi:</b> Thu nhỏ cửa sổ này và mở <b>Chrome / CVAT / GIMP</b> — tính năng hoạt động trên toàn bộ hệ thống!"
            "</span>"
        )
        lbl_guide.set_line_wrap(True)
        lbl_guide.set_halign(Gtk.Align.START)
        card_test.pack_start(lbl_guide, False, False, 0)

    # --- SỰ KIỆN CẤU HÌNH ---
    def on_master_switch_changed(self, switch, gparam):
        is_on = switch.get_active()
        config.set("enabled", is_on)

    def on_axis_radio_toggled(self, button, mode):
        if button.get_active():
            config.set("axis_mode", mode)

    def on_modifier_key_changed(self, combo):
        key_id = combo.get_active_id()
        if key_id:
            config.set("modifier_key", key_id)

    def on_hud_toggled(self, button):
        config.set("show_hud", button.get_active())

    # --- TELEMETRY TỪ ENGINE ---
    def on_telemetry_update(self, data):
        self.hud.update_state(data)
        GLib.idle_add(self._update_ui_telemetry, data)

    def _update_ui_telemetry(self, data):
        self.lbl_pos_val.set_text(f"X: {data['cur_x']}, Y: {data['cur_y']}")

        if data["is_pressed"]:
            self.lbl_key_val.set_markup("<span color='#38bdf8'><b>ĐANG GIỮ</b></span>")
        else:
            self.lbl_key_val.set_text("ĐANG THẢ")

        if data["is_locked"]:
            axis_name = "TRỤC X (NGANG)" if data["axis"] == "x" else "TRỤC Y (DỌC)"
            self.lbl_lock_val.set_markup(f"<span color='#00f0ff'><b>🔒 {axis_name}</b></span>")
        else:
            self.lbl_lock_val.set_text("TỰ DO (2 chiều)")
        return False

    def on_window_destroy(self, widget):
        self.engine.stop()
        self.hud.destroy()
        Gtk.main_quit()

def main():
    win = MainWindow()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
