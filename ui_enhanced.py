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

# Add improved problem card CSS at the top (after other CSS)
st.markdown('''
<style>
.problem-card {
    background: #f7f7fa !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(102,126,234,0.07);
    border: 1px solid #e0e0e0 !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    font-size: 1rem !important;
    color: #222 !important;
    transition: box-shadow 0.2s;
}
.problem-card a { color: #5a67d8 !important; text-decoration: underline; }
@media (max-width: 600px) {
    .problem-card { font-size: 0.98rem !important; padding: 0.7rem !important; }
}
</style>
''', unsafe_allow_html=True)

# Add improved button and header CSS at the top (after other CSS)
st.markdown('''
<style>
.accent-btn {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    margin: 0.2rem 0.1rem !important;
    box-shadow: 0 2px 8px rgba(102,126,234,0.07);
    transition: background 0.2s, box-shadow 0.2s;
}
.accent-btn:hover {
    background: linear-gradient(90deg, #764ba2 0%, #667eea 100%) !important;
    box-shadow: 0 4px 16px rgba(102,126,234,0.13);
}
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
    color: #5a67d8;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-subtext {
    font-size: 0.98rem;
    color: #666;
    margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
    .accent-btn { font-size: 1rem !important; padding: 0.5rem 0.7rem !important; }
    .section-header { font-size: 1.08rem; }
}
</style>
''', unsafe_allow_html=True)

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

# Add learning motivation features
def show_learning_motivation(system):
    """Show learning motivation and achievements"""
    st.markdown("### 🏆 Learning Motivation")
    
    try:
        # Calculate streak and achievements
        all_problems = system.get_all_problems()
        completed_problems = [p for p in all_problems if str(p.get("status", "")).lower() == "completed"]
        total_completed = len(completed_problems)
        
        # Daily streak calculation
        today = datetime.now().date()
        recent_completions = []
        for problem in completed_problems:
            # Handle different possible date formats and structures
            completion_date = None
            if isinstance(problem, dict):
                if 'completed_date' in problem:
                    try:
                        completion_date = datetime.strptime(problem['completed_date'], '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        continue
                elif hasattr(problem, 'completed_date'):
                    try:
                        completion_date = datetime.strptime(problem.completed_date, '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        continue
            
            if completion_date and (today - completion_date).days <= 7:
                recent_completions.append(completion_date)
        
        streak = 0
        current_date = today
        while current_date in recent_completions:
            streak += 1
            current_date -= timedelta(days=1)
        
        # Display motivation metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔥 Daily Streak", f"{streak} days")
            if streak >= 7:
                st.success("🎉 Week streak achieved!")
            elif streak >= 3:
                st.info("💪 Keep going!")
        
        with col2:
            st.metric("✅ Problems Solved", total_completed)
            if total_completed >= 50:
                st.success("🏆 50 problems milestone!")
            elif total_completed >= 25:
                st.info("🎯 Halfway to 50!")
        
        with col3:
            # Safely extract patterns
            patterns = set()
            for p in completed_problems:
                if isinstance(p, dict) and 'pattern' in p:
                    patterns.add(p['pattern'])
                elif hasattr(p, 'pattern'):
                    patterns.add(p.pattern)
            
            patterns_mastered = len(patterns)
            st.metric("📚 Patterns Mastered", patterns_mastered)
            if patterns_mastered >= 5:
                st.success("🌟 Pattern master!")
            elif patterns_mastered >= 3:
                st.info("📖 Learning well!")
        
        # Achievement badges
        st.markdown("#### 🏅 Achievements")
        achievements = []
        
        if total_completed >= 10:
            achievements.append("🥉 Bronze Solver (10 problems)")
        if total_completed >= 25:
            achievements.append("🥈 Silver Solver (25 problems)")
        if total_completed >= 50:
            achievements.append("🥇 Gold Solver (50 problems)")
        if total_completed >= 100:
            achievements.append("💎 Diamond Solver (100 problems)")
        
        if streak >= 3:
            achievements.append("🔥 3-Day Streak")
        if streak >= 7:
            achievements.append("🔥 7-Day Streak")
        if streak >= 30:
            achievements.append("🔥 30-Day Streak")
        
        if patterns_mastered >= 3:
            achievements.append("📚 Pattern Learner")
        if patterns_mastered >= 5:
            achievements.append("📚 Pattern Master")
        
        # Display achievements
        if achievements:
            for achievement in achievements:
                st.success(f"✅ {achievement}")
        else:
            st.info("🎯 Start solving problems to earn achievements!")
        
        # Study reminder
        if streak == 0:
            st.warning("💡 Don't break your streak! Solve a problem today!")
        elif streak >= 1:
            st.success(f"🔥 Amazing! {streak}-day streak! Keep it up!")
    
    except Exception as e:
        st.error(f"Error loading learning motivation: {str(e)}")
        st.info("🎯 Start solving problems to see your progress!")

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

# Add this to the dashboard after learning motivation
def show_dashboard(system):
    """Mobile-friendly dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 DSA Mastery Dashboard</h1>
        <p class="mobile-text">Track your progress and start solving</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Learning motivation
    show_learning_motivation(system)
    
    # Daily learning tip
    show_daily_learning_tip()
    
    # PC Auto-Sync Status
    if not os.environ.get('STREAMLIT_SERVER_HEADLESS', False):
        st.markdown("### 💻 PC Auto-Sync Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Check if local folders exist
            local_notes = Path("local_notes")
            local_flashcards = Path("local_flashcards")
            notebooklm_export = Path("notebooklm_export")
            
            if local_notes.exists():
                note_count = len(list(local_notes.rglob("*.md")))
                st.metric("📝 Local Notes", f"{note_count} files")
            else:
                st.metric("📝 Local Notes", "Not synced")
        
        with col2:
            if local_flashcards.exists():
                flashcard_count = len(list(local_flashcards.rglob("*.csv")))
                st.metric("📊 Local Flashcards", f"{flashcard_count} files")
            else:
                st.metric("📊 Local Flashcards", "Not synced")
        
        with col3:
            if notebooklm_export.exists():
                notebooklm_count = len(list(notebooklm_export.rglob("*.md")))
                st.metric("📚 NotebookLM Export", f"{notebooklm_count} files")
            else:
                st.metric("📚 NotebookLM Export", "Not synced")
        
        # Auto-sync info
        st.info("""
        **🔄 PC Auto-Sync Active**
        - Automatically syncs from GitHub every 5 minutes
        - Updates local notes and flashcards
        - Exports to NotebookLM format
        - No manual intervention required
        """)
        
        # NotebookLM Integration Status
        st.markdown("### 📚 NotebookLM Integration Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Google Drive sync
            if os.getenv('GDRIVE_FOLDER_ID'):
                st.metric("☁️ Google Drive", "✅ Active")
            else:
                st.metric("☁️ Google Drive", "❌ Not configured")
        
        with col2:
            # Webhook sync
            if os.getenv('NOTEBOOKLM_WEBHOOK_URL'):
                st.metric("🔗 Webhook", "✅ Active")
            else:
                st.metric("🔗 Webhook", "❌ Not configured")
        
        with col3:
            # Local folder sync
            st.metric("📁 Local Folder", "✅ Active")
        
        with col4:
            # API sync
            if os.getenv('NOTEBOOKLM_API_KEY'):
                st.metric("🔌 API", "✅ Active")
            else:
                st.metric("🔌 API", "❌ Not configured")
        
        # NotebookLM auto-sync info
        st.success("""
        **📚 NotebookLM Zero-Manual Integration Active**
        - File watcher monitoring notebooklm_export folder
        - Auto-uploading to all configured sync methods
        - Real-time sync with zero manual work
        - NotebookLM automatically has your notes!
        """)
    
    st.markdown('<div class="section-header">📅 Today’s Problem</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtext">Solve today’s recommended problem to keep your streak going!</div>', unsafe_allow_html=True)
    # Today's problem
    today_problem = system.get_today_problem()
    if today_problem:
        pattern, problem = today_problem
        st.subheader(f"📅 Today's Problem")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            # Use helper function to get LeetCode URL
            leetcode_url = get_leetcode_url(problem)
            
            st.markdown(f"""
            <div class="problem-card">
                <strong style='font-size:1.1rem'>{problem['id']} - {problem['title']}</strong><br>
                <small>Pattern: <b>{pattern}</b> | Difficulty: <b>{problem['difficulty']}</b></small><br>
                <a href="{leetcode_url}" target="_blank">🔗 Solve on LeetCode</a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🚀 Start Solving Now", key="start_today", use_container_width=True, help="Go to solve tab", type="primary"):
                st.session_state.page = "solve"
                st.session_state.current_problem = problem
                st.rerun()
    
    st.markdown('<div class="section-header">📊 Progress Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtext">Track your DSA journey and see your achievements at a glance.</div>', unsafe_allow_html=True)
    # Progress overview
    
    # Get progress data - handle case where get_all_problems might not exist
    try:
        all_problems = system.get_all_problems()
        total_problems = len(all_problems)
        completed = len([p for p in all_problems if str(p.get("status", "")).lower() == "completed"])
        skipped = len([p for p in all_problems if str(p.get("status", "")).lower() == "skipped"])
    except AttributeError:
        # Fallback to neetcode attribute if get_all_problems doesn't exist
        all_problems = system.neetcode
        total_problems = len(all_problems)
        completed = len([p for p in all_problems if str(p.get("status", "")).lower() == "completed"])
        skipped = len([p for p in all_problems if str(p.get("status", "")).lower() == "skipped"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Problems", total_problems)
    with col2:
        st.metric("Completed", completed)
    with col3:
        st.metric("Skipped", skipped)
    
    # Progress bar
    progress = (completed / total_problems * 100) if total_problems > 0 else 0
    st.progress(progress / 100)
    st.caption(f"Overall Progress: {progress:.1f}%")
    
    st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    # Quick actions
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Solve Problems", key="quick_solve", use_container_width=True, help="Practice new problems", type="primary"):
            st.session_state.page = "solve"
            st.rerun()
    with col2:
        if st.button("📚 Study All Notes", key="quick_study", use_container_width=True, help="Review all notes", type="primary"):
            st.session_state.page = "study"
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Browse Problems", key="quick_browse", use_container_width=True, help="Browse all problems", type="primary"):
            st.session_state.page = "browser"
            st.rerun()
    with col2:
        if st.button("📖 Review Notes", key="quick_review", use_container_width=True, help="Review your notes", type="primary"):
            st.session_state.page = "review"
            st.rerun()

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
    if not today_problem or not (isinstance(today_problem, dict) and today_problem.get("pattern") == selected_pattern):
        st.warning("No problem loaded for this pattern. Click below to load today's problem.")
        if st.button("🔄 Load Today's Problem", key="load_today_problem", use_container_width=True):
            st.session_state.page = "solve"
            st.session_state.current_problem = None
            st.rerun()
        return
    
    st.subheader(f"🎯 {today_problem['id']} - {today_problem['title']}")
    st.markdown(f"**{today_problem['difficulty']}** • {today_problem['pattern']}")
    
    # Add LeetCode link using helper function
    leetcode_url = get_leetcode_url(today_problem)
    st.markdown(f"[🔗 Solve on LeetCode]({leetcode_url})")
    
    # Compact problem description
    with st.expander("📝 Problem Description", expanded=False):
        st.markdown(today_problem.get("description", "No description available"))
    
    # Clear code paste label
    st.subheader("💻 Paste your code here")
    user_code = st.text_area("Paste your code here:", value=st.session_state.get("user_code", ""), 
                            height=200, key="code_input", 
                            placeholder="Paste or write your solution here...")
    st.session_state.user_code = user_code
    
    # Action buttons: Explain Solution and Submit Solution
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Explain Solution", key="explain_solution", use_container_width=True):
            if user_code.strip():
                with st.spinner("Analyzing and explaining your solution..."):
                    analysis = system.analyze_solution(today_problem, user_code)
                    st.session_state.analysis = analysis
                    st.session_state.code_explanation = generate_code_explanation(today_problem, user_code, "python")
            else:
                st.warning("Please paste or write your code first.")
    with col2:
        if st.button("✅ Submit Solution", key="submit_solution", use_container_width=True):
            if user_code.strip():
                system.mark_problem_status(today_problem["id"], "completed")
                st.success("Problem marked as completed!")
                st.rerun()
            else:
                st.warning("Please paste or write your code first.")
    
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
            
            # Mobile download buttons
            st.markdown("---")
            st.markdown("#### 📱 Mobile Downloads")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Download Note", key=f"download_note_{today_problem['id']}", use_container_width=True):
                    try:
                        import base64
                        b64 = base64.b64encode(note_md.encode()).decode()
                        href = f'<a href="data:file/md;base64,{b64}" download="{today_problem["title"].replace(" ", "_")}.md">📥 Download Note</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.success("✅ Note ready for download!")
                    except Exception as e:
                        st.error(f"Download error: {e}")
            
            with col2:
                if st.button("📊 Export Flashcards", key=f"export_flashcards_{today_problem['id']}", use_container_width=True):
                    try:
                        import pandas as pd
                        df = pd.DataFrame(flashcards)
                        csv = df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="{today_problem["title"].replace(" ", "_")}_flashcards.csv">📊 Download Flashcards</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.success("✅ Flashcards ready for download!")
                    except Exception as e:
                        st.error(f"Export error: {e}")
            
            with col3:
                if st.button("📋 Copy to Clipboard", key=f"copy_note_{today_problem['id']}", use_container_width=True):
                    try:
                        st.code(note_md)
                        st.success("✅ Note copied! Paste into Obsidian on PC")
                    except Exception as e:
                        st.error(f"Copy error: {e}")
            
            # Cloud upload buttons
            st.markdown("#### ☁️ Direct Cloud Upload")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🐙 Upload to GitHub", key=f"github_upload_{today_problem['id']}", use_container_width=True):
                    try:
                        from cloud_sync import CloudSync
                        cloud_sync = CloudSync()
                        filename = f"{today_problem['id']} - {today_problem['title']}.md"
                        success, message = cloud_sync.upload_note_to_github(note_md, filename, today_problem['pattern'])
                        if success:
                            st.success(message)
                        else:
                            st.warning(f"GitHub upload: {message}")
                    except Exception as e:
                        st.error(f"GitHub upload error: {e}")
            
            with col2:
                if st.button("📊 Upload Flashcards", key=f"upload_flashcards_{today_problem['id']}", use_container_width=True):
                    try:
                        from cloud_sync import CloudSync
                        cloud_sync = CloudSync()
                        filename = f"{today_problem['id']} - {today_problem['title']}_flashcards.csv"
                        success, message = cloud_sync.upload_flashcards_to_github(flashcards, filename, today_problem['title'])
                        if success:
                            st.success(message)
                        else:
                            st.warning(f"Flashcard upload: {message}")
                    except Exception as e:
                        st.error(f"Flashcard upload error: {e}")
            
            # NotebookLM Export
            st.markdown("#### 📚 NotebookLM Export")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📚 Export to NotebookLM", key=f"notebooklm_export_{today_problem['id']}", use_container_width=True):
                    try:
                        from notebooklm_export import NotebookLMExporter
                        exporter = NotebookLMExporter()
                        notebooklm_content = exporter.parse_note_for_notebooklm(note_md, today_problem['pattern'], f"{today_problem['id']} - {today_problem['title']}.md")
                        
                        # Save to NotebookLM folder
                        output_path = Path("notebooklm_export") / f"{today_problem['pattern']}_{today_problem['id']} - {today_problem['title']}.md"
                        output_path.parent.mkdir(exist_ok=True)
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(notebooklm_content)
                        
                        st.success(f"✅ Exported to NotebookLM: {output_path}")
                    except Exception as e:
                        st.error(f"NotebookLM export error: {e}")
            
            with col2:
                if st.button("🔄 Auto-Sync All", key=f"auto_sync_{today_problem['id']}", use_container_width=True):
                    try:
                        # Upload to GitHub
                        from cloud_sync import CloudSync
                        cloud_sync = CloudSync()
                        filename = f"{today_problem['id']} - {today_problem['title']}.md"
                        note_success, note_message = cloud_sync.upload_note_to_github(note_md, filename, today_problem['pattern'])
                        # Upload flashcards
                        flashcard_filename = f"{today_problem['id']} - {today_problem['title']}_flashcards.csv"
                        flashcard_success, flashcard_message = cloud_sync.upload_flashcards_to_github(flashcards, flashcard_filename, today_problem['title'])
                        # Export to NotebookLM
                        from notebooklm_export import NotebookLMExporter
                        exporter = NotebookLMExporter()
                        notebooklm_content = exporter.parse_note_for_notebooklm(note_md, today_problem['pattern'], f"{today_problem['id']} - {today_problem['title']}.md")
                        output_path = Path("notebooklm_export") / f"{today_problem['pattern']}_{today_problem['id']} - {today_problem['title']}.md"
                        output_path.parent.mkdir(exist_ok=True)
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(notebooklm_content)
                        st.success("✅ Auto-sync complete!")
                    except Exception as e:
                        st.error(f"Auto-sync error: {e}")
        
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
        
        # Use helper function to get LeetCode URL
        leetcode_url = get_leetcode_url(problem)
        
        st.markdown(f"""
        <div class="problem-card">
            {status_emoji} <strong style='font-size:1.05rem'>{problem['id']} - {problem['title']}</strong><br>
            <small>{problem['difficulty']} • {problem['pattern']}</small><br>
            <a href="{leetcode_url}" target="_blank">🔗 Solve on LeetCode</a>
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

def show_study_mode(system):
    """Study Mode: Review all notes from Google Drive or GitHub, with sorting/filtering/search"""
    import os
    import glob
    import re
    import base64
    import requests
    from pathlib import Path
    import streamlit as st

    st.markdown("""
    <div class="main-header">
        <h1>📚 Study Mode</h1>
        <p class="mobile-text">Review, search, and study all your notes</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Load notes from Google Drive (preferred) or GitHub (fallback) ---
    notes = []
    note_source = ""
    # Try Google Drive first
    gdrive_folder = os.environ.get('GDRIVE_FOLDER_ID')
    gdrive_creds = os.environ.get('GDRIVE_CREDENTIALS')
    if gdrive_folder and gdrive_creds:
        try:
            from cloud_sync import CloudSync
            cloud_sync = CloudSync()
            notes = cloud_sync.list_notes_from_gdrive()
            note_source = "Google Drive"
        except Exception as e:
            st.warning(f"Google Drive load failed: {e}")
    # Fallback to local folder
    if not notes:
        local_notes = Path("local_notes")
        if local_notes.exists():
            for note_file in local_notes.rglob("*.md"):
                with open(note_file, "r", encoding="utf-8") as f:
                    notes.append({
                        "title": note_file.stem,
                        "content": f.read(),
                        "pattern": note_file.parent.name,
                        "path": str(note_file)
                    })
            note_source = "Local Folder"
    # Fallback to GitHub
    if not notes and os.environ.get('GITHUB_TOKEN') and os.environ.get('GITHUB_REPO'):
        try:
            headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github.v3+json"}
            repo = os.environ['GITHUB_REPO']
            api_url = f"https://api.github.com/repos/{repo}/contents/notes"
            r = requests.get(api_url, headers=headers)
            if r.status_code == 200:
                for file_info in r.json():
                    if file_info['name'].endswith('.md'):
                        file_url = file_info['download_url']
                        note_content = requests.get(file_url).text
                        notes.append({
                            "title": file_info['name'].replace('.md',''),
                            "content": note_content,
                            "pattern": file_info.get('path','').split('/')[-2] if '/' in file_info.get('path','') else '',
                            "path": file_info['path']
                        })
                note_source = "GitHub"
        except Exception as e:
            st.warning(f"GitHub load failed: {e}")

    if not notes:
        st.info("No notes found in Google Drive, local folder, or GitHub.")
        return

    # --- Sorting/filtering/search UI ---
    patterns = sorted(set(n.get('pattern','') for n in notes if n.get('pattern','')))
    pattern_filter = st.selectbox("Pattern", ["All"] + patterns, key="study_pattern")
    search_query = st.text_input("Search notes by title or content", key="study_search")
    sort_by = st.selectbox("Sort by", ["Title", "Pattern"], key="study_sort")

    filtered_notes = notes
    if pattern_filter != "All":
        filtered_notes = [n for n in filtered_notes if n.get('pattern','') == pattern_filter]
    if search_query:
        filtered_notes = [n for n in filtered_notes if search_query.lower() in n['title'].lower() or search_query.lower() in n['content'].lower()]
    if sort_by == "Title":
        filtered_notes = sorted(filtered_notes, key=lambda n: n['title'])
    elif sort_by == "Pattern":
        filtered_notes = sorted(filtered_notes, key=lambda n: n.get('pattern',''))

    st.markdown(f"**Source:** {note_source} | **Total Notes:** {len(filtered_notes)}")

    # --- Display notes ---
    for note in filtered_notes:
        with st.expander(f"📝 {note['title']} [{note.get('pattern','')}]", expanded=False):
            st.markdown(note['content'], unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                b64 = base64.b64encode(note['content'].encode()).decode()
                href = f'<a href="data:file/md;base64,{b64}" download="{note["title"].replace(" ", "_")}.md">📥 Download Note</a>'
                st.markdown(href, unsafe_allow_html=True)
            with col2:
                if st.button(f"📚 Export to NotebookLM", key=f"notebooklm_export_{note['title']}"):
                    try:
                        from notebooklm_export import NotebookLMExporter
                        exporter = NotebookLMExporter()
                        notebooklm_content = exporter.parse_note_for_notebooklm(note['content'], note.get('pattern',''), f"{note['title']}.md")
                        output_path = Path("notebooklm_export") / f"{note.get('pattern','')}_{note['title']}.md"
                        output_path.parent.mkdir(exist_ok=True)
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(notebooklm_content)
                        st.success(f"✅ Exported to NotebookLM: {output_path}")
                    except Exception as e:
                        st.error(f"NotebookLM export error: {e}")

# Floating AI Chatbox (persistent on all pages)
def show_floating_ai_chatbox():
    import streamlit as st
    from ai_client import call_ai_api
    import time
    
    # Use session state for chat history
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    if 'ai_chatbox_open' not in st.session_state:
        st.session_state.ai_chatbox_open = False
    
    # Floating chatbox CSS
    st.markdown('''
    <style>
    .floating-chatbox {
        position: fixed;
        bottom: 1.5rem;
        right: 1.5rem;
        width: 320px;
        max-width: 90vw;
        z-index: 9999;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.18);
        border: 1px solid #e0e0e0;
        font-size: 0.95rem;
        transition: box-shadow 0.2s;
    }
    .floating-chatbox-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        padding: 0.7rem 1rem;
        border-radius: 12px 12px 0 0;
        cursor: pointer;
        font-weight: bold;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .floating-chatbox-body {
        padding: 0.7rem 1rem 0.7rem 1rem;
        max-height: 300px;
        overflow-y: auto;
    }
    .floating-chatbox-input {
        padding: 0.7rem 1rem;
        border-top: 1px solid #eee;
        background: #fafaff;
        border-radius: 0 0 12px 12px;
    }
    .floating-chatbox-minimized {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        position: fixed;
        bottom: 1.5rem;
        right: 1.5rem;
        z-index: 9999;
        box-shadow: 0 2px 16px rgba(0,0,0,0.18);
        cursor: pointer;
    }
    @media (max-width: 600px) {
        .floating-chatbox { right: 0.5rem; bottom: 0.5rem; width: 98vw; }
        .floating-chatbox-minimized { right: 0.5rem; bottom: 0.5rem; }
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Minimized button
    if not st.session_state.ai_chatbox_open:
        st.markdown('''<div class="floating-chatbox-minimized" onclick="window.dispatchEvent(new Event('openChatbox'))">💬</div>''', unsafe_allow_html=True)
        st.markdown('''<script>window.addEventListener('openChatbox', function() { window.parent.postMessage({isChatboxOpen: true}, '*'); });</script>''', unsafe_allow_html=True)
        # Open button (Streamlit workaround)
        if st.button("💬", key="open_chatbox_btn", help="Open AI Chat", use_container_width=True):
            st.session_state.ai_chatbox_open = True
        return
    
    # Floating chatbox
    st.markdown('<div class="floating-chatbox">', unsafe_allow_html=True)
    st.markdown('''<div class="floating-chatbox-header" onclick="window.dispatchEvent(new Event('closeChatbox'))">🤖 AI Chat <span style="float:right; cursor:pointer;">✖️</span></div>''', unsafe_allow_html=True)
    st.markdown('''<script>window.addEventListener('closeChatbox', function() { window.parent.postMessage({isChatboxOpen: false}, '*'); });</script>''', unsafe_allow_html=True)
    if st.button("✖️", key="close_chatbox_btn", help="Close AI Chat", use_container_width=True):
        st.session_state.ai_chatbox_open = False
        st.stop()
    
    # Chat history
    st.markdown('<div class="floating-chatbox-body">', unsafe_allow_html=True)
    for msg in st.session_state.ai_chat_history[-10:]:
        if msg['role'] == 'user':
            st.markdown(f'<div style="margin-bottom:0.5rem;"><b>🧑‍💻 You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-bottom:0.5rem;"><b>🤖 AI:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input box
    st.markdown('<div class="floating-chatbox-input">', unsafe_allow_html=True)
    chat_input = st.text_input("Ask anything about DSA, code, or notes...", key="ai_chat_input", label_visibility="collapsed", placeholder="Type your question and press Enter...")
    if chat_input:
        st.session_state.ai_chat_history.append({'role': 'user', 'content': chat_input})
        with st.spinner("AI is thinking..."):
            try:
                ai_response = call_ai_api(chat_input)
            except Exception as e:
                ai_response = f"[Error: {e}]"
        st.session_state.ai_chat_history.append({'role': 'ai', 'content': ai_response})
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Update main function to use mobile navigation
def main():
    # Initialize session state first
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'user_code' not in st.session_state:
        st.session_state.user_code = ""
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'code_explanation' not in st.session_state:
        st.session_state.code_explanation = None
    if 'selected_pattern' not in st.session_state:
        # We'll initialize this after getting the system
        st.session_state.selected_pattern = None

    # Initialize system
    system = get_system()
    
    # Setup cloud sync
    cloud_sync = setup_cloud_sync()
    
    # Setup automatic PC sync
    if not os.environ.get('STREAMLIT_SERVER_HEADLESS', False):
        setup_auto_sync()
    
    # Initialize selected_pattern after system is loaded
    if st.session_state.selected_pattern is None:
        all_patterns = system.get_learning_order_patterns()
        st.session_state.selected_pattern = all_patterns[0] if all_patterns else None

    # Mobile navigation
    show_mobile_nav()
    
    # Display selected page
    if st.session_state.page == "dashboard":
        show_dashboard(system)
        show_floating_ai_chatbox()
    elif st.session_state.page == "solve":
        show_solve_interface(system)
        show_floating_ai_chatbox()
    elif st.session_state.page == "browser":
        show_problem_browser(system)
        show_floating_ai_chatbox()
    elif st.session_state.page == "review":
        show_review_interface(system)
        show_floating_ai_chatbox()
    elif st.session_state.page == "study":
        show_study_mode(system)
        show_floating_ai_chatbox()

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

if __name__ == "__main__":
    main() 