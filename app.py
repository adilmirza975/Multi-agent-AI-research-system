"""
Streamlit UI for the multi-agent research pipeline.

Drop this file in the same folder as agents.py / tools.py / pipeline.py
and run:

    streamlit run app.py

It reuses the exact same agents/chains as pipeline.py (build_search_agent,
build_reader_agent, writer_chain, critic_chain), but calls them step-by-step
so progress can be shown live in the browser instead of only in the terminal.
"""

import streamlit as st
from datetime import datetime

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

if "state" not in st.session_state:
    st.session_state.state = {}
if "running" not in st.session_state:
    st.session_state.running = False


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🔎 About this pipeline")
    st.markdown(
        """
This app runs a **4-agent research pipeline**:

1. **Search Agent** — finds recent, reliable sources
2. **Reader Agent** — scrapes the most relevant source
3. **Writer Chain** — drafts a full report
4. **Critic Chain** — reviews the report and gives feedback
        """
    )
    st.divider()
    if st.session_state.state.get("report"):
        st.success("Last run completed ✅")
    st.caption(f"Session time: {datetime.now().strftime('%H:%M:%S')}")


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("🔎 Multi-Agent Research System")
st.caption("Search → Read → Write → Critique, powered by your agent pipeline.")

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of quantum computing on cryptography",
    disabled=st.session_state.running,
)

run_clicked = st.button(
    "🚀 Run Research",
    type="primary",
    disabled=st.session_state.running or not topic.strip(),
)


# ----------------------------------------------------------------------------
# Pipeline execution (mirrors pipeline.py, step by step, with live UI updates)
# ----------------------------------------------------------------------------
def run_pipeline_ui(topic: str):
    state = {}

    # ---- Step 1: Search agent -------------------------------------------------
    with st.status("Step 1/4 — Search agent finding sources...", expanded=True) as status:
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["search_results"] = search_result["messages"][-1].content
        status.update(label="Step 1/4 — Search complete ✅", state="complete", expanded=False)

    with st.expander("📄 Search Results", expanded=False):
        st.markdown(state["search_results"])

    # ---- Step 2: Reader agent --------------------------------------------------
    with st.status("Step 2/4 — Reader agent scraping top resource...", expanded=True) as status:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        status.update(label="Step 2/4 — Scraping complete ✅", state="complete", expanded=False)

    with st.expander("📰 Scraped Content", expanded=False):
        st.markdown(state["scraped_content"])

    # ---- Step 3: Writer chain ---------------------------------------------------
    with st.status("Step 3/4 — Writer drafting the report...", expanded=True) as status:
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        status.update(label="Step 3/4 — Draft complete ✅", state="complete", expanded=False)

    # ---- Step 4: Critic chain ----------------------------------------------------
    with st.status("Step 4/4 — Critic reviewing the report...", expanded=True) as status:
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        status.update(label="Step 4/4 — Review complete ✅", state="complete", expanded=False)

    return state


if run_clicked:
    st.session_state.running = True
    try:
        st.session_state.state = run_pipeline_ui(topic)
    except Exception as e:
        st.error(f"Pipeline failed: {e}")
    finally:
        st.session_state.running = False
    st.rerun()


# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
state = st.session_state.state

if state.get("report"):
    st.divider()
    report_text = state["report"] if isinstance(state["report"], str) else str(state["report"])

    tab_report, tab_feedback = st.tabs(["📝 Final Report", "🧐 Critic Feedback"])

    with tab_report:
        st.markdown(report_text)
        st.download_button(
            "⬇️ Download report (.md)",
            data=report_text,
            file_name=f"research_report_{topic.replace(' ', '_')[:40]}.md",
            mime="text/markdown",
        )

    with tab_feedback:
        feedback_text = state["feedback"] if isinstance(state["feedback"], str) else str(state["feedback"])
        st.markdown(feedback_text)
elif not run_clicked:
    st.info("Enter a topic above and click **Run Research** to start the pipeline.")