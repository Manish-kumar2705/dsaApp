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
    
    # Sidebar navigation
    st.sidebar.title("🎯 DSA Mastery")
    st.sidebar.markdown("---")
    
    selected = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Dashboard", "💻 Solve Problems", "📚 Problem Browser", "📖 Review Notes", "🎓 Study Mode"]
    )
    
    # Display selected page
    if selected == "🏠 Dashboard":
        show_dashboard(system)
    elif selected == "💻 Solve Problems":
        show_solve_interface(system)
    elif selected == "📚 Problem Browser":
        show_problem_browser(system)
    elif selected == "📖 Review Notes":
        show_review_interface(system)
    elif selected == "🎓 Study Mode":
        show_study_mode(system)

def show_dashboard(system):
    st.markdown("""
    <div class="main-header">
        <h1>🎯 DSA Mastery Dashboard</h1>
        <p>Track your progress and master Data Structures & Algorithms</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress overview
    col1, col2, col3, col4 = st.columns(4)
    
    total_problems = len(system.neetcode)
    completed = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "completed"])
    skipped = len([p for p in system.neetcode if str(p.get("status", "")).lower() == "skipped"])
    remaining = total_problems - completed - skipped
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Total Problems</h3>
            <h2>{total_problems}</h2>
            <p>NeetCode 150</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Completed</h3>
            <h2>{completed}</h2>
            <p>{completed/total_problems*100:.1f}% done</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏭️ Skipped</h3>
            <h2>{skipped}</h2>
            <p>For later review</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Remaining</h3>
            <h2>{remaining}</h2>
            <p>To solve</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Get New Problem", use_container_width=True, type="primary"):
            problem = system.get_random_unsolved()
            if problem:
                st.session_state.current_problem = problem
                st.session_state.user_code = ""
                st.session_state.analysis = None
                st.rerun()
            else:
                st.error("No unsolved problems available!")
    
    with col2:
        if st.button("📚 Browse Problems", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🎓 Start Study Session", use_container_width=True):
            st.rerun()

def show_solve_interface(system):
    st.markdown("""
    <div class="main-header">
        <h1>💻 Solve Problems</h1>
        <p>Practice with AI-powered guidance and feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Problem Selection")
        
        # Problem selection
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Hard"])
        
        # Get all available patterns
        all_patterns = set()
        for problem in system.neetcode:
            if problem.get("pattern"):
                all_patterns.add(problem["pattern"])
        all_patterns = sorted(list(all_patterns))
        
        pattern_filter = st.selectbox("Pattern", ["Any"] + all_patterns)
        show_skipped = st.checkbox("Include skipped problems")
        
        if st.button("🎲 Get Random Problem", use_container_width=True, type="primary"):
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
                st.session_state.code_explanation = None
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
            language = st.selectbox("Programming Language", ["python", "java", "cpp", "javascript"], index=0)
            
            # Code editor
            st.session_state.user_code = st.text_area(
                "Write your solution here:", 
                st.session_state.user_code,
                height=300,
                help="Write your solution code here. The AI will analyze and provide detailed feedback."
            )
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
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
                if st.button("💾 Save Solution", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("💾 Saving..."):
                            try:
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
    <div class="main-header">
        <h1>📚 Problem Browser</h1>
        <p>Browse and filter all available problems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
    
    with col2:
        status_filter = st.selectbox("Status", ["All", "Not Started", "Completed", "Skipped"])
    
    with col3:
        pattern_filter = st.selectbox("Pattern", ["All"] + sorted(list(set([p.get("pattern", "") for p in system.neetcode if p.get("pattern")]))))
    
    # Filter problems
    filtered_problems = system.neetcode
    
    if difficulty_filter != "All":
        filtered_problems = [p for p in filtered_problems if p.get("difficulty") == difficulty_filter]
    
    if status_filter != "All":
        status_map = {"Not Started": "", "Completed": "completed", "Skipped": "skipped"}
        target_status = status_map[status_filter]
        filtered_problems = [p for p in filtered_problems if str(p.get("status", "")).lower() == target_status]
    
    if pattern_filter != "All":
        filtered_problems = [p for p in filtered_problems if p.get("pattern") == pattern_filter]
    
    # Display problems
    st.subheader(f"📋 Problems ({len(filtered_problems)} found)")
    
    for problem in filtered_problems[:20]:  # Show first 20
        status = str(problem.get("status", "")).lower()
        status_color = {
            "completed": "✅",
            "skipped": "⏭️",
            "": "⏳"
        }.get(status, "⏳")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{problem['id']} - {problem['title']}**")
            st.write(f"Pattern: {problem.get('pattern', 'N/A')}")
        
        with col2:
            st.write(f"{status_color} {status.title() if status else 'Not Started'}")
        
        with col3:
            st.write(f"<span class='difficulty-badge difficulty-{problem['difficulty'].lower()}'>{problem['difficulty']}</span>", unsafe_allow_html=True)
        
        st.divider()

def show_review_interface(system):
    st.markdown("""
    <div class="main-header">
        <h1>📖 Review Notes</h1>
        <p>Review your saved solutions and notes</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📝 Review interface coming soon! This will show your saved solutions and notes.")

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