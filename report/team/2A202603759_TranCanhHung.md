# Báo cáo cá nhân — TranCanhHung-2A202603759

Đổi tên file theo quy tắc `MSSV_HoTen.md` → nên đổi thành `2A202603759_TranCanhHung.md` trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: Trần Cảnh Hưng
- MSSV: 2A202603759
- Email: 26ai.hungtc@vinuni.edu.vn
- GitHub: danialtranz

## 2. Phần việc phụ trách

- UI Streamlit và link dùng thử
- Eval nhóm (`eval_group.json`, chạy suite group)
- Báo cáo nhóm / hoàn thiện deliverable CP4–CP5
- Phát triển trên các nhánh `feat/ui` và `trancanhh`

## 3. Đóng góp cụ thể

- Xây trang chat Streamlit (`starter_v0/app.py`), thêm dependency UI vào `requirements.txt` trên nhánh `feat/ui`.
- Tiếp tục hoàn thiện trên nhánh `trancanhh` (eval, tool/test, versioning, CP4–CP5).
- Viết và chạy bộ eval nhóm 10 case (5 single + 5 multi) trong `data/eval_group.json`; có run group 10/10.
- Tham gia vòng sau: `compare_sources`, unit test, version log v8–v9; tổng hợp bằng chứng cho `group_report.md` và transcript live.
- Các commit dưới author `danialtranz` trên hai nhánh trên phản ánh phần việc này.

## 4. Bằng chứng

- File/commit/PR:
  - Nhánh: `feat/ui` (PR #4 merge vào `main`), `trancanhh` (PR #3)
  - `70a6bdd` — Design Chat Page for user (`app.py`, `requirements.txt`)
  - `e87411b` — update v0
  - `6c0c1f2` — complete c3/c4 (run base v8, version log)
  - `18948ee` — complete cp4/cp5 (`eval_group.json`, run group, `compare_sources`, tests, v9)
  - UI: https://1f0a-14-247-60-241.ngrok-free.app
  - Transcript: `starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json`
  - Group run: `starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng AI hỗ trợ soạn UI/eval/report; tự kiểm bằng cách chạy UI thật, `run_eval.py --suite group`, đọc run JSON (`passed_cases`, `provider_error_cases`), và đối chiếu transcript trước khi ghi vào báo cáo.

## 5. Tự đánh giá

Phần UI và eval nhóm mình hoàn thành đúng phạm vi phụ trách, có bằng chứng chạy được trên `feat/ui` và `trancanhh`. Vẫn còn điểm cần cải thiện: transcript live chưa cover đủ scenario thiếu thông tin / xác nhận trước khi gửi Telegram, nên bằng chứng demo chưa đầy như kỳ vọng. Nhìn chung đóng góp ổn định trong nhóm, còn chỗ để làm kỹ hơn ở khâu evidence live.
