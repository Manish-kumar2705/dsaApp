#!/usr/bin/env python3
"""
Enhanced DSA Mastery System UI
A better, more functional interface for DSA practice
"""

import streamlit as st
import json
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
from dsa_system import DSAMasterySystem
from config import *
from ai_client import call_ai_api
import os

# Page configuration
st.set_page_config(
    page_title="DSA Mastery System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .problem-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .analysis-card {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .error-card {
        background: #ffeaea;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #F44336;
        margin: 1rem 0;
    }
    
    .difficulty-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .difficulty-easy { background: #4CAF50; color: white; }
    .difficulty-medium { background: #FF9800; color: white; }
    .difficulty-hard { background: #F44336; color: white; }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    .code-block {
        background: #f4f4f4;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #667eea;
        font-family: 'Courier New', monospace;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_system():
    """Get cached system instance"""
    return DSAMasterySystem()

def main():
    # Initialize system
    system = get_system()
    
    # Initialize session state
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'user_code' not in st.session_state:
        st.session_state.user_code = ""
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'code_explanation' not in st.session_state:
        st.session_state.code_explanation = None
    # Shared pattern selector state
    if 'selected_pattern' not in st.session_state:
        all_patterns = system.get_learning_order_patterns()
        st.session_state.selected_pattern = all_patterns[0] if all_patterns else None

    # --- Move navigation to top of main page ---
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    with nav_col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
    with nav_col2:
        if st.button("💻 Solve Problems", use_container_width=True):
            st.session_state.page = "solve"
    with nav_col3:
        if st.button("📚 Problem Browser", use_container_width=True):
            st.session_state.page = "browser"
    with nav_col4:
        if st.button("📖 Review Notes", use_container_width=True):
            st.session_state.page = "review"
    with nav_col5:
        if st.button("🎓 Study Mode", use_container_width=True):
            st.session_state.page = "study"
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

    # --- Display selected page ---
    if st.session_state.page == "dashboard":
        show_dashboard(system)
    elif st.session_state.page == "solve":
        show_solve_interface(system)
    elif st.session_state.page == "browser":
        show_problem_browser(system)
    elif st.session_state.page == "review":
        show_review_interface(system)
    elif st.session_state.page == "study":
        show_study_mode(system)

def show_dashboard(system):
    st.markdown("""
    <div class="main-header">
        <h1>🎯 DSA Mastery Dashboard</h1>
        <p>Track your progress and master Data Structures & Algorithms</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Motivational message and stats ---
    st.markdown("""
    <div style='background:linear-gradient(90deg,#e0eafc,#cfdef3);padding:1rem 1.5rem;border-radius:8px;margin-bottom:1rem;'>
        <b>Goal:</b> Become the best at DSA! 🚀<br>
        Stay consistent, keep learning, and you'll master every pattern and problem.
    </div>
    """, unsafe_allow_html=True)

    # --- Stats section ---
    total_problems = len(system.neetcode)
    completed = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"])
    skipped = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "skipped"])
    remaining = total_problems - completed - skipped
    percent = (completed / total_problems * 100) if total_problems else 0
    stat_cols = st.columns([2,2,2,2,2])
    with stat_cols[0]:
        st.metric("Total", total_problems)
    with stat_cols[1]:
        st.metric("Completed", completed)
    with stat_cols[2]:
        st.metric("Skipped", skipped)
    with stat_cols[3]:
        st.metric("Remaining", remaining)
    with stat_cols[4]:
        st.metric("% Done", f"{percent:.1f}%")

    # --- Shared pattern selector ---
    all_patterns = system.get_learning_order_patterns()
    st.subheader("Choose Pattern to View Progress")
    selected_pattern = st.selectbox("Pattern", all_patterns, index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, key="dashboard_pattern_select")
    st.session_state.selected_pattern = selected_pattern

    # --- Seamless Integration Status ---
    st.markdown("---")
    st.subheader("🔗 Integration Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📁 Obsidian Vault**")
        if os.path.exists(OBSIDIAN_VAULT):
            st.success(f"✅ Connected: {OBSIDIAN_VAULT}")
        else:
            st.error("❌ Vault not found")
    
    with col2:
        st.markdown("**📚 Anki Integration**")
        try:
            import requests
            resp = requests.get("http://localhost:8765", timeout=2)
            if resp.status_code == 200:
                st.success("✅ AnkiConnect Active")
            else:
                st.warning("⚠️ AnkiConnect not responding")
        except:
            st.error("❌ AnkiConnect not available")
    
    with col3:
        st.markdown("**🤖 NotebookLM Export**")
        notebooklm_dir = Path("notebooklm_export")
        if notebooklm_dir.exists():
            st.success("✅ Export directory ready")
        else:
            st.info("ℹ️ Export directory will be created")
    
    # --- Quick Actions ---
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Export All to NotebookLM", use_container_width=True):
            try:
                from notebooklm_export import export_for_notebooklm
                with st.spinner("📤 Exporting all notes to NotebookLM..."):
                    export_for_notebooklm()
                st.success("✅ All notes exported to NotebookLM!")
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    with col2:
        if st.button("🔄 Sync Progress", use_container_width=True):
            try:
                system.save_progress()
                st.success("✅ Progress synced across all tools!")
            except Exception as e:
                st.error(f"Sync failed: {e}")
    
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            try:
                # Generate a progress report
                completed_by_pattern = {}
                for p in system.neetcode:
                    if str(p.get("status", "")).lower() == "completed":
                        pattern = p.get("pattern", "Unknown")
                        if pattern not in completed_by_pattern:
                            completed_by_pattern[pattern] = 0
                        completed_by_pattern[pattern] += 1
                
                st.markdown("**📊 Progress by Pattern:**")
                for pattern, count in completed_by_pattern.items():
                    st.write(f"• {pattern}: {count} problems")
            except Exception as e:
                st.error(f"Report generation failed: {e}")

    # --- Show current pattern and today's problem ---
    st.subheader("📅 Today's Problem (Pattern-wise)")
    pattern, today_problem = system.get_today_problem(selected_pattern)
    if today_problem:
        st.markdown(f"""
        <div class="problem-card">
            <h4>Current Pattern: <span class='difficulty-badge'>{pattern}</span></h4>
            <p><strong>{today_problem['id']} - {today_problem['title']}</strong></p>
            <p>Difficulty: <span class='difficulty-badge difficulty-{today_problem['difficulty'].lower()}'>{today_problem['difficulty']}</span></p>
            <a href="{today_problem['url']}" target="_blank">🔗 LeetCode Link</a>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start Solving Today's Problem", use_container_width=True, type="primary"):
            st.session_state.current_problem = today_problem
            st.session_state.user_code = ""
            st.session_state.analysis = None
            st.session_state.code_explanation = None
            st.session_state.page = "solve"
            st.rerun()
    else:
        st.success("🎉 All problems completed! You have mastered NeetCode 150.")

    # --- List all problems in current pattern with status, green tick, and Revise button ---
    if selected_pattern:
        st.subheader(f"🗂️ {selected_pattern} Pattern Progress")
        problems = system.get_problems_by_pattern(selected_pattern)
        for i, p in enumerate(problems):
            status = str(p.get("status", "")).lower()
            status_emoji = "✅" if status == "completed" else ("⏭️" if status == "skipped" else "⏳")
            line = f"{status_emoji} **{p['id']} - {p['title']}** ({p['difficulty']})"
            progress = system.progress.get("problems", {}).get(p["id"], {})
            summary = ""
            if status == "completed":
                analysis = progress.get("analysis", {})
                one_liner = analysis.get("approach_summary") or analysis.get("complexity") or "Solved"
                summary = f" — _{one_liner}_"
            cols = st.columns([6, 2, 2])
            with cols[0]:
                st.markdown(line + summary)
            with cols[1]:
                st.markdown(f"[LeetCode]({p['url']})")
            with cols[2]:
                if status == "completed":
                    if st.button(f"Revise {i}", key=f"revise_{p['id']}"):
                        st.session_state.current_problem = p
                        st.session_state.user_code = ""
                        st.session_state.analysis = None
                        st.session_state.code_explanation = None
                        st.session_state.page = "solve"
                        st.rerun()

    # --- Study session (planned, not random) ---
    st.subheader("🎓 Study Session")
    if pattern:
        study_set = [p for p in system.get_problems_by_pattern(pattern) if str(p.get("status", "")).lower() != "completed"][:5]
        st.write(f"Next up in {pattern} pattern:")
        for p in study_set:
            st.markdown(f"- **{p['id']} - {p['title']}** ({p['difficulty']})")
        if st.button("🎓 Start Study Session", use_container_width=True):
            if study_set:
                st.session_state.study_session = study_set
                st.session_state.study_index = 0
                st.session_state.current_problem = study_set[0]
                st.session_state.user_code = ""
                st.session_state.analysis = None
                st.session_state.code_explanation = None
                st.session_state.page = "solve"
                st.rerun()
            else:
                st.info("No more problems left in this pattern!")
    else:
        st.info("All patterns completed!")

def show_solve_interface(system):
    st.markdown("""
    <div class="main-header" style="font-size:1.5rem;">
        <h1 style='font-size:2rem;'>💻 Solve Problems</h1>
        <p style='font-size:1rem;'>Practice with AI-powered guidance and feedback</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Shared pattern selector in learning order ---
    all_patterns = system.get_learning_order_patterns()
    st.subheader("Choose Pattern to Practice")
    selected_pattern = st.selectbox("Pattern", all_patterns, index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, key="solve_pattern_select")
    st.session_state.selected_pattern = selected_pattern

    # --- Pattern introduction (AI-powered, improved prompt) ---
    if 'pattern_intro' not in st.session_state or st.session_state.pattern_intro_pattern != selected_pattern:
        with st.spinner("Fetching pattern introduction from AI..."):
            prompt = f"""
            Give a concise, interview-focused introduction to the DSA pattern: {selected_pattern}.
            - What is this pattern and when is it used?
            - What are the most common data structures and algorithms involved?
            - What types of problems does it solve?
            - Summarize the typical approach in 2-3 sentences.
            - Provide a general Java code template for this pattern (if applicable), in a code block.
            Respond in markdown, with the code template in a separate section at the end.
            """
            from ai_client import call_ai_api
            st.session_state.pattern_intro = call_ai_api(prompt)
            st.session_state.pattern_intro_pattern = selected_pattern
    st.markdown(f"#### About {selected_pattern}", unsafe_allow_html=True)
    with st.expander("Show Pattern Overview & Template", expanded=False):
        st.markdown(st.session_state.pattern_intro)

    # --- Show current pattern and today's problem ---
    st.markdown(f"### Current Pattern: <span class='difficulty-badge'>{selected_pattern}</span>", unsafe_allow_html=True)
    _, today_problem = system.get_today_problem(selected_pattern)
    if today_problem:
        st.markdown(f"""
        <div class="problem-card">
            <h4>Today's Problem</h4>
            <p><strong>{today_problem['id']} - {today_problem['title']}</strong></p>
            <p>Difficulty: <span class='difficulty-badge difficulty-{today_problem['difficulty'].lower()}'>{today_problem['difficulty']}</span></p>
            <a href="{today_problem['url']}" target="_blank">🔗 LeetCode Link</a>
        </div>
        """, unsafe_allow_html=True)
        # --- Single column: code input, then note preview, then chatbox ---
        st.markdown("#### Paste your Java solution (or leave blank for AI solution):")
        code_key = f"code_{today_problem['id']}"
        user_code = st.session_state.get(code_key, "")
        user_code = st.text_area("Java Code", value=user_code, key=code_key, height=180, placeholder="Paste your Java code here...")
        # --- Get Solution/Explanation button ---
        if st.button("Get Solution/Explanation", key=f"getsol_{today_problem['id']}"):
            with st.spinner("Generating detailed solution and notes with AI..."):
                try:
                    # Updated prompt: always use user code if provided, ask AI to review, suggest corrections, and provide better implementation
                    note_md, flashcards = system.generate_dsa_note(today_problem, user_code)
                    if not note_md or not note_md.strip():
                        st.session_state[f"note_md_{today_problem['id']}"] = None
                        st.session_state[f"flashcards_{today_problem['id']}"] = []
                        st.error("AI did not return a valid note. Please try again or check your API key.")
                    else:
                        st.session_state[f"note_md_{today_problem['id']}"] = note_md
                        st.session_state[f"flashcards_{today_problem['id']}"] = flashcards
                except Exception as e:
                    st.session_state[f"note_md_{today_problem['id']}"] = None
                    st.session_state[f"flashcards_{today_problem['id']}"] = []
                    st.error(f"Analysis failed: {e}")
        # --- Note preview (centered) ---
        note_md = st.session_state.get(f"note_md_{today_problem['id']}")
        if note_md:
            st.markdown("---")
            st.markdown("<div style='text-align:center;'><h4>AI-Generated Note Preview</h4></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='max-width:700px;margin:auto;'>{note_md}</div>", unsafe_allow_html=True)
            if st.button("Save to Notes", key=f"save_note_{today_problem['id']}"):
                result = system.save_dsa_note_and_flashcards(today_problem, note_md, st.session_state.get(f"flashcards_{today_problem['id']}", []))
                st.success(f"Note and flashcards saved! (Obsidian: {result.get('note_path')})")
                st.info(f"Saved file path: {result.get('note_path')}")
                st.markdown("---")
                st.markdown("#### Export & Review Actions")
                col1, col2, col3 = st.columns(3)
                with col1:
                    note_path = result.get('note_path')
                    if note_path and os.path.exists(note_path):
                        if st.button("Open in Obsidian", key=f"open_obsidian_save_{today_problem['id']}"):
                            import subprocess
                            subprocess.Popen(["cmd", "/c", "start", note_path], shell=True)
                with col2:
                    if st.button("Export to NotebookLM", key=f"export_notebooklm_save_{today_problem['id']}"):
                        try:
                            from notebooklm_export import export_for_notebooklm
                            with st.spinner("Exporting to NotebookLM..."):
                                export_for_notebooklm()
                            st.success("✅ Exported to NotebookLM!")
                        except Exception as e:
                            st.error(f"NotebookLM export failed: {e}")
                with col3:
                    if st.button("Send to Anki (AnkiConnect)", key=f"send_anki_connect_save_{today_problem['id']}"):
                        try:
                            from anki_manager import send_complete_to_anki
                            # Use the note and flashcards from the result/session
                            note_md = st.session_state.get(f"note_md_{today_problem['id']}")
                            flashcards = st.session_state.get(f"flashcards_{today_problem['id']}", [])
                            analysis = {"flashcards": flashcards}
                            success, results = send_complete_to_anki(today_problem, analysis, note_md)
                            if success:
                                st.success(f"✅ Sent {len(flashcards)} cards + note summary to Anki via AnkiConnect!")
                            else:
                                st.error(f"Some items failed: {results}")
                        except Exception as e:
                            st.error(f"AnkiConnect error: {e}")
                st.markdown("---")
                st.markdown("#### Export Status")
                st.markdown(f"- Obsidian: {'✅' if result.get('obsidian') else '❌'}")
                st.markdown(f"- Anki: {'✅' if result.get('anki') else '❌'}")
                st.markdown(f"- NotebookLM: {'✅' if result.get('notebooklm') else '❌'}")
                if result.get('error'):
                    st.error(f"Errors: {result['error']}")
                # Button to open in Obsidian
                note_path = result.get('note_path')
                if note_path and os.path.exists(note_path):
                    if st.button("Open in Obsidian", key=f"open_obsidian_save_{today_problem['id']}"):
                        import subprocess
                        subprocess.Popen(["cmd", "/c", "start", note_path], shell=True)
                # Button to review in Anki
                if st.button("Review in Anki", key=f"review_anki_save_{today_problem['id']}"):
                    st.info("Open Anki and review your new flashcards for this problem!")
            # --- Chatbox for further AI queries ---
            st.markdown("---")
            st.markdown("#### Ask AI about this problem/note")
            chat_key = f"chat_{today_problem['id']}"
            user_query = st.text_input("Type your question...", key=chat_key)
            if st.button("Ask AI", key=f"askai_{today_problem['id']}"):
                if user_query.strip():
                    with st.spinner("AI is thinking..."):
                        try:
                            chat_prompt = f"You are a DSA tutor. The user is reviewing the following problem and note:\n\n{note_md}\n\nUser's code (if any):\n{user_code}\n\nUser's question: {user_query}\n\nFirst, review the user's code (if provided), suggest corrections and improvements, and then answer the question in detail, referencing the note/code if relevant."
                            ai_response = call_ai_api(chat_prompt)
                            st.session_state[f"chat_resp_{today_problem['id']}"] = ai_response
                        except Exception as e:
                            st.session_state[f"chat_resp_{today_problem['id']}"] = f"AI error: {e}"
                else:
                    st.session_state[f"chat_resp_{today_problem['id']}"] = "Please enter a question."
            chat_resp = st.session_state.get(f"chat_resp_{today_problem['id']}")
            if chat_resp:
                st.markdown(f"**AI Response:**\n{chat_resp}")
    else:
        st.success("🎉 All problems in this pattern are completed!")

    # --- List all problems in selected pattern with status, one-liner, Note section, and Notes button ---
    st.subheader(f"🗂️ {selected_pattern} Pattern Problems")
    problems = system.get_problems_by_pattern(selected_pattern)
    for i, p in enumerate(problems):
        status = str(p.get("status", "")).lower()
        status_emoji = "✅" if status == "completed" else ("⏭️" if status == "skipped" else "⏳")
        line = f"{status_emoji} <b>{p['id']} - {p['title']}</b> <span style='font-size:0.9rem;'>({p['difficulty']})</span>"
        progress = system.progress.get("problems", {}).get(p["id"], {})
        analysis = progress.get("analysis", {})
        one_liner = analysis.get("approach_summary") or analysis.get("complexity") or "Solved"
        # Save the one-liner in progress if not already present
        if status == "completed":
            if "problems" in system.progress:
                if p["id"] not in system.progress["problems"]:
                    system.progress["problems"][p["id"]] = {}
                system.progress["problems"][p["id"]]["ai_note"] = one_liner
        cols = st.columns([1, 5, 2, 4, 2, 2])
        col_chk, col0, col1, col2, col3, col_notes = cols[0], cols[1], cols[2], cols[3], cols[4], cols[5]
        with col_chk:
            chk_key = f"done_{p['id']}"
            is_done = str(p.get("status", "")).lower() == "completed"
            checked = st.checkbox("Mark as done", value=is_done, key=chk_key, label_visibility="collapsed")
            if checked and not is_done:
                p["status"] = "completed"
                if "problems" in system.progress:
                    if p["id"] not in system.progress["problems"]:
                        system.progress["problems"][p["id"]] = {}
                    system.progress["problems"][p["id"]]["solved"] = True
            elif not checked and is_done:
                p["status"] = ""
                if "problems" in system.progress and p["id"] in system.progress["problems"]:
                    system.progress["problems"][p["id"]]["solved"] = False
        with col0:
            st.markdown(f"<div style='display:flex;align-items:center;gap:0.5rem;padding:0;margin:0;'>{line}</div>", unsafe_allow_html=True)
        with col1:
            st.markdown(f"<span class='difficulty-badge difficulty-{p['difficulty'].lower()}' style='font-size:0.8rem;'>{p['difficulty']}</span>", unsafe_allow_html=True)
        with col2:
            note_key = f"note_{p['id']}"
            if status == "completed":
                st.markdown(f"<span style='font-size:0.95rem;color:#388e3c;padding:0;margin:0;'><b>{one_liner}</b></span>", unsafe_allow_html=True)
            else:
                user_note = st.session_state.get(note_key, "")
                st.text_input("Quick note", value=user_note, key=note_key, placeholder="Add a quick note...", label_visibility="collapsed")
        with col3:
            st.markdown(f"[LeetCode]({p['url']})", unsafe_allow_html=True)
        with col_notes:
            if status == "completed":
                if st.button("Notes", key=f"notes_{p['id']}"):
                    note_path = f"{OBSIDIAN_VAULT}/Problems/{p['id']} - {p['title']}.md"
                    if os.path.exists(note_path):
                        with open(note_path, "r", encoding="utf-8") as f:
                            note_md = f.read()
                        with st.modal(f"Note for {p['id']} - {p['title']}"):
                            st.markdown(note_md, unsafe_allow_html=True)
                    else:
                        st.warning("No solution/note has been generated yet for this problem. Solve the problem to generate a note.")
        st.markdown("<hr style='margin:0.1rem 0;' />", unsafe_allow_html=True)

    with col2:
        if st.session_state.current_problem:
            p = st.session_state.current_problem
            st.subheader(f"🎯 {p['title']}")
            
            # Problem description
            with st.expander("📝 Problem Description", expanded=True):
                st.markdown(p["description"])
            
            # Code editor
            st.subheader("💻 Your Solution")
            
            # Language selector
            language = st.selectbox("Programming Language", ["python", "java", "cpp", "javascript"], index=0)
            
            # Code editor
            st.session_state.user_code = st.text_area(
                "Write your solution here:", 
                st.session_state.user_code,
                height=300,
                help="Write your solution code here. The AI will analyze and provide detailed feedback."
            )
            
            # Action buttons
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("🔍 Analyze Solution", use_container_width=True, type="primary"):
                    if st.session_state.user_code.strip():
                        with st.spinner("🤖 Analyzing with AI..."):
                            try:
                                analysis = system.analyze_solution(p, st.session_state.user_code)
                                st.session_state.analysis = analysis
                                st.success("✅ Analysis complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Analysis failed: {e}")
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn2:
                if st.button("📚 Explain Code", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("🤖 Generating explanation..."):
                            try:
                                explanation = generate_code_explanation(p, st.session_state.user_code, language)
                                st.session_state.code_explanation = explanation
                                st.success("✅ Explanation generated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Explanation failed: {e}")
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn3:
                if st.button("💾 Save & Export All", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("💾 Saving and exporting..."):
                            try:
                                # Save solution
                                simple_analysis = {
                                    "correct": True,
                                    "approach_summary": "Solution saved",
                                    "complexity": "Analysis pending"
                                }
                                system.record_solution(p, st.session_state.user_code, simple_analysis)
                                
                                # Export to NotebookLM
                                from notebooklm_export import export_for_notebooklm
                                export_for_notebooklm()
                                
                                st.success("✅ Solution saved and exported to NotebookLM!")
                            except Exception as e:
                                st.error(f"Save/Export failed: {e}")
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn4:
                if st.button("📤 Export to NotebookLM", use_container_width=True):
                    try:
                        from notebooklm_export import export_for_notebooklm
                        with st.spinner("📤 Exporting to NotebookLM..."):
                            export_for_notebooklm()
                        st.success("✅ Exported to NotebookLM!")
                    except Exception as e:
                        st.error(f"NotebookLM export failed: {e}")
            
            # Display analysis results
            if st.session_state.analysis:
                display_analysis_results(st.session_state.analysis, language)
            
            # Display code explanation
            if st.session_state.code_explanation:
                display_code_explanation(st.session_state.code_explanation)

def display_analysis_results(analysis, language):
    """Display AI analysis results in a nice format"""
    st.divider()
    st.subheader("🤖 AI Analysis Results")
    
    # Overall result
    if analysis.get("correct", False):
        st.markdown('<div class="success-message">✅ Your solution is correct!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-message">⚠️ Your solution needs improvement</div>', unsafe_allow_html=True)
    
    # Analysis details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📝 Analysis Summary**")
        st.write("**Approach:**", analysis.get("approach_summary", "Not provided"))
        st.write("**Complexity:**", analysis.get("complexity", "Not provided"))
        st.write("**Brute Force:**", analysis.get("brute_force", "Not provided"))
        
        # Mistakes
        mistakes = analysis.get("mistakes", [])
        if mistakes:
            st.markdown("**❌ Common Mistakes:**")
            for mistake in mistakes:
                st.write(f"• {mistake}")
    
    with col2:
        st.markdown("**🔧 Optimized Solution**")
        fixed_code = analysis.get("fixed_code", "")
        if fixed_code:
            st.code(fixed_code, language=language)
        else:
            st.write("No optimized solution provided")
    
    # Annotated code
    annotated_code = analysis.get("annotated_code", "")
    if annotated_code:
        st.markdown("**📖 Annotated Solution**")
        st.code(annotated_code, language=language)
    
    # Flashcards
    flashcards = analysis.get("flashcards", [])
    if flashcards:
        st.markdown("**🎯 Study Flashcards**")
        
        # Export to Anki button
        if st.button("📚 Export to Anki", key="export_anki_from_analysis"):
            try:
                from anki_manager import create_flashcards
                csv_file = create_flashcards(flashcards, "DSA Problem")
                if csv_file:
                    st.success(f"✅ Flashcards exported to: {csv_file}")
                    st.info("📚 Import this CSV file into Anki using File → Import")
                else:
                    st.error("Failed to export flashcards")
            except Exception as e:
                st.error(f"Export failed: {e}")
        
        # Display flashcards
        for i, flashcard in enumerate(flashcards, 1):
            if ";" in flashcard:
                question, answer = flashcard.split(";", 1)
                with st.expander(f"Card {i}: {question}"):
                    st.write(answer)

def display_code_explanation(explanation):
    """Display code explanation in a nice format"""
    st.divider()
    st.subheader("📚 Code Explanation")
    st.markdown(explanation)

def generate_code_explanation(problem, code, language):
    """Generate detailed explanation of the code using AI"""
    prompt = f"""
    Problem: {problem['title']}
    Description: {problem['description']}
    
    Code to explain:
    ```{language}
    {code}
    ```
    
    Please provide a detailed explanation including:
    1. What the code does step by step
    2. The algorithm/pattern used
    3. Time and space complexity
    4. Key insights and logic
    5. Potential improvements
    
    Format the response in markdown with clear sections.
    """
    
    try:
        response = call_ai_api(prompt)
        return response
    except Exception as e:
        return f"""
        ## Code Explanation for {problem['title']}
        
        **Note:** AI explanation failed due to: {e}
        
        ### What the code does:
        [AI explanation would appear here]
        
        ### Algorithm Pattern:
        [Pattern detection would appear here]
        
        ### Complexity:
        [Complexity analysis would appear here]
        
        ### Key Insights:
        [Insights would appear here]
        """

def show_problem_browser(system):
    st.markdown("""
    <div class="main-header" style="font-size:1.5rem;">
        <h1 style='font-size:2rem;'>📚 Problem Browser</h1>
        <p style='font-size:1rem;'>Browse and filter all available problems</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Compact filters ---
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"], key="browser_difficulty")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Not Started", "Completed", "Skipped"], key="browser_status")
    with col3:
        all_patterns = system.get_learning_order_patterns()
        pattern_filter = st.selectbox("Pattern", ["All"] + all_patterns, key="browser_pattern")

    # --- Filter problems robustly ---
    filtered_problems = system.neetcode
    if difficulty_filter != "All":
        filtered_problems = [p for p in filtered_problems if str(p.get("difficulty", "")).strip().lower() == difficulty_filter.lower()]
    if status_filter != "All":
        status_map = {"Not Started": ["", None, "not started"], "Completed": ["completed"], "Skipped": ["skipped"]}
        target_statuses = status_map[status_filter]
        filtered_problems = [
            p for p in filtered_problems
            if (str(p.get("status", "")).strip().lower() in [s for s in target_statuses if s is not None]) or (p.get("status") is None and None in target_statuses)
        ]
    if pattern_filter != "All":
        filtered_problems = [p for p in filtered_problems if str(p.get("pattern", "")).strip() == pattern_filter]

    # --- Compact problem list ---
    st.subheader(f"📋 Problems ({len(filtered_problems)} found)")
    for problem in filtered_problems:
        status = str(problem.get("status", "")).lower()
        status_emoji = {"completed": "✅", "skipped": "⏭️", "": "⏳"}.get(status, "⏳")
        # Save AI one-liner note for solved problems if not present
        progress = system.progress.get("problems", {}).get(problem["id"], {})
        analysis = progress.get("analysis", {})
        one_liner = analysis.get("approach_summary") or analysis.get("complexity") or "Solved"
        if status == "completed":
            if "problems" in system.progress:
                if problem["id"] not in system.progress["problems"]:
                    system.progress["problems"][problem["id"]] = {}
                if "ai_note" not in system.progress["problems"][problem["id"]]:
                    system.progress["problems"][problem["id"]]["ai_note"] = one_liner
        cols = st.columns([5, 1, 1])
        col0, col1, col2 = cols[0], cols[1], cols[2]
        with col0:
            st.markdown(f"<span style='font-size:1rem;'>{status_emoji} <b>{problem['id']} - {problem['title']}</b> <span style='font-size:0.9rem;'>({problem['difficulty']})</span></span>", unsafe_allow_html=True)
        with col1:
            st.markdown(f"<span class='difficulty-badge difficulty-{problem['difficulty'].lower()}' style='font-size:0.8rem;'>{problem['difficulty']}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"[LeetCode]({problem['url']})", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0.2rem 0;' />", unsafe_allow_html=True)

def show_review_interface(system):
    st.markdown("""
    <div class="main-header" style="font-size:1.5rem;">
        <h1 style='font-size:2rem;'>📖 Review Notes</h1>
        <p style='font-size:1rem;'>Review your AI-generated notes, flashcards, and revision status for each pattern and problem.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Pattern selector ---
    all_patterns = system.get_learning_order_patterns()
    st.subheader("Choose Pattern to Review")
    selected_pattern = st.selectbox("Pattern", all_patterns, index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, key="review_pattern_select")
    st.session_state.selected_pattern = selected_pattern

    # --- List all solved problems for the selected pattern ---
    solved_problems = [p for p in system.get_problems_by_pattern(selected_pattern) if str(p.get("status", "")).lower() == "completed"]
    st.subheader(f"🗂️ {selected_pattern} - Solved Problems ({len(solved_problems)})")
    if not solved_problems:
        st.info("No solved problems in this pattern yet.")
        return

    # --- Problem selector ---
    problem_titles = [f"{p['id']} - {p['title']}" for p in solved_problems]
    selected_idx = st.selectbox("Select a problem to review", list(range(len(problem_titles))), format_func=lambda i: problem_titles[i], key="review_problem_select")
    problem = solved_problems[selected_idx]

    # --- Load and display the note from Obsidian vault ---
    note_path = f"{OBSIDIAN_VAULT}/Problems/{problem['id']} - {problem['title']}.md"
    note_md = None
    if os.path.exists(note_path):
        with open(note_path, "r", encoding="utf-8") as f:
            note_md = f.read()
    else:
        st.warning("No solution/note has been generated yet for this problem. Solve the problem to generate a note.")
    if note_md:
        st.markdown("---")
        st.markdown(f"#### Note for {problem['id']} - {problem['title']}")
        st.markdown(note_md, unsafe_allow_html=True)

    # --- Flashcards (from progress or parsed from note) ---
    progress = system.progress.get("problems", {}).get(problem["id"], {})
    flashcards = progress.get("analysis", {}).get("flashcards", [])
    if not flashcards and note_md:
        # Try to parse flashcards from note
        flashcards = []
        for line in note_md.splitlines():
            if ";" in line and line.count(";") == 1:
                q, a = line.split(";", 1)
                if len(q.strip()) > 0 and len(a.strip()) > 0:
                    flashcards.append(f"{q.strip()};{a.strip()}")
    with st.expander("Review Flashcards", expanded=False):
        if flashcards:
            for i, card in enumerate(flashcards, 1):
                if ";" in card:
                    q, a = card.split(";", 1)
                    st.markdown(f"**Q{i}:** {q}")
                    st.markdown(f"**A{i}:** {a}")
                    st.markdown("---")
        else:
            st.info("No flashcards found for this problem.")

    # --- Revision status and actions ---
    st.markdown("---")
    st.markdown(f"**Revision Status:** {progress.get('revision_status', 'new')}")
    if st.button("Mark as Revised", key=f"revise_{problem['id']}"):
        if "problems" in system.progress:
            if problem["id"] not in system.progress["problems"]:
                system.progress["problems"][problem["id"]] = {}
            system.progress["problems"][problem["id"]]["revision_status"] = "revised"
            st.success("Marked as revised!")
    st.markdown(f"**Last Reviewed:** {progress.get('last_reviewed', 'Never')}")
    if st.button("Update Last Reviewed Date", key=f"reviewed_{problem['id']}"):
        if "problems" in system.progress:
            if problem["id"] not in system.progress["problems"]:
                system.progress["problems"][problem["id"]] = {}
            from datetime import datetime
            system.progress["problems"][problem["id"]]["last_reviewed"] = datetime.now().isoformat()
            st.success("Last reviewed date updated!")

    # --- Export/Open actions ---
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if os.path.exists(note_path):
            if st.button("Open in Obsidian", key=f"open_obsidian_{problem['id']}"):
                import subprocess
                subprocess.Popen(["cmd", "/c", "start", note_path], shell=True)
    with col2:
        if st.button("Export to NotebookLM", key=f"export_notebooklm_{problem['id']}"):
            try:
                from notebooklm_export import export_for_notebooklm
                export_for_notebooklm()
                st.success("Exported for NotebookLM!")
            except Exception as e:
                st.error(f"Export failed: {e}")
    with col3:
        if st.button("Export to Anki (CSV)", key=f"export_anki_{problem['id']}"):
            if flashcards:
                try:
                    from anki_manager import create_flashcards
                    csv_file = create_flashcards(flashcards, f"{problem['id']} - {problem['title']}")
                    if csv_file:
                        st.success(f"✅ Flashcards exported to: {csv_file}")
                        st.info("📚 Import this CSV file into Anki using File → Import")
                    else:
                        st.error("Failed to export flashcards")
                except Exception as e:
                    st.error(f"Export failed: {e}")
            else:
                st.warning("No flashcards available for this problem")
    with col4:
        if st.button("Send to Anki (AnkiConnect)", key=f"send_anki_connect_{problem['id']}"):
            if flashcards or note_md:
                try:
                    from anki_manager import send_complete_to_anki
                    # Create a simple analysis object with flashcards
                    analysis = {"flashcards": flashcards}
                    success, results = send_complete_to_anki(problem, analysis, note_md)
                    if success:
                        st.success(f"✅ Sent {len(flashcards)} cards + note summary to Anki via AnkiConnect!")
                    else:
                        st.error(f"Some items failed: {results}")
                except Exception as e:
                    st.error(f"AnkiConnect error: {e}")
            else:
                st.warning("No flashcards or notes available for this problem")

    # --- Anki Instructions ---
    with st.expander("📚 How to Use Anki with Your DSA Notes", expanded=False):
        from anki_manager import generate_anki_import_instructions
        st.markdown(generate_anki_import_instructions())

def show_study_mode(system):
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Study Mode</h1>
        <p>Spaced repetition learning for DSA concepts</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🎓 Study mode coming soon! This will include spaced repetition flashcards and concept reviews.")

if __name__ == "__main__":
    main() 