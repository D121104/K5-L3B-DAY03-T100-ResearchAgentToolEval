# Team

## Thông tin nhóm

- Tên nhóm: T100
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-T100-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: [repo](https://github.com/D121104/K5-L3B-DAY03-T100-ResearchAgentToolEval) · nhánh `main` · commit [`22da5fd`](https://github.com/D121104/K5-L3B-DAY03-T100-ResearchAgentToolEval/commit/22da5fd) (cập nhật lại hash khi chốt nộp)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Minh Nhân | 2A202603723 | nhannguyenit04@gmail.com | uscalurn | Tools |
|   2 | Đào Đức Duy | 2A202603900 | 26ai.duydd4@vinuni.edu.vn | D121104 | Prompts |
|   3 | Trần Cảnh Hưng | 2A202603759 | 26ai.hungtc@vinuni.edu.vn | danialtranz | Report, UI, Eval |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## NguyenMinhNhan-2A202603723

### Phần việc phụ trách

- Tool mới và unit test tool

### Đóng góp cụ thể

- Viết `compare_sources` (`tools/compare_sources/`), đăng ký vào `tools/__init__.py` và `artifacts/tools.yaml`
- Viết ≥ 4 unit test cho tool mới trong `tests/test_tools_todo.py`
- Tham gia mở rộng test suite (test challenge)

### Bằng chứng

- `starter_v0/tools/compare_sources/`
- `starter_v0/tests/test_tools_todo.py` (các test `compare_sources_*`)
- `pytest` 93 passed, 0 skipped

## DaoDucDuy-2A202603900

### Phần việc phụ trách

- System prompt và vòng tối ưu prompt

### Đóng góp cụ thể

- Sửa `artifacts/system_prompt.md` qua các version: bỏ ép tool / tự đoán, thêm scope research, clarify khi thiếu info, sequence xác nhận trước `send`, rule bỏ nguồn cũ, routing `compare_sources`
- Ghi giả thuyết và metric vào `artifacts/version_log.csv`

### Bằng chứng

- `starter_v0/artifacts/system_prompt.md`
- `starter_v0/artifacts/version_log.csv` (v1–v9)
- Run base v8/v9 đạt 20/20: `runs/v8_B_base_*.json`, `runs/v9_B_base_*.json`

## TranCanhHung-2A202603759

### Phần việc phụ trách

- Eval nhóm, UI, báo cáo

### Đóng góp cụ thể

- Viết 10 case `data/eval_group.json` (5 single + 5 multi), chạy suite group
- UI Streamlit (`app.py`) + link dùng thử ngrok
- Báo cáo nhóm `report/team/group_report.md` và transcript live

### Bằng chứng

- `starter_v0/data/eval_group.json`
- `starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json` (10/10)
- UI: `https://1f0a-14-247-60-241.ngrok-free.app`
- Transcript: `starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json`
