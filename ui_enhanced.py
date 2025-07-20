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
from cloud_sync import CloudSync

# Page configuration - make it mobile-friendly
st.set_page_config(
    page_title="DSA Mastery",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapse sidebar on mobile
)

# Add mobile-friendly CSS
st.markdown("""
<style>
/* Mobile-friendly styles */
@media (max-width: 768px) {
    .main-header h1 { font-size: 1.5rem !important; }
    .main-header p { font-size: 0.9rem !important; }
    .stButton > button { 
        font-size: 0.8rem !important; 
        padding: 0.3rem 0.6rem !important;
        margin: 0.1rem !important;
    }
    .stSelectbox > div > div { font-size: 0.8rem !important; }
    .stTextInput > div > div > input { font-size: 0.8rem !important; }
    .stTextArea > div > div > textarea { font-size: 0.8rem !important; }
    .stMarkdown { font-size: 0.9rem !important; }
    .stExpander { margin: 0.2rem 0 !important; }
    .stColumns { gap: 0.5rem !important; }
}

/* Compact navigation */
.nav-button {
    font-size: 0.8rem !important;
    padding: 0.3rem 0.5rem !important;
    margin: 0.1rem !important;
    border-radius: 0.3rem !important;
}

/* Compact problem cards */
.problem-card {
    padding: 0.5rem !important;
    margin: 0.2rem 0 !important;
    border-radius: 0.3rem !important;
    border: 1px solid #e0e0e0 !important;
}

/* Compact sidebar */
.sidebar .sidebar-content {
    padding: 0.5rem !important;
}

/* Mobile-friendly text */
.mobile-text {
    font-size: 0.9rem !important;
    line-height: 1.3 !important;
}

/* Compact buttons */
.compact-btn {
    font-size: 0.7rem !important;
    padding: 0.2rem 0.4rem !important;
    margin: 0.1rem !important;
}

/* Responsive columns */
@media (max-width: 768px) {
    .stColumns > div { 
        width: 100% !important; 
        margin-bottom: 0.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

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

def setup_cloud_sync():
    """Setup cloud sync for automatic syncing"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ☁️ Cloud Sync Setup")
    
    # Initialize cloud sync
    try:
        cloud_sync = CloudSync()
        status = cloud_sync.get_cloud_status()
        
        # Show current status
        col1, col2 = st.columns(2)
        with col1:
            if status['obsidian']['enabled']:
                st.success(f"📂 Obsidian: {status['obsidian']['method']}")
            else:
                st.info("📂 Obsidian: Not synced")
        
        with col2:
            if status['anki']['enabled']:
                st.success("📚 Anki: Synced")
            else:
                st.info("📚 Anki: Not synced")
        
        # Setup buttons
        if st.button("🔧 Setup Cloud Sync"):
            st.info("""
            **Cloud Sync Options:**
            
            **📂 Obsidian Sync:**
            - GitHub (Free, manual sync)
            - Google Drive (Free, automatic)
            - Dropbox (Free, automatic)
            
            **📚 Anki Sync:**
            - AnkiWeb (Free, automatic)
            
            Run `python cloud_sync.py` in terminal to setup!
            """)
        
        return cloud_sync
        
    except Exception as e:
        st.error(f"Cloud sync error: {e}")
        return None

# Mobile-friendly navigation
def show_mobile_nav():
    """Compact mobile navigation"""
    st.markdown("---")
    nav_cols = st.columns(5)
    with nav_cols[0]:
        if st.button("🏠", help="Dashboard", key="nav_dash", use_container_width=True):
            st.session_state.page = "dashboard"
    with nav_cols[1]:
        if st.button("💻", help="Solve", key="nav_solve", use_container_width=True):
            st.session_state.page = "solve"
    with nav_cols[2]:
        if st.button("📚", help="Browse", key="nav_browse", use_container_width=True):
            st.session_state.page = "browser"
    with nav_cols[3]:
        if st.button("📖", help="Review", key="nav_review", use_container_width=True):
            st.session_state.page = "review"
    with nav_cols[4]:
        if st.button("🎓", help="Study", key="nav_study", use_container_width=True):
            st.session_state.page = "study"
    st.markdown("---")

# Compact dashboard
def show_dashboard(system):
    """Mobile-friendly dashboard"""
    # Show cloud status and sync instructions
    show_cloud_status()
    show_sync_instructions()
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 DSA Mastery</h1>
        <p class="mobile-text">Track progress & master DSA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact stats
    col1, col2, col3 = st.columns(3)
    with col1:
        completed = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"])
        st.metric("✅ Done", completed)
    with col2:
        total = len(system.neetcode)
        st.metric("📊 Total", total)
    with col3:
        progress = int((completed / total) * 100) if total > 0 else 0
        st.metric("📈 Progress", f"{progress}%")
    
    # Compact today's problem
    st.subheader("🎯 Today's Problem")
    pattern, today_problem = system.get_today_problem()
    if today_problem:
        status = str(today_problem.get("status", "")).lower()
        if status != "completed":
            st.markdown(f"""
            <div class="problem-card">
                <strong>{today_problem['id']} - {today_problem['title']}</strong><br>
                <small>{today_problem['difficulty']} • {today_problem['pattern']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💻 Solve", key="solve_today", use_container_width=True):
                    st.session_state.page = "solve"
            with col2:
                if st.button("⏭️ Skip", key="skip_today", use_container_width=True):
                    system.mark_problem_status(today_problem["id"], "skipped")
                    st.rerun()
        else:
            st.success("✅ Today's problem completed!")
    else:
        st.info("No problem assigned for today")
    
    # Compact recent activity
    with st.expander("📋 Recent Activity", expanded=False):
        recent_problems = [p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"][-5:]
        for p in recent_problems:
            st.markdown(f"✅ {p['id']} - {p['title']} ({p['difficulty']})")

# Compact solve interface
def show_solve_interface(system):
    """Mobile-friendly solve interface"""
    st.markdown("""
    <div class="main-header">
        <h1>💻 Solve Problems</h1>
        <p class="mobile-text">Practice DSA with AI guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact pattern selector
    all_patterns = system.get_learning_order_patterns()
    selected_pattern = st.selectbox("📂 Pattern", all_patterns, 
                                   index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, 
                                   key="solve_pattern_select")
    st.session_state.selected_pattern = selected_pattern
    
    # Compact today's problem
    pattern, today_problem = system.get_today_problem()
    if today_problem and isinstance(today_problem, dict) and today_problem.get("pattern") == selected_pattern:
        st.subheader(f"🎯 {today_problem['id']} - {today_problem['title']}")
        st.markdown(f"**{today_problem['difficulty']}** • {today_problem['pattern']}")
        
        # Compact problem description
        with st.expander("📝 Problem Description", expanded=False):
            st.markdown(today_problem.get("description", "No description available"))
        
        # Compact code input
        st.subheader("💻 Your Solution")
        user_code = st.text_area("Code", value=st.session_state.get("user_code", ""), 
                                height=200, key="code_input", 
                                placeholder="Write your solution here...")
        st.session_state.user_code = user_code
        
        # Compact action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Analyze", key="analyze_code", use_container_width=True):
                if user_code.strip():
                    with st.spinner("Analyzing..."):
                        analysis = system.analyze_solution(today_problem, user_code)
                        st.session_state.analysis = analysis
                        st.session_state.code_explanation = generate_code_explanation(today_problem, user_code, "python")
                else:
                    st.warning("Please write some code first")
        
        with col2:
            if st.button("✅ Mark Complete", key="mark_complete", use_container_width=True):
                system.mark_problem_status(today_problem["id"], "completed")
                st.success("Problem marked as completed!")
                st.rerun()
        
        # Compact analysis results
        if st.session_state.analysis:
            with st.expander("📊 Analysis Results", expanded=False):
                display_analysis_results(st.session_state.analysis, "python")
        
        # Compact code explanation
        if st.session_state.code_explanation:
            with st.expander("💡 Code Explanation", expanded=False):
                display_code_explanation(st.session_state.code_explanation)
        
        # Compact note generation
        if st.session_state.analysis:
            note_md, flashcards = system.generate_dsa_note(today_problem, user_code)
            st.session_state[f"flashcards_{today_problem['id']}"] = flashcards
            st.session_state[f"note_md_{today_problem['id']}"] = note_md
            
            with st.expander("📝 Generated Note", expanded=False):
                st.markdown(note_md, unsafe_allow_html=True)
                
                if st.button("💾 Save Note", key=f"save_note_{today_problem['id']}", use_container_width=True):
                    result = system.save_dsa_note_and_flashcards(today_problem, note_md, st.session_state.get(f"flashcards_{today_problem['id']}", []))
                    st.success("✅ Note saved!")
                    
                    # Cloud sync integration
                    if 'cloud_sync' in locals() and cloud_sync:
                        try:
                            filename = f"{today_problem['id']} - {today_problem['title']}.md"
                            if cloud_sync.sync_note_to_cloud(note_md, filename):
                                st.success("☁️ Synced to cloud!")
                            
                            flashcards = st.session_state.get(f"flashcards_{today_problem['id']}", [])
                            if flashcards:
                                deck_name = f"DSA_{today_problem['pattern']}"
                                if cloud_sync.sync_flashcards_to_anki(flashcards, deck_name):
                                    st.success("📚 Synced to Anki!")
                        except Exception as e:
                            st.warning(f"Cloud sync: {e}")
        
        # Compact AI chat
        with st.expander("🤖 AI Chat", expanded=False):
            user_query = st.text_input("Ask AI...", key=f"chat_{today_problem['id']}", placeholder="Type your question...")
            if st.button("Ask", key=f"askai_{today_problem['id']}", use_container_width=True):
                if user_query.strip():
                    with st.spinner("AI thinking..."):
                        try:
                            note_md = st.session_state.get(f"note_md_{today_problem['id']}", "")
                            chat_prompt = f"User question: {user_query}\n\nProblem: {today_problem['title']}\n\nNote: {note_md}\n\nCode: {user_code}"
                            ai_response = call_ai_api(chat_prompt)
                            st.session_state[f"chat_resp_{today_problem['id']}"] = ai_response
                        except Exception as e:
                            st.session_state[f"chat_resp_{today_problem['id']}"] = f"AI error: {e}"
            
            chat_resp = st.session_state.get(f"chat_resp_{today_problem['id']}")
            if chat_resp:
                st.markdown(f"**AI:** {chat_resp}")
    
    # Compact problem list
    st.subheader(f"📋 {selected_pattern} Problems")
    problems = system.get_problems_by_pattern(selected_pattern)
    for p in problems:
        status = str(p.get("status", "")).lower()
        status_emoji = "✅" if status == "completed" else ("⏭️" if status == "skipped" else "⏳")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"{status_emoji} **{p['id']} - {p['title']}**")
        with col2:
            st.markdown(f"`{p['difficulty']}`")
        with col3:
            if st.button("Notes", key=f"notes_{p['id']}", use_container_width=True):
                # Show notes in modal
                note_content = st.session_state.get(f"note_md_{p['id']}", "No notes available")
                st.markdown(f"**Notes for {p['id']}:**")
                st.markdown(note_content)

# Compact problem browser
def show_problem_browser(system):
    """Mobile-friendly problem browser"""
    st.markdown("""
    <div class="main-header">
        <h1>📚 Problem Browser</h1>
        <p class="mobile-text">Browse and filter all problems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact filters
    col1, col2 = st.columns(2)
    with col1:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"], key="browser_difficulty")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Not Started", "Completed", "Skipped"], key="browser_status")
    
    pattern_filter = st.selectbox("Pattern", ["All"] + system.get_learning_order_patterns(), key="browser_pattern")
    
    # Filter problems
    filtered_problems = system.neetcode
    if difficulty_filter != "All":
        filtered_problems = [p for p in filtered_problems if str(p.get("difficulty", "")).strip().lower() == difficulty_filter.lower()]
    if status_filter != "All":
        status_map = {"Not Started": ["", None, "not started"], "Completed": ["completed"], "Skipped": ["skipped"]}
        target_statuses = status_map[status_filter]
        filtered_problems = [p for p in filtered_problems if (str(p.get("status", "")).strip().lower() in [s for s in target_statuses if s is not None]) or (p.get("status") is None and None in target_statuses)]
    if pattern_filter != "All":
        filtered_problems = [p for p in filtered_problems if str(p.get("pattern", "")).strip() == pattern_filter]
    
    # Compact problem list
    st.subheader(f"📋 Problems ({len(filtered_problems)})")
    for problem in filtered_problems:
        status = str(problem.get("status", "")).lower()
        status_emoji = {"completed": "✅", "skipped": "⏭️", "": "⏳"}.get(status, "⏳")
        
        st.markdown(f"""
        <div class="problem-card">
            {status_emoji} <strong>{problem['id']} - {problem['title']}</strong><br>
            <small>{problem['difficulty']} • {problem['pattern']}</small>
        </div>
        """, unsafe_allow_html=True)

# Compact review interface
def show_review_interface(system):
    """Mobile-friendly review interface"""
    st.markdown("""
    <div class="main-header">
        <h1>📖 Review Notes</h1>
        <p class="mobile-text">Review your notes and flashcards</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pattern selector
    all_patterns = system.get_learning_order_patterns()
    selected_pattern = st.selectbox("Pattern", all_patterns, 
                                   index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, 
                                   key="review_pattern_select")
    st.session_state.selected_pattern = selected_pattern
    
    # Solved problems
    solved_problems = [p for p in system.get_problems_by_pattern(selected_pattern) if str(p.get("status", "")).lower() == "completed"]
    
    if not solved_problems:
        st.info("No solved problems in this pattern yet.")
        return
    
    # Problem selector
    problem_titles = [f"{p['id']} - {p['title']}" for p in solved_problems]
    selected_idx = st.selectbox("Select problem", list(range(len(problem_titles))), 
                               format_func=lambda i: problem_titles[i], key="review_problem_select")
    problem = solved_problems[selected_idx]
    
    # Show note
    note_path = f"{OBSIDIAN_VAULT}/Problems/{problem['id']} - {problem['title']}.md"
    note_md = None
    if os.path.exists(note_path):
        with open(note_path, "r", encoding="utf-8") as f:
            note_md = f.read()
    
    if note_md:
        with st.expander(f"📝 Note for {problem['id']}", expanded=True):
            st.markdown(note_md, unsafe_allow_html=True)
    else:
        st.warning("No note available for this problem")
    
    # Flashcards
    progress = system.progress.get("problems", {}).get(problem["id"], {})
    flashcards = progress.get("analysis", {}).get("flashcards", [])
    
    if flashcards:
        with st.expander("🃏 Flashcards", expanded=False):
            for i, card in enumerate(flashcards, 1):
                st.markdown(f"**{i}.** {card}")

# Compact study mode
def show_study_mode(system):
    """Mobile-friendly study mode"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Study Mode</h1>
        <p class="mobile-text">Focused study sessions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pattern selector
    all_patterns = system.get_learning_order_patterns()
    selected_pattern = st.selectbox("Study Pattern", all_patterns, 
                                   index=all_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in all_patterns else 0, 
                                   key="study_pattern_select")
    st.session_state.selected_pattern = selected_pattern
    
    # Pattern introduction
    if st.button("📚 Get Pattern Intro", key="pattern_intro_btn"):
        prompt = f"Explain the {selected_pattern} pattern in DSA. Include key concepts, common problems, and study tips."
        try:
            pattern_intro = call_ai_api(prompt)
            if pattern_intro and pattern_intro.strip():
                st.session_state.pattern_intro = pattern_intro
            else:
                st.session_state.pattern_intro = f"## {selected_pattern}\n\nThis is a fundamental pattern in Data Structures and Algorithms. Practice problems in this pattern to master the concept."
            st.session_state.pattern_intro_pattern = selected_pattern
        except Exception as e:
            st.session_state.pattern_intro = f"## {selected_pattern}\n\nThis is a fundamental pattern in Data Structures and Algorithms. Practice problems in this pattern to master the concept.\n\n*Note: AI introduction failed: {e}*"
            st.session_state.pattern_intro_pattern = selected_pattern
    
    if st.session_state.get("pattern_intro") and st.session_state.get("pattern_intro_pattern") == selected_pattern:
        with st.expander("📚 Pattern Introduction", expanded=False):
            st.markdown(st.session_state.pattern_intro, unsafe_allow_html=True)
    
    # Study problems
    problems = system.get_problems_by_pattern(selected_pattern)
    unsolved = [p for p in problems if str(p.get("status", "")).lower() != "completed"]
    
    if unsolved:
        st.subheader(f"📝 Study Problems ({len(unsolved)})")
        for p in unsolved[:5]:  # Show only first 5 for mobile
            st.markdown(f"""
            <div class="problem-card">
                <strong>{p['id']} - {p['title']}</strong><br>
                <small>{p['difficulty']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🎉 All problems in this pattern completed!")

# Update main function to use mobile navigation
def main():
    # Initialize system
    system = get_system()
    
    # Setup cloud sync
    cloud_sync = setup_cloud_sync()
    
    # Initialize session state
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'user_code' not in st.session_state:
        st.session_state.user_code = ""
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'code_explanation' not in st.session_state:
        st.session_state.code_explanation = None
    if 'selected_pattern' not in st.session_state:
        all_patterns = system.get_learning_order_patterns()
        st.session_state.selected_pattern = all_patterns[0] if all_patterns else None

    # Mobile navigation
    show_mobile_nav()
    
    # Display selected page
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
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

def show_cloud_status():
    """Show cloud deployment status and instructions"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Cloud Deployment")
    
    # Check if running on Streamlit Cloud
    import os
    is_cloud = os.environ.get('STREAMLIT_SERVER_HEADLESS', False)
    
    if is_cloud:
        st.sidebar.success("✅ Running on Cloud")
        st.sidebar.info("""
        **Cloud Features:**
        - 📱 Mobile access
        - 🤖 AI chat
        - 📝 Note generation
        - 📊 Progress tracking
        
        **Export Options:**
        - 📥 Download notes
        - 📊 Export flashcards
        - 📋 Copy to clipboard
        """)
    else:
        st.sidebar.info("💻 Running Locally")
        st.sidebar.info("""
        **Local Features:**
        - 📁 Direct Obsidian save
        - 🃏 Direct Anki export
        - 📚 NotebookLM export
        """)
    
    st.sidebar.markdown("---")

def show_sync_instructions():
    """Show instructions for syncing between mobile and local PC"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Mobile ↔ PC Sync")
    
    st.sidebar.info("""
    **Mobile Workflow:**
    1. 📱 Solve problems on phone
    2. 📝 Generate notes & flashcards
    3. 📥 Download files
    4. 💻 Transfer to PC when home
    
    **PC Integration:**
    1. 📁 Copy downloaded files to PC
    2. 📂 Place notes in Obsidian vault
    3. 📊 Import flashcards to Anki
    4. 📚 Export to NotebookLM
    """)
    
    # Quick sync guide
    with st.sidebar.expander("📋 Sync Guide"):
        st.markdown("""
        **Step 1: Mobile (While Traveling)**
        - Solve problems and generate notes
        - Download notes and flashcards
        - Save to phone storage
        
        **Step 2: PC (When Home)**
        - Connect phone to PC
        - Copy files to your folders:
          - Notes → `~/Obsidian/DSA/Problems/`
          - Flashcards → Import to Anki
          - NotebookLM → Export from Obsidian
        
        **Step 3: Seamless Workflow**
        - All tools stay on your PC
        - Mobile just generates content
        - Perfect sync when you're home
        """)

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

if __name__ == "__main__":
    main() 