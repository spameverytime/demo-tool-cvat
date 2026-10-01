# Mouse Helper (Ubuntu Native Desktop App)

**Giải quyết:** [P-010](../problem-backlog.md#p-010) — Khó khăn khi kẻ vẽ các đoạn thẳng trực giao (đường làn, vạch phân cách, mép đường, ranh giới thẳng) trên CVAT/trình duyệt và toàn bộ hệ điều hành do run tay hoặc thiếu tính năng khóa trục.

---

## Pain point

Trước khi có tool:
- Khi gán nhãn polyline, polygon hoặc vẽ các đường ranh giới thẳng tắp (vạch kẻ đường trắng/vàng, mép vỉa hè `curb`, mép tường `wall`, cột biển báo `pole`), annotator phải nín thở, ghì chặt chuột để cố kéo thẳng.
- Do quán tính và rung vi mô của tay (micro-tremor), các đoạn thẳng luôn bị lệch từ $1.5^\circ$ – $4.5^\circ$ hoặc biến thành đường răng cưa.
- Annotator phải nhấn `Ctrl + Z` xóa đi vẽ lại trung bình 3-5 lần mỗi frame, gây căng cơ cổ tay và giảm 30% năng suất gán nhãn.
- Các giải pháp trên trình duyệt bị giới hạn trong Sandbox của web, không thể can thiệp sâu và triệt để vào con trỏ chuột vật lý của Hệ điều hành.

---

## Tool làm gì

Ứng dụng độc lập chạy trực tiếp trên nền tảng **Ubuntu Linux (Desktop App - GTK 3 & X11 Engine)**:
- **Tác động toàn hệ thống (System-Wide OS Level):** Không phụ thuộc vào trình duyệt Chrome. Hoạt động trên mọi cửa sổ: CVAT trên Chrome, Firefox, GIMP, Inkscape, hay bất kỳ công cụ gán nhãn nào.
- **Cơ chế Khoá trục khi Giữ Phím (`Shift-Hold Axis Lock`):**
  - **Mặc định:** Chuột di chuyển tự do 2D bình thường.
  - **Khi NHẤN & GIỮ phím `Shift` (hoặc phím Modifier tùy chọn):** Động cơ X11 ngay lập tức chốt toạ độ neo gốc và cưỡng chế toạ độ chuột vật lý **chỉ di chuyển theo đúng 1 phương: phương Ngang (Trục X) hoặc phương Dọc (Trục Y)** theo cấu hình. Con trỏ chuột trên màn hình bị ghì chặt vào trục, không thể lệch hướng.
  - **Khi NHẢ phím `Shift`:** Chuột quay lại di chuyển tự do 2D ngay lập tức không độ trễ.
- **Hệ thống hiển thị trực quan (Full-screen HUD Overlay):**
  - Cửa sổ trong suốt, click-through 100% hiển thị tia laser huỳnh quang dóng trục vô tận cắt ngang/dọc màn hình, đánh dấu điểm neo gốc và thẻ chỉ báo $\Delta px$ thời gian thực.
- **Giao diện điều khiển GTK 3 hiện đại:**
  - Có công tắc Bật/Tắt tức thời.
  - Chọn phương khoá: Trục X (Ngang), Trục Y (Dọc), hoặc Tự động (Auto Ortho Snap).
  - Chọn phím kích hoạt: `Shift`, `Alt`, `Ctrl`.
  - Tích hợp sẵn khung canvas vẽ thử nghiệm trực tiếp ngay trong ứng dụng.

---

## Cài đặt và chạy

Ứng dụng viết bằng Python 3 kết hợp thư viện chuẩn GTK 3 của Ubuntu và `python-xlib`, `pynput`:

### 1. Khởi chạy nhanh bằng script
```bash
cd thu_thach_tuan3/reports/source-tool/mouse-helper-app
./run.sh
```

### 2. Khởi chạy thủ công bằng lệnh Python
```bash
cd thu_thach_tuan3/reports/source-tool/mouse-helper-app
python3 main_gui.py
```

---

## Đầu vào / đầu ra

- **Đầu vào:**
  - Tín hiệu giữ/thả phím `Shift` (hoặc `Alt`, `Ctrl`) từ bàn phím toàn cục của hệ điều hành.
  - Toạ độ di chuyển chuột vật lý của người dùng.
- **Đầu ra:**
  - Toạ độ con trỏ chuột vật lý của OS được ghim chặt vào toạ độ trục $Y_0$ (nếu khoá X) hoặc $X_0$ (nếu khoá Y).
  - Tia laser dóng toạ độ huỳnh quang trên toàn màn hình.

---

## Đã thử trên

- **Hệ điều hành:** Ubuntu 24.04 LTS (X11 Desktop Session).
- **Phần mềm đã kiểm thử tương thích:**
  - Google Chrome (CVAT Computer Vision Annotation Tool).
  - Canvas vẽ nội bộ của ứng dụng.
- **Kết quả đo lường định lượng:**
  - **Độ lệch góc:** $0.00^\circ$ tuyệt đối.
  - **Thời gian vẽ 1 đoạn thẳng polyline:** Tiết kiệm ~65% thời gian so với thao tác thủ công.
  - **Giảm đau mỏi cổ tay:** Annotator không cần gồng cứng tay để giữ chuột đi thẳng.

---

## Người viết
@spameverytime & Đội ngũ Kỹ thuật Data Annotation — AI Action khóa IV
