from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
DEFAULT_PROMPT = ARTIFACTS_DIR / "system_prompt.md"
DEFAULT_TOOLS = ARTIFACTS_DIR / "tools.yaml"

load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered",
)


@st.cache_resource
def load_runtime(provider_name: str, model: str | None, version: str) -> dict[str, Any]:
    system_prompt = DEFAULT_PROMPT.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(DEFAULT_TOOLS)
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", None)
    artifact = build_artifact_version(version, DEFAULT_PROMPT, DEFAULT_TOOLS)
    return {
        "system_prompt": system_prompt,
        "openai_tools": openai_tools,
        "provider": provider,
        "model": selected_model,
        "artifact_version": artifact.artifact_version,
        "tool_names": [t.get("function", {}).get("name") or t.get("name") for t in openai_tools],
    }


def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []  # display: {role, content, tools?}
    if "history" not in st.session_state:
        st.session_state.history = []  # provider context pairs


def render_tool_event(event: dict[str, Any]) -> None:
    """Pretty-print special local tools; fall back to raw dump."""
    tool_name = event.get("tool") or (event.get("result") or {}).get("tool")
    result = event.get("result") if isinstance(event.get("result"), dict) else {}
    args = event.get("args")

    st.markdown(f"**`{tool_name or 'tool'}`**")
    if args:
        st.caption(f"args: `{args}`")

    if tool_name == "rank_sources" and "items" in result and "error" not in result:
        rows = [
            {
                "score": item.get("score"),
                "title": item.get("title") or item.get("url") or "",
                "matched_terms": ", ".join(item.get("matched_terms") or []),
                "source": item.get("source") or "",
            }
            for item in result.get("items") or []
        ]
        st.caption(f"query: `{result.get('query', '')}` · kept {result.get('item_count', 0)}")
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("Không còn item sau khi xếp hạng.")
        return

    if tool_name == "cite" and "citations" in result and "error" not in result:
        st.caption(f"style: `{result.get('style', '')}` · {result.get('item_count', 0)} item(s)")
        citations = result.get("citations") or ""
        if citations:
            st.code(citations, language="text")
        else:
            st.info("Danh sách citation trống.")
        return

    st.code(f"{tool_name}({args})\n→ {event.get('result')}", language="text")


def render_sidebar() -> dict[str, Any]:
    st.sidebar.header("Cấu hình")
    provider = st.sidebar.selectbox(
        "Provider",
        ["openrouter", "openai", "anthropic", "gemini", "ollama"],
        index=0,
    )
    version = st.sidebar.text_input("Artifact version", value="v0")
    model = st.sidebar.text_input("Model (để trống = mặc định provider)", value="")
    history_window = st.sidebar.slider("History window (cặp user/assistant)", 1, 10, 5)
    max_tool_rounds = st.sidebar.slider("Max tool rounds", 1, 8, 4)

    if st.sidebar.button("Xóa hội thoại", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    return {
        "provider": provider,
        "version": version.strip() or "v0",
        "model": model.strip() or None,
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
    }


def main() -> None:
    init_session()
    cfg = render_sidebar()

    st.title("Research Agent")
    st.caption("UI Streamlit — gọi trực tiếp agent + tool trong cùng process Python (không REST).")

    try:
        runtime = load_runtime(cfg["provider"], cfg["model"], cfg["version"])
    except Exception as exc:
        st.error(f"Không khởi tạo được provider/tools: {type(exc).__name__}: {exc}")
        st.info("Kiểm tra `starter_v0/.env` và chạy lại `python scripts/preflight_provider.py --provider openrouter`.")
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Artifact:** `{runtime['artifact_version']}`")
    st.sidebar.markdown(f"**Model:** `{runtime['model']}`")
    with st.sidebar.expander("Tools đang load"):
        for name in runtime["tool_names"]:
            st.write(f"- `{name}`")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            tools = msg.get("tools") or []
            if tools:
                with st.expander(f"Tool calls ({len(tools)})"):
                    for event in tools:
                        render_tool_event(event)

    prompt = st.chat_input("Nhập yêu cầu research…")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
        {"role": "system", "content": runtime["system_prompt"]},
        *trim_history(st.session_state.history, cfg["history_window"]),
        {"role": "user", "content": prompt},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy nghĩ / gọi tool…"):
            try:
                result = run_model_tool_loop(
                    provider=runtime["provider"],
                    messages=messages,
                    tools=runtime["openai_tools"],
                    model=cfg["model"],
                    max_tool_rounds=cfg["max_tool_rounds"],
                )
                assistant_text = result.get("assistant_text") or "(không có nội dung)"
                tool_events = result.get("tool_events") or []
                status = result.get("status")
            except Exception as exc:
                assistant_text = f"Lỗi provider: {type(exc).__name__}: {exc}"
                tool_events = []
                status = "provider_error"

        st.markdown(assistant_text)
        if status and status != "answered":
            st.caption(f"status: `{status}`")
        if tool_events:
            with st.expander(f"Tool calls ({len(tool_events)})"):
                for event in tool_events:
                    render_tool_event(event)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text, "tools": tool_events}
    )
    if status != "provider_error":
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    main()
