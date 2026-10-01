# Problem backlog

Những chỗ gặp trong lúc gán nhãn mà **guideline chưa trả lời được**, cộng các pain point về công cụ.

Ghi ngay khi gặp, kể cả lúc chưa biết xử lý thế nào. Một edge case không được ghi lại thì
mỗi người sẽ tự xử lý theo một kiểu — và đó là nguồn lớn nhất của nhãn không nhất quán.

> Các mục bên dưới là **ví dụ**, tên và link CVAT đều giả. Mẫu trống để copy nằm cuối file.

## Danh sách

| Mã | Tóm tắt | Loại | Mục guideline | Trạng thái | Kết quả |
|---|---|---|---|---|---|
| [P-001](#p-001) | Người ngồi sau xe máy: box riêng hay gộp với người lái | Guideline mơ hồ | §3.2 | ✅ Đã chốt | [QĐ-001](so-quyet-dinh.md#qđ-001) |
| [P-002](#p-002) | Xe bị che khuất hơn một nửa | Guideline chưa nói tới | §3.4 | ↗️ Hỏi BTC | — |
| [P-003](#p-003) | Phải vẽ lại box y hệt qua nhiều frame liên tiếp | Pain point công cụ | — | 🗣️ Đang bàn | — |
| [P-004](#p-004) | Pre-label dồn cục tại sống mũi khi mặt nghiêng che khuất | Guideline đã nói nhưng cần áp dụng | VF50 §2.2 | ✅ Đã chốt | [QĐ-003](so-quyet-dinh.md#qđ-003) |
| [P-005](#p-005) | Lỗi bắt chéo contour điểm bờ mí mắt và môi trong khi nhắm mắt / ngậm miệng | Guideline đã nói nhưng cần áp dụng | VF50 §2.3 | ✅ Đã chốt | [QĐ-004](so-quyet-dinh.md#qđ-004) |
| [P-006](#p-006) | Điểm bờ trên lông mày đặt trên trán và điểm mắt lệch bờ mi | Guideline đã nói nhưng cần áp dụng | VF50 §2.1 | ✅ Đã chốt | [QĐ-005](so-quyet-dinh.md#qđ-005) |
| [P-007](#p-007) | Sai cấu trúc ID mí mắt và khoảng cách 3 đoạn sống mũi không đều | Guideline đã nói nhưng cần áp dụng | VF50 §2.1, §2.4 | ✅ Đã chốt | [QĐ-006](so-quyet-dinh.md#qđ-006) |
| [P-008](#p-008) | Định vị điểm giải phẫu mắt nhắm, lỗ tai, chóp mũi trong Human Pose | Guideline đã nói nhưng cần áp dụng | Pose17 §2 | ✅ Đã chốt | [QĐ-007](so-quyet-dinh.md#qđ-007) |
| [P-009](#p-009) | Quên gán thuộc tính occluded cho khớp bị che khuất tương hỗ | Guideline đã nói nhưng cần áp dụng | Pose17 §3 | ✅ Đã chốt | [QĐ-008](so-quyet-dinh.md#qđ-008) |
| [P-010](#p-010) | Khó vẽ đường thẳng trực giao (đường làn, mép đường, bounding box) do rung tay và thiếu khóa trục | Pain point công cụ | BBox §3; Segmentation §3 | 🛠️ Làm tool | [mouse-helper-app](source-tool/mouse-helper-app/README.md) |

**Loại**

| Loại | Nghĩa là |
|---|---|
| Guideline chưa nói tới | Tình huống không có trong guideline |
| Guideline mơ hồ | Đọc guideline ra được hai cách hiểu trở lên |
| Guideline mâu thuẫn | Hai mục trong guideline nói ngược nhau |
| Pain point công cụ | Guideline rõ, nhưng làm trên CVAT chậm hoặc dễ sai |

**Trạng thái:** 🔴 Mở · 🗣️ Đang bàn · ↗️ Hỏi BTC · ✅ Đã chốt (trỏ sang QĐ) · 🛠️ Làm tool (trỏ sang `source-tool/`) · ⚪ Bỏ (ghi lý do)

---

## P-001

**Người ngồi sau xe máy: box riêng hay gộp chung với người lái**

- **Loại:** Guideline mơ hồ
- **Mục guideline:** §3.2 — "mỗi người một bounding box"
- **Người phát hiện:** @thanh-vien-b · 16/09/2026
- **Link CVAT:**
  - https://cvat.example.com/tasks/12/jobs/101?frame=37 — hai người, gần như chồng khít
  - https://cvat.example.com/tasks/12/jobs/101?frame=112 — người ngồi sau chỉ lộ đầu
- **Mô tả:** §3.2 nói mỗi người một box, nhưng hình minh hoạ trong guideline lại vẽ một box
  cho cả xe máy lẫn người trên xe.
- **Các cách hiểu:**
  1. Theo câu chữ: người ngồi sau có box `nguoi` riêng.
  2. Theo hình minh hoạ: không vẽ box `nguoi` cho ai đang ngồi trên xe.
- **Xử lý tạm trong lúc chờ:** vẽ box riêng và gắn tag `can_xem_lai` để dễ lọc ra sửa.
- **Kết quả:** ✅ [QĐ-001](so-quyet-dinh.md#qđ-001)

## P-002

**Xe bị che khuất hơn một nửa**

- **Loại:** Guideline chưa nói tới
- **Mục guideline:** §3.4 — chỉ nói về vật thể bị cắt ở mép ảnh, không nói về bị che
- **Người phát hiện:** @thanh-vien-c · 17/09/2026
- **Link CVAT:**
  - https://cvat.example.com/tasks/12/jobs/103?frame=8 — ô tô sau xe buýt, lộ khoảng 30%
  - https://cvat.example.com/tasks/12/jobs/103?frame=64 — xe máy sau cột điện, lộ khoảng 50%
- **Mô tả:** Không rõ có gán nhãn vật thể bị che không, và nếu có thì box ôm phần nhìn thấy
  hay ôm cả phần ước lượng bị che.
- **Các cách hiểu:**
  1. Bỏ qua khi lộ dưới 50%.
  2. Luôn gán, box chỉ ôm phần nhìn thấy.
  3. Luôn gán, box ôm cả phần ước lượng.
- **Xử lý tạm trong lúc chờ:** dừng job 103, chuyển sang job khác ít ca che khuất.
- **Kết quả:** ↗️ Đã hỏi BTC ngày 18/09/2026, chờ trả lời.

## P-003

**Phải vẽ lại box y hệt qua nhiều frame liên tiếp**

- **Loại:** Pain point công cụ
- **Mục guideline:** —
- **Người phát hiện:** @thanh-vien-d · 18/09/2026
- **Link CVAT:** https://cvat.example.com/tasks/12/jobs/105?frame=200 — frame 200–260, xe đỗ không di chuyển
- **Mô tả:** Ảnh chụp liên tiếp từ camera cố định. Xe đỗ bên đường xuất hiện y nguyên ở hàng chục
  frame, annotator phải vẽ lại ở từng frame. Ước tính chiếm ~40% thời gian job 105.
- **Hướng đang cân nhắc:**
  1. Dùng chế độ *Track* sẵn có của CVAT — cần thử xem có hợp với dữ liệu dạng ảnh rời không.
  2. Viết script đọc file export của CVAT, nhân box sang các frame kế tiếp, rồi import lại.
- **Kết quả:** 🗣️ Đang bàn. Nếu chọn hướng 2 thì đổi trạng thái sang 🛠️ và làm trong
  [`source-tool/`](source-tool/).

---

## P-004

**Pre-label dồn cục tại sống mũi khi mặt nghiêng che khuất**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Face Landmark VF50 §2.2
- **Người phát hiện:** @nnq2412 · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/341/jobs/2203 — Mặt nghiêng mạnh, mắt/lông mày phía xa bị che khuất nhưng pre-label dồn cục điểm tại sống mũi, annotator để nguyên và đánh Occluded
- **Mô tả:** Khi góc quay mặt nghiêng mạnh, một phần khuôn mặt (mắt hoặc lông mày phía xa) bị che khuất hoàn toàn, model pre-label tự động dồn tất cả các điểm thành một cụm tại vùng sống mũi. Annotator giữ nguyên vị trí sai đó và set trạng thái Occluded thay vì xử lý đúng.
- **Các cách hiểu:**
  1. Giữ nguyên cụm điểm lệch và set Occluded vì cho rằng pre-label đã đặt như vậy.
  2. Căn cứ quy tắc guideline: nếu số điểm nhìn thấy < 4/8 (với mắt) hoặc < 3/5 (với lông mày), bắt buộc phải đánh trạng thái `Outside` cho toàn bộ skeleton đó.
- **Xử lý tạm trong lúc chờ:** Reviewer raise issue, annotator chuyển trạng thái cụm điểm bị che sang `Outside`.
- **Kết quả:** ✅ Đã chốt — [QĐ-003](so-quyet-dinh.md#qđ-003)

## P-005

**Lỗi bắt chéo contour điểm bờ mí mắt và môi trong khi nhắm mắt / ngậm miệng**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Face Landmark VF50 §2.3
- **Người phát hiện:** @nnq2412 · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/340/jobs/2199 — Miệng đóng / nhắm mắt, các điểm mép trên bị kéo tụt xuống thấp hơn mép dưới làm contour bắt chéo hình chữ X
- **Mô tả:** Xảy ra ở các frame người lái xe ngậm miệng hoặc nhắm mắt. Do khoảng cách giữa 2 bờ mí/mép rất hẹp, annotator căn chỉnh làm điểm thuộc mép trên tụt xuống thấp hơn mép dưới (toạ độ y mép trên > toạ độ y mép dưới trên ảnh), làm đường contour nối bị vắt chéo thành chữ X.
- **Các cách hiểu:**
  1. Để điểm mép trên và mép dưới chéo nhau miễn là bám trong vùng môi/mắt.
  2. Điểm mép trên / mí trên bắt buộc phải nằm cao hơn hoặc bằng (trùng khít) điểm đối diện ở mép dưới / mí dưới, không bao giờ được bắt chéo contour.
- **Xử lý tạm trong lúc chờ:** Reviewer yêu cầu kéo lại toạ độ các điểm mép trên thẳng hàng hoặc trùng khít mép dưới.
- **Kết quả:** ✅ Đã chốt — [QĐ-004](so-quyet-dinh.md#qđ-004)

## P-006

**Điểm bờ trên lông mày đặt trên trán và điểm mắt lệch hoàn toàn khỏi bờ mi**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Face Landmark VF50 §2.1
- **Người phát hiện:** @nnq2412 · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/341/jobs/2204 — Dải 4 điểm bờ trên lông mày đặt quá cao lọt thỏm trên da trán
  - https://cvat.note.transformerlabs.ai/tasks/340/jobs/2200 — Cụm 8 điểm mắt lệch ra ngoài phần da trán hoặc má
- **Mô tả:** Model pre-label đặt lệch cụm điểm lông mày và mắt, annotator không kiểm tra kỹ mà giữ nguyên toạ độ sai, dẫn tới điểm bờ trên lông mày nằm lọt thỏm trên trán, còn điểm mắt nằm trên da má/trán.
- **Các cách hiểu:**
  1. Giữ nguyên vị trí do model đặt vì nghĩ rằng model đã ước lượng chuẩn.
  2. Cấm dựa dẫm pre-label; bắt buộc phải kéo điểm chạm đúng đường viền mép lông ngoài cùng bờ trên lông mày và bám sát bờ mi nhãn cầu thực tế.
- **Xử lý tạm trong lúc chờ:** Annotator rà soát lại toạ độ từng điểm, căn chỉnh chính xác theo đường viền giải phẫu thực tế.
- **Kết quả:** ✅ Đã chốt — [QĐ-005](so-quyet-dinh.md#qđ-005)

## P-007

**Sai cấu trúc ID mí mắt và khoảng cách 3 đoạn sống mũi không đều**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Face Landmark VF50 §2.1, §2.4
- **Người phát hiện:** @nnq2412 · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/340/jobs/2201 — Kéo nhầm điểm contour làm mí trên có 2 điểm, mí dưới có 4 điểm, sai lệch ID khoé mắt 18/26
  - https://cvat.note.transformerlabs.ai/tasks/341/jobs/2205 — Khoảng cách 3 đoạn sống mũi không đều, đoạn dưới 12-13 bị co ngắn hẳn
- **Mô tả:** Annotator kéo nhầm thứ tự điểm contour mắt làm biến dạng cấu trúc ID (mí trên 2 điểm, mí dưới 4 điểm); đồng thời ở sống mũi chia 3 đoạn không đều, làm điểm 13 bị kéo sai lệch khỏi chân sống mũi.
- **Các cách hiểu:**
  1. Đặt điểm sống mũi tùy biến theo cảm tính; số lượng điểm mắt miễn đủ 8 điểm vòng quanh mắt.
  2. Cấu trúc mắt bắt buộc chia đúng chuẩn: 2 điểm khoé, 3 điểm mí trên, 3 điểm mí dưới; 3 đoạn sống mũi phải chia đều với tỉ lệ sai lệch max/min $\le 1.01$, điểm 13 đặt tại chân sống mũi.
- **Xử lý tạm trong lúc chờ:** Trả job yêu cầu annotator sắp xếp lại đúng ID cấu trúc mắt và chia đều khoảng cách sống mũi.
- **Kết quả:** ✅ Đã chốt — [QĐ-006](so-quyet-dinh.md#qđ-006)

## P-008

**Định vị điểm giải phẫu mắt nhắm, lỗ tai, chóp mũi trong Human Pose**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Human Pose 17 keypoints §2
- **Người phát hiện:** @spameverytime · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/339/jobs/2197?frame=1 — Độ chính xác của keypoint mắt chưa chuẩn tâm mắt/đồng tử
  - https://cvat.note.transformerlabs.ai/tasks/339/jobs/2197?frame=2 — Lệch point so với vị trí lỗ/ống tai
  - https://cvat.note.transformerlabs.ai/tasks/339/jobs/2197?frame=3 — Tài xế nhắm mắt, điểm mắt bị đặt lệch lên trên/xuống dưới
  - https://cvat.note.transformerlabs.ai/tasks/339/jobs/2197?frame=4 — Điểm mũi bị đặt ra ngoài vùng mũi hoặc lệch đỉnh chóp mũi
- **Mô tả:** Khi gán nhãn Human Pose vùng đầu mặt, annotator gặp khó khăn trong việc định vị chuẩn xác điểm mắt khi tài xế nhắm mắt (Frame 3), điểm tai bị đặt lệch ra vành tai ngoài thay vì lỗ tai (Frame 2), và điểm mũi bị đặt lệch ra ngoài thay vì đỉnh chóp mũi (Frame 4).
- **Các cách hiểu:**
  1. Đặt điểm tự do gần vùng mắt/tai/mũi.
  2. Thống nhất chuẩn giải phẫu: Khi nhắm mắt đặt chính giữa khe mí mắt; điểm tai đặt chính xác tại lỗ tai/ống tai; điểm mũi đặt tại đỉnh chóp mũi; điểm mắt mở đặt tại tâm đồng tử.
- **Xử lý tạm trong lúc chờ:** Reviewer gửi feedback chi tiết từng frame để annotator căn chỉnh lại toạ độ.
- **Kết quả:** ✅ Đã chốt — [QĐ-007](so-quyet-dinh.md#qđ-007)

## P-009

**Quên gán thuộc tính occluded cho khớp bị che khuất tương hỗ**

- **Loại:** Guideline đã nói nhưng cần áp dụng
- **Mục guideline:** Human Pose 17 keypoints §3
- **Người phát hiện:** @spameverytime, Trương Trọng Đức · 27/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/339/jobs/2197?frame=5 — Khớp háng bị cổ tay che khuất, annotator quên set thuộc tính visible/occluded
- **Mô tả:** Trong tư thế ngồi lái xe, các bộ phận cơ thể thường xuyên che khuất lẫn nhau (cổ tay che khớp háng, cánh tay che ngực/bụng). Annotator vẫn định vị điểm nhưng quên thiết lập thuộc tính `occluded` mà để mặc định là `visible`.
- **Các cách hiểu:**
  1. Nếu ước lượng được vị trí thì cứ để mặc định visible.
  2. Điểm không nhìn thấy trực tiếp do bị bộ phận khác che khuất bắt buộc phải đánh dấu thuộc tính `occluded`.
- **Xử lý tạm trong lúc chờ:** Annotator rà soát lại toàn bộ 10 frames của job và set lại thuộc tính `occluded` cho các điểm bị che.
- **Kết quả:** ✅ Đã chốt — [QĐ-008](so-quyet-dinh.md#qđ-008)

## P-010

**Khó khăn khi kẻ vẽ các đoạn thẳng trực giao (đường làn, vạch phân cách, mép đường, ranh giới thẳng) trên CVAT/trình duyệt do run tay hoặc thiếu tính năng khóa trục**

- **Loại:** Pain point công cụ
- **Mục guideline:** BBox & Polyline §3 (Lane markings, Curbs), Segmentation §3
- **Người phát hiện:** @spameverytime · 30/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/341/jobs/2205 — Các ca vẽ polyline cho vạch kẻ đường `lane/single white` và mép vỉa hè `lane/road curb` thường xuyên bị rung răng cưa, tốn nhiều thời gian nắn toạ độ
- **Mô tả:** Trình duyệt và CVAT mặc định bắt toạ độ chuột 2D tự do. Khi annotator cần vẽ các đường thẳng dài theo phương ngang hoặc dọc (vạch dừng xe, vạch kẻ đường, cạnh chân tường, chân bounding box), bàn tay luôn có dao động vi mô làm đường vẽ bị lệch góc $1.5^\circ - 4.5^\circ$. Annotator phải nắn nót hoặc Undo nhiều lần.
- **Hướng đang cân nhắc:**
  1. Yêu cầu annotator zoom lớn rồi nhấp từng điểm nhỏ (rất tốn thời gian, mỏi tay).
  2. Xây dựng ứng dụng độc lập trên Ubuntu Linux (Mouse Helper Desktop App) can thiệp máy chủ X11 để khoá cứng trục di chuyển chuột vật lý khi người dùng giữ phím `Shift`.
- **Xử lý tạm trong lúc chờ:** Kéo zoom mức 300% để giảm thiểu sai số rung tay khi vẽ.
- **Kết quả:** 🛠️ Làm tool — [mouse-helper-app](source-tool/mouse-helper-app/README.md)

---

## Mẫu để copy

```markdown
## P-NNN

**Tóm tắt một dòng**

- **Loại:** Guideline chưa nói tới | Guideline mơ hồ | Guideline mâu thuẫn | Pain point công cụ
- **Mục guideline:** §
- **Người phát hiện:** @ · dd/mm/yyyy
- **Link CVAT:** (bỏ trống nếu không có)
  - https://…/tasks/<id>/jobs/<id>?frame=<n> — frame này có gì
- **Mô tả:**
- **Các cách hiểu:** (với pain point công cụ thì ghi **Hướng đang cân nhắc:**)
  1.
  2.
- **Xử lý tạm trong lúc chờ:**
- **Kết quả:** 🔴 Mở
```

Nhớ thêm một dòng vào bảng **Danh sách** ở đầu file.
