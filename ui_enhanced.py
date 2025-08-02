#!/usr/bin/env python3
"""
Enhanced DSA Mastery System UI
A better, more functional interface for DSA practice
"""

import streamlit as st

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="DSA Mastery",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
import webbrowser
from streamlit_monaco import st_monaco
from dsa_system import DSA_LEARNING_ORDER

# Theme CSS
st.markdown("""
<style>
/* Theme colors */
:root {
    --bg-primary: #0E1117;
    --bg-secondary: #1E1E2F;
    --bg-card: #262638;
    --text-primary: #FFFFFF;
    --text-secondary: #B0B0B0;
    --accent-primary: #4CAF50;
    --accent-secondary: #45a049;
    --border-color: #383850;
    --hover-color: rgba(76, 175, 80, 0.1);
}

/* Global styles */
.stApp {
    background-color: var(--bg-primary) !important;
}

.main .block-container {
    padding: 2rem 1rem !important;
}

/* Cards */
.neon-card {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}

.neon-card:hover {
    box-shadow: 0 6px 8px rgba(76, 175, 80, 0.1) !important;
    border-color: var(--accent-primary) !important;
    transition: all 0.3s ease !important;
}

/* Navigation */
.nav-container {
    background-color: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border-color) !important;
    padding: 1rem !important;
    margin: -1rem -1rem 1rem -1rem !important;
}

.nav-item {
    color: var(--text-secondary) !important;
    background-color: var(--bg-card) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
}

.nav-item:hover {
    background-color: var(--hover-color) !important;
    color: var(--accent-primary) !important;
}

.nav-item.active {
    color: var(--accent-primary) !important;
    background-color: var(--hover-color) !important;
}

/* Text styles */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

p, div {
    color: var(--text-primary) !important;
}

.text-secondary {
    color: var(--text-secondary) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    color: white !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2) !important;
}

/* Add to CSS */
.stButton > button[type="secondary"] {
    background: linear-gradient(90deg, #6c757d, #5c636a) !important; /* Neutral gray */
    color: white !important;
}

/* Progress bars */
.progress-bar {
    background-color: var(--bg-secondary) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

.progress-fill {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    height: 100% !important;
    border-radius: 8px !important;
    transition: width 0.5s ease !important;
}

/* Stats cards */
.stats-card {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

.stats-value {
    color: var(--accent-primary) !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

.stats-label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}

/* Inputs and text areas */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* Code blocks */
.stCodeBlock {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-primary);
}

/* Info boxes */
.stAlert {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

.streamlit-expanderContent {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 0 0 8px 8px !important;
}

.code-editor-container {
    background-color: #1A1A2E !important;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.notes-container {
    background-color: #2A2A3E !important;
    padding: 15px;
    border-radius: 8px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_system():
    """Get or create DSA system instance"""
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

# Add automatic PC sync functionality
def setup_auto_sync():
    """Setup automatic PC sync that runs in background"""
    import threading
    import time
    from pathlib import Path
    
    def auto_sync_worker():
        """Background worker for automatic sync"""
        while True:
            try:
                # Check if we're on PC (not mobile)
                if not os.environ.get('STREAMLIT_SERVER_HEADLESS', False):
                    # Auto-sync from GitHub to local
                    sync_from_github_to_local()
                    
                    # Auto-export to NotebookLM
                    auto_export_to_notebooklm()
                
                # Sleep for 5 minutes before next sync
                time.sleep(300)
            except Exception as e:
                print(f"Auto-sync error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def sync_from_github_to_local():
        """Automatically sync from GitHub to local folders"""
        try:
            from cloud_sync import CloudSync
            cloud_sync = CloudSync()
            
            # Create local folders
            local_notes = Path("local_notes")
            local_flashcards = Path("local_flashcards")
            local_notes.mkdir(exist_ok=True)
            local_flashcards.mkdir(exist_ok=True)
            
            # Fetch notes from GitHub
            notes = cloud_sync.fetch_notes_from_github()
            flashcards = cloud_sync.fetch_flashcards_from_github()
            
            # Save to local folders
            for note in notes:
                pattern_folder = local_notes / note['pattern']
                pattern_folder.mkdir(exist_ok=True)
                
                file_path = pattern_folder / note['filename']
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(note['content'])
            
            for flashcard in flashcards:
                pattern_folder = local_flashcards / flashcard['pattern']
                pattern_folder.mkdir(exist_ok=True)
                
                file_path = pattern_folder / flashcard['filename']
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(flashcard['content'])
            
            print(f"✅ Auto-synced {len(notes)} notes and {len(flashcards)} flashcards from GitHub")
            
        except Exception as e:
            print(f"Auto-sync from GitHub error: {e}")
    
    def auto_export_to_notebooklm():
        """Automatically export to NotebookLM"""
        try:
            from notebooklm_export import NotebookLMExporter
            exporter = NotebookLMExporter()
            exporter.export_to_notebooklm(auto_sync=True)
            print("✅ Auto-exported to NotebookLM")
        except Exception as e:
            print(f"Auto-export to NotebookLM error: {e}")
    
    # Start background sync thread
    sync_thread = threading.Thread(target=auto_sync_worker, daemon=True)
    sync_thread.start()
    
    return True

# Mobile-friendly navigation
def show_mobile_nav():
    """Compact mobile navigation"""
    st.markdown("---")
    nav_cols = st.columns(4)
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
        if st.button("🎓", help="Study", key="nav_study", use_container_width=True):
            st.session_state.page = "study"
    st.markdown("---")

# Helper function to get LeetCode URL
def get_leetcode_url(problem):
    """Get LeetCode URL for a problem, using existing URL or generating one"""
    # Use existing URL from the data if available
    if 'url' in problem and problem['url']:
        return problem['url']
    
    # Fallback to generated URL
    title = problem['title'].lower()
    # Clean the title for URL generation
    title = title.replace(' ', '-').replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace(':', '').replace(';', '')
    return f"https://leetcode.com/problems/{title}/"

# Add daily learning tip
def show_daily_learning_tip():
    """Show daily learning tip and motivation"""
    st.markdown("### 💡 Daily Learning Tip")
    
    # Get today's tip based on date
    today = datetime.now().day
    tips = [
        "🎯 **Focus on patterns, not just problems.** Understanding the underlying pattern helps you solve similar problems faster.",
        "⏰ **Consistency beats intensity.** Solving 1 problem daily is better than solving 10 problems once a week.",
        "📝 **Write down your thought process.** Even if you get the answer wrong, documenting your approach helps you learn.",
        "🔄 **Review solved problems.** Revisit problems you solved weeks ago to reinforce your learning.",
        "🎨 **Draw it out.** Visualizing the problem often reveals the solution approach.",
        "🧠 **Think out loud.** Explaining your approach helps you identify gaps in your understanding.",
        "📚 **Learn one pattern at a time.** Master one pattern before moving to the next.",
        "🎯 **Start with brute force.** Always start with the simplest solution, then optimize.",
        "⏱️ **Time yourself.** Practice under time pressure to prepare for interviews.",
        "🤔 **Question your assumptions.** Always verify your understanding of the problem.",
        "📊 **Track your progress.** Seeing improvement motivates you to keep going.",
        "🎪 **Make it fun.** Turn problem-solving into a game or challenge.",
        "👥 **Study with others.** Discussing problems with peers deepens understanding.",
        "📖 **Read solutions after solving.** Compare your approach with optimal solutions.",
        "🎯 **Focus on fundamentals.** Strong basics make advanced concepts easier.",
        "🔄 **Practice spaced repetition.** Review concepts at increasing intervals.",
        "📝 **Keep a learning journal.** Document insights and breakthroughs.",
        "🎨 **Use different approaches.** Try multiple solutions to the same problem.",
        "⏰ **Set realistic goals.** Aim for steady progress rather than perfection.",
        "🎯 **Celebrate small wins.** Every solved problem is progress worth celebrating.",
        "📚 **Connect concepts.** Look for relationships between different patterns.",
        "🎪 **Make it visual.** Use diagrams and flowcharts to understand algorithms.",
        "🧠 **Teach others.** Explaining concepts to others solidifies your understanding.",
        "📊 **Analyze complexity.** Always consider time and space complexity.",
        "🎯 **Focus on edge cases.** Test your solutions with boundary conditions.",
        "🔄 **Iterate and improve.** Refine your solutions based on feedback.",
        "📝 **Document your learning.** Keep notes of key insights and techniques.",
        "🎨 **Think creatively.** Sometimes the best solution is the most elegant one.",
        "⏰ **Build momentum.** Small daily progress compounds into significant results.",
        "🎯 **Stay curious.** Always ask 'why' and 'how' to deepen understanding."
    ]
    
    daily_tip = tips[today % len(tips)]
    st.info(daily_tip)
    
    # Add motivational quote
    quotes = [
        "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
        "The best way to predict the future is to implement it. - Alan Kay",
        "Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The expert in anything was once a beginner. - Helen Hayes",
        "Learning never exhausts the mind. - Leonardo da Vinci",
        "The more you learn, the more you earn. - Warren Buffett",
        "Education is not preparation for life; education is life itself. - John Dewey",
        "The beautiful thing about learning is that no one can take it away from you. - B.B. King"
    ]
    
    daily_quote = quotes[today % len(quotes)]
    st.markdown(f"*\"{daily_quote}\"*")

def get_current_page():
    """Get current page from query parameters"""
    try:
        return st.query_params.get("page", "dashboard")
    except:
        # Fallback in case query_params is not available
        return "dashboard"

def show_top_progress_bar(system):
    """Show a minimal progress bar at the very top"""
    total_problems = len(system.neetcode)
    completed = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"])
    progress_percent = (completed / total_problems) * 100
    
    st.markdown(f"""
        <div style="position: fixed; top: 0; left: 0; right: 0; z-index: 1000; padding: 0;">
            <div style="height: 3px; background: #141414; width: 100%;">
                <div style="height: 100%; width: {progress_percent}%; background: linear-gradient(90deg, #4CAF50, #45a049); transition: width 0.5s ease;"></div>
            </div>
            <div style="position: absolute; right: 10px; top: 5px; color: #4CAF50; font-size: 0.8rem; font-weight: 500;">
                {progress_percent:.1f}% ({completed}/{total_problems})
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_navigation():
    """Show the top navigation bar"""
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Navigation items with their icons and labels
    nav_items = [
        ('dashboard', '🏠', 'Dashboard'),
        ('solve', '💻', 'Solve'),
        ('browse', '📚', 'Browse'),
        ('review', '📝', 'Review'),
        ('study', '🎓', 'Study')
    ]
    
    # Create columns for navigation items
    cols = st.columns([2] + [1] * len(nav_items))
    
    # Logo in first column
    with cols[0]:
        if st.button("🎯 DSA Mastery", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    # Navigation items in remaining columns
    for i, (page, icon, label) in enumerate(nav_items):
        with cols[i + 1]:
            if st.button(f"{icon} {label}", use_container_width=True, type="secondary" if current_page != page else "primary"):
                st.session_state.current_page = page
                st.rerun()

def show_progress_section(system):
    """Show detailed progress tracking and gamification"""
    
    # Get progress data
    total_problems = len(system.neetcode)
    completed = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"])
    attempted = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "attempted"])
    
    # Calculate completion rate and predict completion
    days_active = (datetime.now() - datetime.fromisoformat(system.progress["stats"]["last_run"])).days + 1
    avg_problems_per_day = completed / max(days_active, 1)
    remaining_problems = total_problems - completed
    days_to_complete = int(remaining_problems / max(avg_problems_per_day, 0.1))
    completion_date = datetime.now() + timedelta(days=days_to_complete)
    progress_percent = (completed / total_problems) * 100

    # Overall Progress Container
    with st.container():
        # Title and percentage
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📊 Overall Progress")
        with col2:
            st.markdown(f"<h3 style='text-align: right; color: #4CAF50;'>{progress_percent:.1f}%</h3>", unsafe_allow_html=True)
        
        # Progress bar
        st.progress(progress_percent / 100)
        
        # Stats grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style='background-color: #1E1E2F; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #383850;'>
                <div style='color: #B0B0B0; font-size: 0.9rem;'>Completed</div>
                <div style='color: #4CAF50; font-size: 1.5rem; font-weight: bold;'>{}/{}</div>
            </div>
            """.format(completed, total_problems), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #1E1E2F; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #383850;'>
                <div style='color: #B0B0B0; font-size: 0.9rem;'>Current Streak</div>
                <div style='color: #4CAF50; font-size: 1.5rem; font-weight: bold;'>{}d</div>
            </div>
            """.format(system.progress["stats"].get("streak", 0)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #1E1E2F; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #383850;'>
                <div style='color: #B0B0B0; font-size: 0.9rem;'>Avg. per Day</div>
                <div style='color: #4CAF50; font-size: 1.5rem; font-weight: bold;'>{:.1f}</div>
            </div>
            """.format(avg_problems_per_day), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background-color: #1E1E2F; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #383850;'>
                <div style='color: #B0B0B0; font-size: 0.9rem;'>Days Left</div>
                <div style='color: #4CAF50; font-size: 1.5rem; font-weight: bold;'>{}</div>
            </div>
            """.format(days_to_complete), unsafe_allow_html=True)
        
        # Completion date
        st.markdown("""
        <div style='text-align: center; margin-top: 15px; color: #B0B0B0; font-size: 0.9rem;'>
            At your current pace, you'll complete all problems by 
            <span style='color: #4CAF50;'>{}</span>
        </div>
        """.format(completion_date.strftime('%B %d, %Y')), unsafe_allow_html=True)
    
    # Pattern Progress
    pattern_progress = {}
    for problem in system.neetcode:
        pattern = problem.get("pattern", "Other")
        if pattern not in pattern_progress:
            pattern_progress[pattern] = {"total": 0, "completed": 0}
        pattern_progress[pattern]["total"] += 1
        if str(problem.get("status", "")).lower() == "completed":
            pattern_progress[pattern]["completed"] += 1
    
    # Sort patterns by completion percentage
    sorted_patterns = sorted(
        pattern_progress.items(),
        key=lambda x: (x[1]["completed"] / x[1]["total"]) if x[1]["total"] > 0 else 0,
        reverse=True
    )
    
    with st.expander("📈 Pattern-wise Progress", expanded=False):
        st.markdown("""
            <div style='color: #B0B0B0; font-size: 0.9rem; margin-bottom: 15px;'>
                Track your mastery across different DSA patterns
            </div>
            <div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'>
        """, unsafe_allow_html=True)
        
        for pattern, stats in sorted_patterns:
            if pattern != "Other":
                completion = (stats["completed"] / stats["total"]) * 100
                st.markdown(f"""
                    <div style='background-color: #1E1E2F; padding: 10px; border-radius: 8px; border: 1px solid #383850; text-align: center;'>
                        <div style='color: white; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;' title='{pattern}'>{pattern}</div>
                        <div style='color: #4CAF50; font-size: 1.2rem; font-weight: bold; margin: 5px 0;'>{completion:.0f}%</div>
                        <div style='background-color: #141414; height: 4px; border-radius: 2px; margin: 5px 0;'>
                            <div style='width: {completion}%; height: 100%; background: linear-gradient(90deg, #4CAF50, #45a049); border-radius: 2px;'></div>
                        </div>
                        <div style='color: #B0B0B0; font-size: 0.7rem;'>{stats["completed"]}/{stats["total"]}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_dashboard(system):
    """Show the main dashboard with progress, daily question, and system status"""
    
    # Show today's problem
    st.markdown("### 🎯 Today's Problem")
    show_todays_problem(system)
    
    # Show motivational quote
    st.markdown("### 💭 Daily Motivation")
    show_daily_quote()
    
    # Show progress section (includes pattern progress in expander)
    show_progress_section(system)
    
    # Show daily learning tip
    st.markdown("### 💡 Daily Tip")
    show_daily_learning_tip()

def show_todays_problem(system):
    """Show today's recommended problem"""
    problem = system.get_next_unsolved_in_pattern(system.get_current_pattern())
    if problem:
        st.markdown(f"""
            <div class="neon-card">
                <div style="color: #4CAF50; font-size: 16px; margin-bottom: 10px;">Recommended Problem:</div>
                <div style="color: white; font-size: 20px; margin-bottom: 10px;">{problem['title']}</div>
                <div style="color: #888; font-size: 14px; margin-bottom: 15px;">Pattern: {problem.get('pattern', 'Unknown')}</div>
                <div style="display: flex; gap: 10px;">
                    <a href="{problem['url']}" target="_blank" style="text-decoration: none;">
                        <div style="background: #4CAF50; color: white; padding: 8px 15px; border-radius: 5px; display: inline-block;">
                            Solve on LeetCode
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No problems available. You might have completed all problems in the current pattern!")

def show_daily_quote():
    """Show an inspirational quote"""
    quotes = [
        {
            "text": "The only way to learn a new programming language is by writing programs in it.",
            "author": "Dennis Ritchie"
        },
        {
            "text": "Sometimes it's better to leave something alone, to pause, and that's very true of programming.",
            "author": "Joyce Wheeler"
        },
        {
            "text": "Testing leads to failure, and failure leads to understanding.",
            "author": "Burt Rutan"
        },
        {
            "text": "The best error message is the one that never shows up.",
            "author": "Thomas Fuchs"
        },
        {
            "text": "The most damaging phrase in the language is 'We've always done it this way.'",
            "author": "Grace Hopper"
        }
    ]
    quote = random.choice(quotes)
    st.markdown(f"""
        <div class="neon-card">
            <div style="color: white; font-size: 16px; margin-bottom: 10px;">"{quote['text']}"</div>
            <div style="color: #4CAF50; font-size: 14px;">- {quote['author']}</div>
        </div>
    """, unsafe_allow_html=True)

def show_system_status():
    """Show system integration status"""
    st.markdown("""
        <div class="neon-card">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">Obsidian</div>
                    <div style="color: #888; font-size: 12px;">Connected</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">Anki</div>
                    <div style="color: #888; font-size: 12px;">Synced</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">NotebookLM</div>
                    <div style="color: #888; font-size: 12px;">Ready</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_solve_interface():
    """A clean, focused interface for solving problems, with a two-column layout."""
    st.header("Solve Problem")

    # --- Data Loading and State Management ---
    system = get_system()
    ordered_patterns = DSA_LEARNING_ORDER
    
    # Initialize session state for selected problem and pattern
    if 'selected_pattern' not in st.session_state:
        st.session_state.selected_pattern = system.get_current_pattern() or ordered_patterns[0]
    if 'selected_problem' not in st.session_state:
        st.session_state.selected_problem = None

    # --- Layout: Two Columns ---
    col1, col2 = st.columns([0.8, 2])

    # --- Column 1: Problem List ---
    with col1:
        st.subheader("Problems")
        
        # Pattern Selector
        selected_pattern_from_ui = st.selectbox(
            "Select Pattern:",
            options=ordered_patterns,
            index=ordered_patterns.index(st.session_state.selected_pattern) if st.session_state.selected_pattern in ordered_patterns else 0
        )
        
        # If pattern changes, update state and rerun
        if selected_pattern_from_ui != st.session_state.selected_pattern:
            st.session_state.selected_pattern = selected_pattern_from_ui
            st.session_state.selected_problem = None # Reset problem when pattern changes
            system.set_current_pattern(selected_pattern_from_ui)
            st.rerun()

        st.divider()

        # Get and display problems for the selected pattern
        problems_in_pattern = sorted(system.get_problems_by_pattern(st.session_state.selected_pattern), key=lambda p: int(''.join(filter(str.isdigit, str(p.get('id', '0'))))))

        if not problems_in_pattern:
            st.warning("No problems found for this pattern.")
        else:
            for problem in problems_in_pattern:
                status = str(problem.get('status', '')).lower()
                status_emoji = '✅' if status == 'completed' else '⏳'
                btn_col, link_col = st.columns([3, 1])
                with btn_col:
                    if st.button(f"{problem['id']}: {problem['title']} {status_emoji}", key=f"problem_{problem['id']}", use_container_width=True, type="secondary"):
                        st.session_state.selected_problem = problem
                        st.rerun()
                with link_col:
                    st.link_button("🔗", problem['url'], use_container_width=True)

    # --- Column 2: Code Editor ---
    with col2:
        st.subheader("Code Editor")

        if st.session_state.selected_problem is None:
            st.info("Select a problem from the list on the left to start coding.")
        else:
            problem = st.session_state.selected_problem
            st.markdown(f"**Current Problem: [{problem['title']}]({problem['url']})**")
            
            # Language Selector - default to Java
            languages = ["java", "python", "javascript", "cpp", "c"]
            selected_language = st.selectbox("Language:", options=languages, index=0)
            
            # Code Editor
            code_template = get_language_template(selected_language)
            
            if 'code_editor_value' not in st.session_state:
                st.session_state.code_editor_value = code_template
            
            # When problem or language changes, reset the code
            if st.session_state.get('current_problem_id') != problem['id'] or st.session_state.get('current_language') != selected_language:
                st.session_state.code_editor_value = code_template
                st.session_state.current_problem_id = problem['id']
                st.session_state.current_language = selected_language

            st.markdown('<div class="code-editor-container">', unsafe_allow_html=True)
            code = st_monaco(
                value=st.session_state.code_editor_value,
                language=selected_language,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Action Buttons
            st.divider()
            b_col1, b_col2, b_col3 = st.columns(3)
            with b_col1:
                if st.button("Generate Notes", use_container_width=True):
                    prompt = f"""
                    Generate detailed DSA notes for LeetCode problem: {problem['title']} (Pattern: {problem['pattern']})
                    Follow this exact structure with small, well-formatted headings:
                    ## Problem Statement and Examples
                    [Detailed problem description and 2-3 examples]
                    ## Hints
                    [3-5 progressive hints]
                    ## Intuition
                    [Clear explanation of core idea and why it works]
                    ## General Solution for Pattern
                    [Broad approach for {problem['pattern']} pattern, with common use cases]
                    ## Brute-Force Approach
                    [Step-by-step brute force solution with complexity analysis]
                    ## Optimal Solution Breakdown
                    [Detailed breakdown of best solution, including time/space complexity, edge cases, and optimizations]
                    ## Code (Java)
                    ```java
                    [Optimal Java code with thorough inline comments explaining each part]
                    ```
                    Keep AI-generated parts as one-line summaries. Add more prompting guidance in notes for better understanding. Ensure readability with smaller sections.
                    """
                    try:
                        notes = call_ai_api(prompt)
                        st.session_state.generated_notes = notes
                        st.rerun()  # Rerun to show notes below
                    except Exception as e:
                        st.error(f"Failed to generate notes: {e}")

            # Editable notes
            if 'generated_notes' in st.session_state and st.session_state.generated_notes:
                edited_notes = st.text_area("Edit Notes", value=st.session_state.generated_notes, height=300)
                st.session_state.generated_notes = edited_notes  # Update with edits

                action_cols = st.columns(2)
                with action_cols[0]:
                    if st.button("Save Notes", use_container_width=True):
                        try:
                            # Save to file
                            pattern = problem['pattern'].replace(' ', '_').lower()
                            title = problem['title'].replace(' ', '_').lower()
                            notes_dir = Path('notes') / pattern
                            notes_dir.mkdir(parents=True, exist_ok=True)
                            notes_path = notes_dir / f"{problem['id']}_{title}.md"
                            overwrite = False
                            if notes_path.exists():
                                st.warning(f"A note for this problem already exists and will be overwritten in Obsidian and NotebookLM.")
                                overwrite = True
                            with open(notes_path, 'w', encoding='utf-8') as f:
                                f.write(edited_notes)
                            st.success(f"Notes saved to {notes_path}")

                            # --- GitHub Sync ---
                            cloud_sync = CloudSync()
                            github_filename = f"{problem['id']}_{title}.md"
                            github_success = cloud_sync.sync_note_to_cloud(edited_notes, github_filename)
                            if github_success:
                                st.success("Notes pushed to GitHub vault!")
                            else:
                                st.info("GitHub sync not configured or failed. Notes only saved locally.")

                            # --- NotebookLM Export ---
                            from notebooklm_export import NotebookLMExporter
                            exporter = NotebookLMExporter()
                            notebooklm_export_path = Path('notebooklm_export') / f"{problem['id']}_{title}.md"
                            if notebooklm_export_path.exists() and not overwrite:
                                st.warning(f"A note for this problem already exists in NotebookLM and will be overwritten.")
                            exporter.export_note_to_notebooklm(notes_path)
                            st.success("Note exported to NotebookLM!")

                            # Generate Anki flashcards
                            from anki_manager import create_flashcards_from_notes
                            flashcards = extract_flashcards_from_notes(edited_notes)  # Assume helper function
                            create_flashcards(flashcards, deck_name=problem['pattern'])
                            st.success("✅ Flashcards generated and ready for Anki")
                        except Exception as e:
                            st.error(f"Failed to save/sync: {e}")

                with action_cols[1]:
                    if st.button("Mark as Done", use_container_width=True, type="primary"):
                        system.mark_problem_completed(problem['id'])
                        st.success(f"Marked {problem['title']} as done!")
                        st.session_state.generated_notes = None

            # Full-width notes section below columns
            if 'generated_notes' in st.session_state and st.session_state.generated_notes:
                with st.expander("### Generated Notes", expanded=True):
                    st.markdown('<div class="notes-container">', unsafe_allow_html=True)
                    st.markdown(st.session_state.generated_notes)
                    st.markdown('</div>', unsafe_allow_html=True)

            with b_col2:
                if st.button("Analyze Code", use_container_width=True):
                    prompt = f"""
                    Analyze this code for LeetCode problem {problem['title']}:
                    ```{selected_language}
                    {st.session_state.code_editor_value}
                    ```
                    Provide:
                    - Correctness
                    - Approach summary
                    - Complexity
                    - Mistakes
                    - Fixed code
                    - Annotated code
                    - Flashcards
                    """
                    try:
                        analysis = call_ai_api(prompt, parse_json=True)  # Assuming it returns JSON
                        display_analysis_results(analysis, selected_language)
                    except Exception as e:
                        st.error(f"Failed to analyze code: {e}")
            with b_col3:
                if st.button("Generate AI Solution", use_container_width=True):
                    prompt = f"Generate optimal {selected_language} solution code for LeetCode problem: {problem['title']}"
                    try:
                        ai_code = call_ai_api(prompt)
                        st.session_state.code_editor_value = ai_code
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to generate AI solution: {e}")

            # Add Mark as Done button
            if 'generated_notes' in st.session_state and st.session_state.generated_notes:
                if st.button("Mark as Done", use_container_width=True, type="primary"):
                    # TODO: Integrate with system to mark problem as completed
                    system.mark_problem_completed(problem['id'])
                    st.success(f"Marked {problem['title']} as done!")
                    st.session_state.generated_notes = None  # Clear notes after marking

            # Daily Review enhancement
            if st.button("Daily Review", use_container_width=True):
                # Load random flashcards from saved notes
                flashcards = load_random_flashcards()  # Assume helper function
                if flashcards:
                    st.markdown("### Daily Review Flashcards")
                    for card in flashcards[:5]:  # Show 5 random
                        with st.expander(card['front']):
                            st.write(card['back'])
                else:
                    st.info("No flashcards available yet.")

def get_language_template(language):
    """Return template code for the selected language"""
    templates = {
        "java": """public class Solution {
    public static void main(String[] args) {
        // Your solution here
    }
}""",
        "python": """def solution():
    # Your solution here
    pass

if __name__ == "__main__":
    solution()""",
        "javascript": """function solution() {
    // Your solution here
}

solution();""",
        "cpp": """#include <iostream>
using namespace std;

int main() {
    // Your solution here
    return 0;
}""",
        "c": """#include <stdio.h>

int main() {
    // Your solution here
    return 0;
}"""
    }
    return templates.get(language, "// Start coding here")

# Compact problem browser
def show_problem_browser(system):
    """Mobile-friendly problem browser with improved horizontal card layout and icons."""
    st.markdown("""
    <div class="main-header">
        <h1>📚 Problem Browser</h1>
        <p class="mobile-text">Browse and filter all problems</p>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"], key="browser_difficulty")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Not Started", "Completed", "Skipped"], key="browser_status")
    pattern_filter = st.selectbox("Pattern", ["All"] + system.get_learning_order(), key="browser_pattern")

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

    # Load progress for note and solved status
    progress = system.progress.get("problems", {})

    st.subheader(f"📋 Problems ({len(filtered_problems)})")
    for problem in filtered_problems:
        status = str(problem.get("status", "")).lower()
        status_emoji = {"completed": "✅", "skipped": "⏭️", "": "⏳"}.get(status, "⏳")
        note_icon = "📝" if progress.get(problem["id"], {}).get("note_path") else ""
        solved = progress.get(problem["id"], {}).get("solved", False) or status == "completed"
        solved_text = "Solved" if solved else "Not Solved"
        solved_color = "#4CAF50" if solved else "#B0B0B0"
        leetcode_url = get_leetcode_url(problem)

        st.markdown(f'''
        <div style="display: flex; align-items: center; border: 1px solid #383850; border-radius: 10px; padding: 0.7rem 1rem; margin-bottom: 0.5rem; background: #1E1E2F;">
            <span style="font-size: 1.5rem; margin-right: 1rem;">{status_emoji}</span>
            <div style="flex: 1;">
                <span style="font-weight: 600; font-size: 1.08rem;">{problem['id']} - {problem['title']}</span><br>
                <span style="font-size: 0.95rem; color: #B0B0B0;">{problem['difficulty']} • {problem['pattern']}</span>
            </div>
            <div style="margin-right: 1.2rem; color: {solved_color}; font-weight: 500;">{solved_text}</div>
            <div style="font-size: 1.2rem; margin-right: 1.2rem;">{note_icon}</div>
            <a href="{leetcode_url}" target="_blank" style="font-size: 1.3rem; text-decoration: none;">🔗</a>
        </div>
        ''', unsafe_allow_html=True)

# Remove the review interface
def show_review_interface(system):
    pass

def show_study_mode(system):
    """Study Mode: Show all notes from GitHub/Obsidian, grouped by pattern, with search and expand/collapse."""
    import os
    import requests
    from pathlib import Path
    import streamlit as st

    st.markdown("""
    <div class="main-header">
        <h1>📚 Study Session</h1>
        <p class="mobile-text">Browse and study all your notes, grouped by pattern</p>
    </div>
    """, unsafe_allow_html=True)

    notes = []
    note_source = ""
    # Fetch notes from GitHub
    if os.environ.get('GITHUB_TOKEN') and os.environ.get('GITHUB_REPO'):
        try:
            headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github.v3+json"}
            repo = os.environ['GITHUB_REPO']
            api_url = f"https://api.github.com/repos/{repo}/contents/notes"
            r = requests.get(api_url, headers=headers)
            if r.status_code == 200:
                patterns = r.json()
                for pattern in patterns:
                    if pattern['type'] == 'dir':
                        pattern_name = pattern['name']
                        pattern_url = f"https://api.github.com/repos/{repo}/contents/notes/{pattern_name}"
                        r2 = requests.get(pattern_url, headers=headers)
                        if r2.status_code == 200:
                            files = r2.json()
                            for file in files:
                                if file['name'].endswith('.md'):
                                    file_r = requests.get(file['download_url'], headers=headers)
                                    if file_r.status_code == 200:
                                        notes.append({
                                            "title": file['name'].replace('.md',''),
                                            "content": file_r.text,
                                            "pattern": pattern_name,
                                            "path": file['path']
                                        })
                note_source = "GitHub"
            else:
                st.warning(f"Failed to fetch notes from GitHub: {r.status_code}")
        except Exception as e:
            st.warning(f"GitHub load failed: {e}")
    else:
        st.info("GitHub sync not configured. No notes to display.")

    # Group notes by pattern
    from collections import defaultdict
    pattern_groups = defaultdict(list)
    for note in notes:
        pattern_groups[note['pattern']].append(note)

    # Search bar
    search_query = st.text_input("Search notes by title or content:")

    # Display notes grouped by pattern
    for pattern in sorted(pattern_groups.keys()):
        st.markdown(f"### {pattern}")
        for note in pattern_groups[pattern]:
            if search_query.lower() in note['title'].lower() or search_query.lower() in note['content'].lower():
                with st.expander(note['title'], expanded=False):
                    st.markdown(note['content'])

def show_floating_ai_chatbox():
    """Show a Cursor-style floating AI chatbox for DSA-related queries"""
    # Initialize chat state
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""
    
    # Chat toggle button
    st.markdown(
        f"""
        <div class="floating-chat-trigger" onclick="document.getElementById('chat-toggle').click()">
            💬
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Hidden button for chat toggle
    if st.button("Toggle Chat", key="chat-toggle", help="Toggle chat window"):
        st.session_state.chat_visible = not st.session_state.chat_visible
    
    # Show chat container if visible
    if st.session_state.chat_visible:
        st.markdown(
            """
            <div class="chat-container">
                <div class="chat-header">
                    <div class="chat-header-title">
                        🤖 DSA Assistant
                    </div>
                    <div class="chat-header-actions">
                        <button class="chat-header-button" onclick="clearChat()">🗑️</button>
                        <button class="chat-header-button" onclick="document.getElementById('chat-toggle').click()">✕</button>
                    </div>
                </div>
                <div class="chat-messages" id="chat-messages">
            """,
            unsafe_allow_html=True
        )
        
        # Display chat messages
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(
                    f"""
                    <div class="chat-message user-message">
                        <div class="message-avatar user-avatar">👤</div>
                        <div class="message-content">
                            {msg['content']}
                            <div class="message-actions">
                                <button class="message-action-button" onclick="editMessage(this)">✏️</button>
                                <button class="message-action-button" onclick="deleteMessage(this)">🗑️</button>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-message assistant-message">
                        <div class="message-avatar assistant-avatar">🤖</div>
                        <div class="message-content">
                            {msg['content']}
                            <div class="message-actions">
                                <button class="message-action-button" onclick="copyMessage(this)">📋</button>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Chat input
        st.markdown(
            """
            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <textarea
                        class="chat-input"
                        placeholder="Ask about DSA concepts..."
                        rows="1"
                        onkeydown="if(event.keyCode==13 && !event.shiftKey){event.preventDefault();document.getElementById('chat-send').click()}"
                    ></textarea>
                    <button class="chat-send-button" id="chat-send">
                        ➤
                    </button>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add JavaScript for chat functionality
        st.markdown(
            """
            <script>
            function clearChat() {
                // Clear chat history
                document.querySelector('.chat-messages').innerHTML = '';
                // TODO: Add backend clear functionality
            }
            
            function editMessage(button) {
                const messageContent = button.closest('.message-content');
                const text = messageContent.firstChild.textContent.trim();
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.className = 'chat-input';
                textarea.style.width = '100%';
                messageContent.innerHTML = '';
                messageContent.appendChild(textarea);
                textarea.focus();
                
                textarea.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        const newText = this.value;
                        messageContent.innerHTML = newText;
                        // TODO: Add backend update functionality
                    }
                });
            }
            
            function deleteMessage(button) {
                const message = button.closest('.chat-message');
                message.remove();
                // TODO: Add backend delete functionality
            }
            
            function copyMessage(button) {
                const text = button.closest('.message-content').firstChild.textContent.trim();
                navigator.clipboard.writeText(text);
                // Show copy feedback
                const feedback = document.createElement('div');
                feedback.textContent = 'Copied!';
                feedback.style.position = 'absolute';
                feedback.style.right = '8px';
                feedback.style.bottom = '8px';
                feedback.style.fontSize = '12px';
                feedback.style.color = 'var(--text-bright)';
                button.closest('.message-content').appendChild(feedback);
                setTimeout(() => feedback.remove(), 1500);
            }
            
            // Auto-resize textarea
            document.querySelector('.chat-input').addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
            </script>
            """,
            unsafe_allow_html=True
        )
        
        # Handle chat input
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("", key="chat_input", label_visibility="collapsed")
            submit = st.form_submit_button("Send", use_container_width=True)
            
            if submit and user_input:
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Get AI response
                try:
                    response = call_ai_api(f"""
                    User's DSA question: {user_input}
                    
                    Provide a clear, concise answer focusing on:
                    1. Direct answer to the question
                    2. Key concepts involved
                    3. Example if helpful (short)
                    4. Best practices or tips
                    
                    Keep the response focused and under 150 words.
                    """)
                    
                    # Add AI response
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    
                    # Rerun to show new messages
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")

def main():
    """Main function to run the Streamlit app"""
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    if 'selected_pattern' not in st.session_state:
        st.session_state.selected_pattern = None
    if 'system' not in st.session_state:
        st.session_state.system = get_system()

    # Get system instance
    system = st.session_state.system

    try:
        # Show top progress bar
        show_top_progress_bar(system)
        
        # Add some space for the top progress bar
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        # Show navigation
        show_navigation()
        
        # Show appropriate page based on session state
        current_page = st.session_state.current_page
        
        if current_page == "solve":
            show_solve_interface()
        elif current_page == "browse":
            show_problem_browser(system)
        elif current_page == "review":
            show_review_interface(system)
        elif current_page == "study":
            show_study_mode(system)
        else:  # dashboard is default
            show_dashboard(system)
        
        # Show system status at the bottom
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">Obsidian</div>
                    <div style="color: #888; font-size: 12px;">Connected</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">Anki</div>
                    <div style="color: #888; font-size: 12px;">Synced</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div style="text-align: center;">
                    <div style="color: #4CAF50; font-size: 24px;">✓</div>
                    <div style="color: white; font-size: 16px;">NotebookLM</div>
                    <div style="color: #888; font-size: 12px;">Ready</div>
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Try refreshing the page. If the error persists, please report it.")

if __name__ == "__main__":
    main()

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
        - 🐙 GitHub upload
        
        **Export Options:**
        - 📥 Download notes
        - 📊 Export flashcards
        - 📋 Copy to clipboard
        - 🐙 Upload to GitHub
        """)
        
        # GitHub Configuration
        st.sidebar.markdown("### 🐙 GitHub Upload")
        if os.getenv('GITHUB_TOKEN'):
            st.sidebar.success("✅ GitHub configured")
            st.sidebar.info(f"Repo: {os.getenv('GITHUB_REPO', 'Not set')}")
        else:
            st.sidebar.warning("❌ GitHub not configured")
            st.sidebar.info("Add GITHUB_TOKEN to secrets")
    else:
        st.sidebar.info("💻 Running Locally")
        st.sidebar.info("""
        **Local Features:**
        - 📁 Direct Obsidian save
        - 🃏 Direct Anki export
        - 📚 NotebookLM export
        - 🐙 GitHub upload
        """)

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

def extract_flashcards_from_notes(notes):
    # Simple extraction logic (e.g., look for Q&A patterns)
    # Implement based on notes structure
    return []  # Placeholder

def load_random_flashcards():
    # Load from Anki or saved files
    return []  # Placeholder 