# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **T100**
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  - Đào Đức Duy — prompts / tối ưu [`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md)
  - Nguyễn Minh Nhân — tools / unit test ([`compare_sources`](../../starter_v0/tools/compare_sources/tool.py))
  - Trần Cảnh Hưng — eval nhóm, UI, báo cáo
- Provider/model dùng cho v0–v9: `openrouter` / `openai/gpt-4o-mini`
- Repo / nhánh / commit chốt: [K5-L3B-DAY03-T100-ResearchAgentToolEval](https://github.com/D121104/K5-L3B-DAY03-T100-ResearchAgentToolEval) · `main` · [`6e50b55`](https://github.com/D121104/K5-L3B-DAY03-T100-ResearchAgentToolEval/commit/6e50b55)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin web / tweet theo tài khoản hoặc chủ đề, đọc URL hoặc paper arXiv, đối chiếu số liệu giữa nhiều nguồn bằng `compare_sources`, hỏi lại khi thiếu thông tin, và chỉ gửi Telegram sau khi user xác nhận.

**Cách chạy UI:**

```text
cd starter_v0
streamlit run app.py
```

Dependency UI: `streamlit>=1.32.0` trong [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt).

**Link dùng thử (deploy):**

> URL: https://1f0a-14-247-60-241.ngrok-free.app

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thiếu thông tin hoặc cần xác nhận gửi/đăng | không |
| timeline | Lấy tweet gần đây của một tài khoản X đã biết | không |
| social_search | Tìm tweet theo từ khóa (Latest/Top) | không |
| lookup | Tìm thông tin / tin tức trên web | không |
| fetch | Đọc nội dung một URL cụ thể | không |
| format | Ghép items đã có thành digest theo template | không |
| send | Gửi nội dung lên Telegram khi `confirmed=true` | không |
| policy | Tra cứu chính sách nội bộ | không |
| papers | Tìm paper trên arXiv theo từ khóa | không |
| paper_text | Đọc nội dung paper arXiv theo ID/URL | không |
| [compare_sources](../../starter_v0/tools/compare_sources/tool.py) | Đối chiếu facts có cấu trúc giữa ≥2 nguồn (consistent / different / missing) | **có** |

### A3. Câu hỏi mẫu để thử

1. `Nghe nói Apple mới ra chip mới đó. Tìm hiểu thử xem nào` (lookup tin tức)
2. `So sánh hai nguồn: Reuters revenue=10B users=100M; Bloomberg revenue=12B users=100M` (route `compare_sources`)
3. `Gửi bản tin này lên Telegram giúp mình` (phải `clarify` yes/no, không gửi ngay)
4. `Tìm paper khoa học về retrieval-augmented generation trên arXiv`
5. `Đọc bài này giúp mình` — khi chưa có URL, agent phải hỏi lại URL

## 3. Giải pháp

Nhóm tối ưu theo vòng giả thuyết → sửa một artifact → đo lại base eval, ghi trong [`artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv).

- **Prompt ([`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md)):** bỏ ép gọi tool và tự đoán; giới hạn scope research (toán/code → không gọi tool); bắt buộc `clarify` khi thiếu handle/URL; sequence xác nhận trước `send`; rule bỏ nguồn cũ khi user chuyển nguồn; thêm routing cho `compare_sources`.
- **Tool declaration ([`tools.yaml`](../../starter_v0/artifacts/tools.yaml)):** viết lại description khi nào dùng/không dùng; convention args (`topic=news`, `timeframe`, `search_type`, handle không `@`); boundary `send` chỉ khi `confirmed=true`.
- **Tool mới [`compare_sources`](../../starter_v0/tools/compare_sources/tool.py):** nhận ≥2 nguồn `{title, facts}`, trả `comparisons` + `summary`; không search web, không phán nguồn nào đúng. Kèm unit test và case group để đo routing.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ [`version_log.csv`](../../starter_v0/artifacts/version_log.csv) và các run JSON. Các run dưới đây có `provider_error_cases == 0`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Prompt ép tool + tự đoán → out_of_scope / missing_info / wrong_boundary | — | 0.70 | [v0_B_base_...172803....json](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) |
| v1 | system_prompt.md | Làm rõ khi không dùng tool → giảm gọi tool ngoài phạm vi | 0.70 | 0.80 | [v1_B_base_...174649....json](../../starter_v0/runs/v1_B_base_openrouter_20261110T174649674549.json) |
| v2 | system_prompt.md | Clarify khi thiếu info + xác nhận trước gửi → giảm missing_info / gửi sớm | 0.80 | 0.90 | [v2_B_base_...175319....json](../../starter_v0/runs/v2_B_base_openrouter_20261110T175319315379.json) |
| v3 | system_prompt.md; tools.yaml | Quy ước args rõ (response_type, topic/timeframe) → giảm sai args | 0.90 | 0.95 | [v3_B_base_...175935....json](../../starter_v0/runs/v3_B_base_openrouter_20261110T175935818586.json) |
| v4 | tools.yaml | Mô tả khi nào dùng/không dùng từng tool | 0.95 | 0.95 | [v4_B_base_...182619....json](../../starter_v0/runs/v4_B_base_openrouter_20261110T182619927517.json) |
| v5 | tools.yaml | Làm rõ args timeline / social_search / papers / paper_text | 0.95 | 0.95 | [v5_B_base_...183357....json](../../starter_v0/runs/v5_B_base_openrouter_20261110T183357288132.json) |
| v6 | tools.yaml | Side-effect + `confirmed=true` của send | 0.95 | 0.95 | [v6_B_base_...183812....json](../../starter_v0/runs/v6_B_base_openrouter_20261110T183812368825.json) |
| v7 | system_prompt.md; tools.yaml | Ưu tiên xác nhận ý định đăng (yes_no) trước hỏi nội dung | 0.95 | 0.95 | [v7_B_base_...190454....json](../../starter_v0/runs/v7_B_base_openrouter_20261110T190454683576.json) |
| v8 | system_prompt.md; tools.yaml | Cấm gọi tool nguồn đã bỏ → hết extra_tool_call | 0.95 | **1.0** | [v8_B_base_...191758....json](../../starter_v0/runs/v8_B_base_openrouter_20261110T191758325842.json) |
| v9 | system_prompt.md; tools.yaml | Thêm `compare_sources` + rule routing; base giữ 20/20 | 1.0 | **1.0** | [v9_B_base_...192431....json](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) |

Group eval (10/10): [v8_B_group_...192326....json](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json).

### B2. Failure Analysis

Lấy từ `results[*].result` trong run v0 (14/20 pass). Cột Evidence trỏ case trong run JSON; cột Fix Evidence trỏ run sau khi hết lỗi tương ứng.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix | Evidence (fail) | Fix Evidence |
|---|---|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send` (trả lời toán bằng send) | Gọi tool cho bài toán ngoài scope | v1: scope research + không dùng send để trả lời chat | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R08_out_of_scope`) | [v1 run](../../starter_v0/runs/v1_B_base_openrouter_20261110T174649674549.json) |
| R14_out_of_scope_coding | out_of_scope | `send` (đẩy code qua send) | Gọi tool cho yêu cầu viết code | Cùng rule scope ở v1 | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R14_out_of_scope_coding`) | [v1 run](../../starter_v0/runs/v1_B_base_openrouter_20261110T174649674549.json) |
| R10_missing_handle | missing_info | `timeline(screenname=sama)` | Đoán handle thay vì hỏi | v2: bắt buộc clarify khi chưa biết account | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R10_missing_handle`) | [v2 run](../../starter_v0/runs/v2_B_base_openrouter_20261110T175319315379.json) |
| R11_missing_url | missing_info | `fetch(url=example.com)` | Đoán URL | v2: clarify khi chưa có URL | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R11_missing_url`) | [v2 run](../../starter_v0/runs/v2_B_base_openrouter_20261110T175319315379.json) |
| R12_confirm_before_send | wrong_boundary | `send` ngay | Gửi chưa xác nhận | v2→v7: sequence clarify yes_no trước send | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R12_confirm_before_send`) | [v8 run](../../starter_v0/runs/v8_B_base_openrouter_20261110T191758325842.json) (20/20) |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg | `lookup(query="AI news")` thiếu `topic=news` | Sai convention args tin tức | v3+: mô tả `topic`/`timeframe` trong tools.yaml | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json) (`id=R13_parallel_web_and_tweets`) | [v3 run](../../starter_v0/runs/v3_B_base_openrouter_20261110T175935818586.json) |

Lỗi còn kéo dài đến v7 chủ yếu quanh boundary confirm-send / extra_tool_call khi đổi nguồn; v8 xử lý xong (20/20).

### B3. Team Eval Cases

Định nghĩa case: [`eval_group.json`](../../starter_v0/data/eval_group.json). Kết quả đo: [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) (10/10).

| Case ID | What It Tests | Expected Tool/Behavior | Result | Evidence File |
|---|---|---|---|---|
| G01_compare_sources_routing | Facts sẵn từ ≥2 nguồn → compare_sources | `compare_sources` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G02_compare_missing_sources | Muốn so sánh nhưng thiếu nguồn | `clarify` (text) | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G03_policy_not_web | Hỏi quy định nội bộ | `policy` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G04_papers_not_web | Tìm paper học thuật | `papers` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G05_confirm_before_send | Gửi lần đầu phải hỏi xác nhận | `clarify` (yes_no), không `send` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G06_compare_after_facts_filled | Multi-turn: đủ facts rồi mới compare | `compare_sources` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G07_carryover_news_topic | Giữ topic=news + timeframe=day khi đổi query | `lookup(query=Claude, topic=news, timeframe=day)` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G08_correction_search_type | Sửa Latest→Top, giữ query | `social_search(search_type=Top)` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G09_paper_text_after_id | Có arXiv ID rồi mới đọc | `paper_text(arxiv_url=1706.03762)` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |
| G10_switch_to_compare_sources | Bỏ web search, chuyển sang compare | `compare_sources` | PASS | [eval_group.json](../../starter_v0/data/eval_group.json) + [v8 group run](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json) |

### B4. Live Chat Evidence

Transcript: [`v9_openrouter_20261110T221843414946.transcript.json`](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json)  
Artifact khớp base v9: [`v9_B_base_...192431....json`](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) (`v9+p06f776a04369+t030a91b8af6f`) · provider `openrouter` · model `openai/gpt-4o-mini`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | `hi` | (không gọi tool) | [transcript](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json) → `turns[0]` · [v9 run](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) | Chào lại bình thường, không ép tool |
| 2 | Tìm hiểu chip mới của Apple | `lookup(query="Apple new chip", topic=news, timeframe=day)` | [transcript](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json) → `turns[1]` · [v9 run](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) | Trả link + tóm tắt tin |
| 3 | Elon Musk / xe bay? | `lookup(query="Elon Musk flying car", topic=news, timeframe=day)` | [transcript](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json) → `turns[2]` · [v9 run](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) | Trả tin liên quan Roadster / flying car |
| 4 | Chat xã giao | (không gọi tool) | [transcript](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json) → `turns[3]` · [v9 run](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json) | Trả lời trực tiếp |

Ghi chú: transcript này cover yêu cầu research thường + không ép tool khi chat thường. Scenario thiếu thông tin / xác nhận trước gửi đã đo trong eval group (G02, G05) và rule trong prompt; nên bổ sung thêm 1–2 lượt live kiểu đó nếu muốn B4 đủ cả 3 scenario trên cùng một transcript.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới `compare_sources` | [`tool.py`](../../starter_v0/tools/compare_sources/tool.py), [`TOOL.md`](../../starter_v0/tools/compare_sources/TOOL.md); đăng ký [`__init__.py`](../../starter_v0/tools/__init__.py) + [`tools.yaml`](../../starter_v0/artifacts/tools.yaml) | Đối chiếu facts → consistent/different/missing; group G01/G06/G10 route đúng | Chỉ dùng khi đã có ≥2 nguồn có facts; thiếu thì clarify, không đoán |
| Unit test tool mới (≥ 3) | [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) — 4 test `compare_sources_*`; `pytest` **93 passed, 0 skipped** | Bắt input xấu (`None`, 1 nguồn, `facts` sai kiểu, thiếu title) bằng error dict | Unit test đo code tool; eval đo lựa chọn của model — tách hai lớp lỗi |
| UI | [`app.py`](../../starter_v0/app.py); lệnh `streamlit run app.py`; link https://1f0a-14-247-60-241.ngrok-free.app | Team khác mở thử được; transcript live từ chat CLI cùng artifact v9 | Ngrok URL có thể hết hạn; cần chạy lại tunnel khi demo |

Tool unit tests: **4 test** cho `compare_sources`. Ví dụ lỗi unit test bắt được nhưng eval không bắt: `facts` truyền string thay vì object → `TypeError` / error dict — eval chỉ kiểm tra model có gọi đúng tool, không kiểm tra code tool xử lý input hỏng thế nào.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | — | Chưa làm | — |
| Hơn 3 tool mới (≥ 4) | — | Chỉ 1 tool mới bắt buộc (`compare_sources`); `rank_sources`/`cite` giữ code nhưng không đăng ký cho model | Tránh phình tool list làm nhiễu routing |
| `send` gửi thật lên Telegram sau xác nhận | Unit test trong [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py); code [`tools/send/tool.py`](../../starter_v0/tools/send/tool.py) | Flow `confirmed=true` + env token/chat id → gọi Telegram API | **Transcript live gửi Telegram thật chưa có trong [`transcripts/`](../../starter_v0/transcripts/)** — cần thêm 1 session chat có clarify → confirm → send nếu muốn bằng chứng bonus đầy đủ |
| Test challenge (0 skipped) | `pytest tests/ -q` → **93 passed, 0 skipped** · [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) | Unskip / viết đủ test cho tool có sẵn + tool mới | Giữ mock HTTP để không phụ thuộc mạng khi CI/local |

Test challenge: suite không còn skip; các test regression cho tool sẵn (send env thiếu, fetch truncate, policy untrusted text, papers HTTP lỗi, …) nằm trong [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py).

### B7. Small Local Model Challenge (bonus)

Không làm trong lab này.

## 5. Khó khăn và cách xử lý

1. **Tool list càng dài, context chọn tool càng nhiễu.** Khi thêm tool / mô tả dài, model dễ gọi thừa hoặc gọi tool nguồn đã bỏ. Nhóm xử lý bằng description “khi nào dùng / không dùng”, rule prompt bỏ nguồn cũ (v8), và không đăng ký tool phụ (`rank_sources`, `cite`) vào `TOOL_FUNCTIONS`/`tools.yaml` để model không thấy.
2. **Model tự ý thi hành thay vì tuân thủ boundary.** Baseline hay `send` luôn hoặc đoán handle/URL. Fix bằng sequence xác nhận cứng trong prompt + `confirmed=true` trong declaration, rồi đo lại từng version; case còn sót được bắt bằng eval group (G05) và base multiturn.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân:

- [2A202603900_DaoDucDuy.md](./2A202603900_DaoDucDuy.md) — prompt / versioning giả thuyết
- [2A202603723_NguyenMinhNhan.md](./2A202603723_NguyenMinhNhan.md) — `compare_sources` + unit test / test challenge
- [2A202603759_TranCanhHung.md](./2A202603759_TranCanhHung.md) — eval group 10 case, UI + ngrok, report + transcript

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc [`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md):** scope research, cấm đoán handle/URL, sequence confirm trước send, bỏ tool nguồn đã abandon, routing `compare_sources`.
- **Fix thuộc [`tools.yaml`](../../starter_v0/artifacts/tools.yaml):** description khi dùng/không dùng, convention args (`topic`, `timeframe`, `search_type`), boundary `send`/`confirmed`.
- **Failure cần review thủ công:** câu trả lời “nghe hay” nhưng nguồn yếu; parallel tool đúng intent nhưng args lệch nhẹ; hành vi live chat ngoài eval schema.
- **Nếu thêm một vòng:** bổ sung transcript live đủ 3 scenario (lookup thường / thiếu info → clarify / confirm → send Telegram thật), và thử rút gọn tool descriptions để giảm nhiễu khi list tool lớn.

## 8. Tài liệu tham khảo

- [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md), [SUBMISSION.md](../../SUBMISSION.md)
- [`version_log.csv`](../../starter_v0/artifacts/version_log.csv), [`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md), [`tools.yaml`](../../starter_v0/artifacts/tools.yaml)
- Run ví dụ: [v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T172803513266.json), [v9](../../starter_v0/runs/v9_B_base_openrouter_20261110T192431461621.json), [group](../../starter_v0/runs/v8_B_group_openrouter_20261110T192326583151.json)
- Transcript: [`v9_openrouter_...221843....transcript.json`](../../starter_v0/transcripts/v9_openrouter_20261110T221843414946.transcript.json)
- Commit chốt: [`6e50b55`](https://github.com/D121104/K5-L3B-DAY03-T100-ResearchAgentToolEval/commit/6e50b55)
