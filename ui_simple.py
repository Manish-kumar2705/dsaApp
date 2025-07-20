import streamlit as st
import json
import os
import time
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
from dsa_system import DSAMasterySystem
from config import *

# Page configuration
st.set_page_config(
    page_title="DSA Mastery System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown(f"""
<style>
    .main {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    
    .main-header {{
        background: linear-gradient(90deg, {THEME_COLOR}, {SECONDARY_COLOR});
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid {THEME_COLOR};
        margin-bottom: 1rem;
    }}
    
    .problem-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }}
    
    .problem-card:hover {{
        border-color: {THEME_COLOR};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, {THEME_COLOR}, {SECONDARY_COLOR});
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    .difficulty-badge {{
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }}
    
    .difficulty-easy {{
        background-color: #4CAF50;
        color: white;
    }}
    
    .difficulty-medium {{
        background-color: #FF9800;
        color: white;
    }}
    
    .difficulty-hard {{
        background-color: #F44336;
        color: white;
    }}
    
    .pattern-badge {{
        background: {THEME_COLOR};
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize system
@st.cache_resource
def get_system():
    return DSAMasterySystem()

system = get_system()

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <h2>🚀 DSA Mastery</h2>
            <p style="color: white; opacity: 0.8;">Your AI-powered study companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = st.selectbox(
            "Navigation",
            ["Dashboard", "Solve Problems", "Problem Browser", "Study Mode"],
            index=0
        )
    
    # Initialize session state
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
    if "user_code" not in st.session_state:
        st.session_state.user_code = ""
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    
    # Route to appropriate page
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Solve Problems":
        show_solve_interface()
    elif selected == "Problem Browser":
        show_problem_browser()
    elif selected == "Study Mode":
        show_study_mode()

def show_dashboard():
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Your DSA Progress Dashboard</h1>
        <p>Track your journey to DSA mastery</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall stats
    stats = system.progress["stats"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Problems Solved</h3>
            <h2>{stats['solved']}/{stats['total']}</h2>
            <p>{(stats['solved']/stats['total']*100):.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Current Streak</h3>
            <h2>{stats['streak']} days</h2>
            <p>Keep it up!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 Last Activity</h3>
            <h2>{stats['last_run'][:10]}</h2>
            <p>Stay consistent!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        daily_goal_progress = min(stats['solved'] % DAILY_GOAL, DAILY_GOAL)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Daily Goal</h3>
            <h2>{daily_goal_progress}/{DAILY_GOAL}</h2>
            <p>Problems today</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Get New Problem", use_container_width=True):
            st.session_state.current_problem = system.get_random_unsolved()
            st.rerun()
    
    with col2:
        if st.button("📚 Review Problems", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🎯 Start Study Session", use_container_width=True):
            st.rerun()

def show_solve_interface():
    st.markdown(f"""
    <div class="main-header">
        <h1>💻 Solve Problems</h1>
        <p>Practice with AI-powered guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Problem Selection")
        
        # Problem selection
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Hard"])
        
        # Get all available patterns from the JSON data
        all_patterns = set()
        for problem in system.neetcode:
            if problem.get("pattern"):
                all_patterns.add(problem["pattern"])
        all_patterns = sorted(list(all_patterns))
        
        pattern_filter = st.selectbox("Pattern", ["Any"] + all_patterns)
        show_skipped = st.checkbox("Include skipped problems")
        
        if st.button("🎲 Get Random Problem", use_container_width=True):
            unsolved = system.get_unsolved_problems(
                difficulty if difficulty != "Any" else None
            )
            
            # Apply pattern filter
            if pattern_filter != "Any":
                unsolved = [p for p in unsolved if p.get("pattern") == pattern_filter]
            
            if show_skipped:
                skipped = [p for p in system.neetcode if str(p.get("status", "")).lower() == "skipped"]
                for p in skipped:
                    if p not in unsolved:
                        unsolved.append(p)
            
            if unsolved:
                problem = random.choice(unsolved)
                st.session_state.current_problem = problem
                st.session_state.user_code = ""
                st.session_state.analysis = None
                st.rerun()
            else:
                st.error("No problems available with current filters")
        
        # Current problem info
        if st.session_state.current_problem:
            p = st.session_state.current_problem
            st.markdown(f"""
            <div class="problem-card">
                <h4>🎯 Current Problem</h4>
                <p><strong>{p['id']} - {p['title']}</strong></p>
                <p>Pattern: {p.get('pattern', 'Auto-detecting...')}</p>
                <p>Difficulty: <span class="difficulty-badge difficulty-{p['difficulty'].lower()}">{p['difficulty']}</span></p>
                <a href="{p['url']}" target="_blank">🔗 LeetCode Link</a>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⏭️ Skip Problem", use_container_width=True):
                for prob in system.neetcode:
                    if prob.get("id") == p.get("id"):
                        prob["status"] = "Skipped"
                        break
                with open(system.NEETCODE_FILE, "w") as f:
                    json.dump(system.neetcode, f, indent=2)
                st.session_state.current_problem = None
                st.success("Problem skipped. Select a new one.")
                st.rerun()
    
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
            language = st.selectbox("Programming Language", ["java", "python", "cpp", "javascript"], index=0)
            
            # Code editor
            st.session_state.user_code = st.text_area(
                "Write your solution here:", 
                st.session_state.user_code,
                height=400,
                help="Write your solution code here. The system will automatically analyze and provide feedback."
            )
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🔍 Analyze Solution", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("🤖 Analyzing with AI..."):
                            try:
                                analysis = system.analyze_solution(p, st.session_state.user_code)
                                st.session_state.analysis = analysis
                                st.success("✅ Analysis complete!")
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
                            except Exception as e:
                                st.error(f"Explanation failed: {e}")
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn3:
                if st.button("💾 Save Solution", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("💾 Saving..."):
                            try:
                                # Create a simple analysis for saving
                                simple_analysis = {
                                    "correct": True,
                                    "approach_summary": "Solution saved",
                                    "complexity": "Analysis pending"
                                }
                                system.record_solution(p, st.session_state.user_code, simple_analysis)
                                st.success("✅ Solution saved successfully!")
                            except Exception as e:
                                st.error(f"Save failed: {e}")
                    else:
                        st.error("Please enter your solution code")
            
            # Display analysis
            if st.session_state.analysis:
                analysis = st.session_state.analysis
                st.divider()
                
                if analysis.get("correct", False):
                    st.success("✅ Your solution is correct!")
                else:
                    st.error("⚠️ Your solution needs improvement")
                
                # Analysis display
                col_analysis1, col_analysis2 = st.columns(2)
                
                with col_analysis1:
                    with st.expander("📝 Analysis Summary", expanded=True):
                        st.write("**Approach:**", analysis.get("approach_summary", ""))
                        st.write("**Complexity:**", analysis.get("complexity", ""))
                
                with col_analysis2:
                    with st.expander("🔧 Optimized Solution"):
                        st.code(analysis.get("fixed_code", ""), language=language)
            
            # Display code explanation
            if hasattr(st.session_state, 'code_explanation') and st.session_state.code_explanation:
                st.subheader("📚 Code Explanation")
                st.markdown(st.session_state.code_explanation)

def generate_code_explanation(problem, code, language):
    """Generate detailed explanation of the code"""
    return f"""
## Code Explanation for {problem['title']}

**Language:** {language}

### What the code does:
[AI explanation would appear here - requires API key]

### DSA Pattern:
[Pattern detection would appear here]

### Complexity:
[Complexity analysis would appear here]

### Key Insights:
[Insights would appear here]

**To enable AI features:**
1. Get API keys from Groq (https://console.groq.com/) or OpenRouter (https://openrouter.ai/)
2. Add them to your `.env` file
3. Restart the application
    """

def show_problem_browser():
    st.markdown(f"""
    <div class="main-header">
        <h1>🔍 Problem Browser</h1>
        <p>Explore and filter problems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Get all available patterns from the JSON data
        all_patterns = set()
        for problem in system.neetcode:
            if problem.get("pattern"):
                all_patterns.add(problem["pattern"])
        all_patterns = sorted(list(all_patterns))
        
        pattern_filter = st.selectbox("Filter by Pattern", 
                                     ["All"] + all_patterns)
    with col2:
        difficulty_filter = st.selectbox("Filter by Difficulty", 
                                        ["All", "Easy", "Medium", "Hard"])
    with col3:
        status_filter = st.selectbox("Filter by Status", 
                                    ["All", "Solved", "Unsolved", "Skipped"])
    with col4:
        search_term = st.text_input("Search by title or ID")
    
    # Display problems
    problems_displayed = 0
    for problem in sorted(system.neetcode, key=lambda x: (str(x.get("status", "")).lower() != "completed", x.get("pattern", ""), x.get("title", ""))):
        # Apply filters
        if pattern_filter != "All" and problem.get("pattern") != pattern_filter:
            continue
        if difficulty_filter != "All" and problem.get("difficulty", "").lower() != difficulty_filter.lower():
            continue
        
        status = problem.get("status", "Unsolved")
        if not isinstance(status, str):
            status = str(status)
        status = status.capitalize()
        
        if status_filter != "All" and status != status_filter:
            continue
        
        if search_term and search_term.lower() not in problem.get("title", "").lower() and search_term.lower() not in problem.get("id", "").lower():
            continue
        
        # Problem card
        difficulty_class = f"difficulty-{problem.get('difficulty', 'unknown').lower()}"
        
        st.markdown(f"""
        <div class="problem-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4>{problem['id']} - {problem['title']}</h4>
                    <p style="color: #666; margin-bottom: 10px;">
                        <span class="pattern-badge">{problem.get('pattern', 'Not detected')}</span>
                        <span class="difficulty-badge {difficulty_class}">{problem.get('difficulty', 'Unknown')}</span>
                        <span style="background: {'#4CAF50' if status == 'Completed' else '#FF9800' if status == 'Skipped' else '#F44336'}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">{status}</span>
                    </p>
                    <p>{problem.get("description", "")[:200]}{'...' if len(problem.get("description", "")) > 200 else ''}</p>
                </div>
                <div style="margin-left: 1rem;">
                    <a href="{problem.get('url', '#')}" target="_blank" style="text-decoration: none;">
                        <button style="background: {THEME_COLOR}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">🔗</button>
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎯 Solve", key=f"solve_{problem['id']}", use_container_width=True):
                st.session_state.current_problem = problem
                st.session_state.user_code = ""
                st.session_state.analysis = None
                st.rerun()
        
        with col_btn2:
            if st.button("📝 View Notes", key=f"notes_{problem['id']}", use_container_width=True):
                st.info("Notes feature coming soon!")
        
        problems_displayed += 1
    
    if problems_displayed == 0:
        st.info("No problems match your current filters. Try adjusting your search criteria.")

def show_study_mode():
    st.markdown(f"""
    <div class="main-header">
        <h1>🎯 Study Mode</h1>
        <p>Spaced repetition and active recall</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Study mode features coming soon! For now, use the Problem Browser to practice problems.")
    
    # Quick quiz placeholder
    st.subheader("🎯 Quick Quiz")
    st.write("**Question:** What pattern is commonly used for array problems?")
    
    options = ["Sliding Window", "Two Pointers", "Dynamic Programming", "All of the above"]
    selected_answer = st.radio("Select the correct answer:", options)
    
    if st.button("✅ Check Answer"):
        if selected_answer == "All of the above":
            st.success("✅ Correct! All these patterns are commonly used for array problems.")
        else:
            st.error("❌ Incorrect. The correct answer is: All of the above")

if __name__ == "__main__":
    main() 