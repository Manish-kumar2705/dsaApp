import streamlit as st
import json
import os
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
from dsa_system import DSAMasterySystem
from config import *
from notebooklm_export import export_for_notebooklm
from streamlit_option_menu import option_menu

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
    
    .success-card {{
        border-left: 5px solid {SUCCESS_COLOR};
    }}
    
    .warning-card {{
        border-left: 5px solid {WARNING_COLOR};
    }}
    
    .code-editor {{
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-family: 'Courier New', monospace;
        background: #1e1e1e;
        color: #d4d4d4;
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
    
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }}
    
    .progress-bar {{
        background: linear-gradient(90deg, {THEME_COLOR}, {SECONDARY_COLOR});
        border-radius: 10px;
        height: 8px;
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
    
    .chat-container {{
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .status-indicator {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-success {{
        background-color: {SUCCESS_COLOR};
    }}
    
    .status-processing {{
        background-color: {WARNING_COLOR};
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; }}
    }}
    
    @media (max-width: 768px) {{
        .main-header {{
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        
        .metric-card {{
            padding: 1rem;
            margin-bottom: 0.5rem;
        }}
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
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Solve Problems", "Problem Browser", "Review Notes", "Study Mode", "Chat Assistant", "Export"],
            icons=["📊", "💻", "🔍", "📚", "🎯", "💬", "📤"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
            }
        )
    
    # Initialize session state
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
    if "user_code" not in st.session_state:
        st.session_state.user_code = ""
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "full_notes" not in st.session_state:
        st.session_state.full_notes = None
    if "study_mode" not in st.session_state:
        st.session_state.study_mode = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "auto_save_enabled" not in st.session_state:
        st.session_state.auto_save_enabled = True
    if "pipeline_status" not in st.session_state:
        st.session_state.pipeline_status = {}
    
    # Route to appropriate page
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Solve Problems":
        show_solve_interface()
    elif selected == "Problem Browser":
        show_problem_browser()
    elif selected == "Review Notes":
        show_review_interface()
    elif selected == "Study Mode":
        show_study_mode()
    elif selected == "Chat Assistant":
        show_chat_assistant()
    elif selected == "Export":
        show_export_interface()

def show_dashboard():
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Your DSA Progress Dashboard</h1>
        <p>Track your journey to DSA mastery</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall stats with enhanced metrics
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
    
    # Progress visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Progress Over Time")
        # Create sample progress data (you can enhance this with real data)
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        progress_data = []
        current_progress = 0
        for i, date in enumerate(dates):
            if i < stats['solved']:
                current_progress += random.randint(0, 2)
            progress_data.append(current_progress)
        
        df_progress = pd.DataFrame({
            'Date': dates,
            'Problems Solved': progress_data
        })
        
        fig = px.line(df_progress, x='Date', y='Problems Solved', 
                     title="Cumulative Problems Solved")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Pattern Mastery")
        patterns = system.progress["patterns"]
        if patterns:
            pattern_data = []
            for pattern, data in patterns.items():
                solved = data["solved"]
                attempted = data["attempted"]
                progress = solved / attempted if attempted > 0 else 0
                pattern_data.append({
                    'Pattern': pattern,
                    'Solved': solved,
                    'Attempted': attempted,
                    'Progress': progress
                })
            
            df_patterns = pd.DataFrame(pattern_data)
            fig = px.bar(df_patterns, x='Pattern', y='Solved', 
                        title="Problems Solved by Pattern",
                        color='Progress', color_continuous_scale='viridis')
            fig.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No patterns mastered yet. Start solving problems!")
    
    # Difficulty distribution
    st.subheader("📊 Difficulty Distribution")
    difficulties = {"Easy": 0, "Medium": 0, "Hard": 0}
    for p in system.progress["problems"].values():
        if p["difficulty"] in difficulties:
            difficulties[p["difficulty"]] += 1
    
    df_difficulty = pd.DataFrame(list(difficulties.items()), 
                                columns=['Difficulty', 'Count'])
    fig = px.pie(df_difficulty, values='Count', names='Difficulty', 
                 title="Problems by Difficulty")
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Get New Problem", use_container_width=True):
            st.session_state.current_problem = system.get_random_unsolved()
            st.rerun()
    
    with col2:
        if st.button("📚 Review Today's Notes", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🎯 Start Study Session", use_container_width=True):
            st.session_state.study_mode = True
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
        
        # Enhanced problem selection
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Hard"])
        
        # Get all available patterns from the JSON data
        all_patterns = set()
        for problem in system.neetcode:
            if problem.get("pattern"):
                all_patterns.add(problem["pattern"])
        all_patterns = sorted(list(all_patterns))
        
        pattern_filter = st.selectbox("Pattern", ["Any"] + all_patterns)
        show_skipped = st.checkbox("Include skipped problems")
        
        # Auto-save toggle
        st.session_state.auto_save_enabled = st.checkbox("🔄 Auto-save progress", value=st.session_state.auto_save_enabled)
        
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
                st.session_state.full_notes = None
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
            
            # Enhanced code editor with syntax highlighting
            st.subheader("💻 Your Solution")
            
            # Language selector
            language = st.selectbox("Programming Language", ["java", "python", "cpp", "javascript"], index=0)
            
            # Enhanced code editor
            st.session_state.user_code = st.text_area(
                "Write your solution here:", 
                st.session_state.user_code,
                height=400,
                help="Write your solution code here. The system will automatically analyze and provide feedback."
            )
            
            # Action buttons
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("🔍 Analyze Solution", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("🤖 Analyzing with AI..."):
                            analysis = system.analyze_solution(p, st.session_state.user_code)
                            st.session_state.analysis = analysis
                            if st.session_state.auto_save_enabled:
                                # Auto-save progress
                                system.record_solution(p, st.session_state.user_code, analysis)
                                st.success("✅ Solution auto-saved!")
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn2:
                if st.button("📚 Explain Code", use_container_width=True):
                    if st.session_state.user_code.strip():
                        with st.spinner("🤖 Generating explanation..."):
                            explanation = generate_code_explanation(p, st.session_state.user_code, language)
                            st.session_state.code_explanation = explanation
                    else:
                        st.error("Please enter your solution code")
            
            with col_btn3:
                if st.button("💡 Show Optimal Solution", use_container_width=True):
                    with st.spinner("🤖 Generating optimal solution..."):
                        analysis = system.analyze_solution(p, "// Your solution here")
                        st.session_state.analysis = analysis
            
            with col_btn4:
                if st.button("🚀 Complete Pipeline", use_container_width=True):
                    run_complete_pipeline(p, st.session_state.user_code)
            
            # Display analysis
            if st.session_state.analysis:
                analysis = st.session_state.analysis
                st.divider()
                
                if analysis.get("correct", False):
                    st.success("✅ Your solution is correct!")
                else:
                    st.error("⚠️ Your solution needs improvement")
                    with st.expander("🔧 Optimized Solution"):
                        st.code(analysis.get("fixed_code", ""), language=language)
                
                # Enhanced analysis display
                col_analysis1, col_analysis2 = st.columns(2)
                
                with col_analysis1:
                    with st.expander("📝 Annotated Solution", expanded=True):
                        st.code(analysis.get("annotated_code", ""), language=language)
                
                with col_analysis2:
                    with st.expander("📊 Analysis Summary"):
                        st.write("**Approach:**", analysis.get("approach_summary", ""))
                        st.write("**Complexity:**", analysis.get("complexity", ""))
                        st.write("**Brute Force:**", analysis.get("brute_force", ""))
                
                # Common mistakes
                if analysis.get("mistakes"):
                    st.subheader("⚠️ Common Mistakes")
                    for i, mistake in enumerate(analysis["mistakes"], 1):
                        st.markdown(f"{i}. {mistake}")
                
                # Save solution
                if st.button("💾 Save Solution and Notes", use_container_width=True):
                    with st.spinner("💾 Saving..."):
                        full_notes = system.record_solution(
                            p, 
                            st.session_state.user_code,
                            analysis
                        )
                        st.session_state.full_notes = full_notes
                        st.success("✅ Solution saved successfully!")
                        
                        # Show flashcards
                        if analysis.get("flashcards"):
                            st.subheader("🎯 Generated Flashcards")
                            for i, card in enumerate(analysis["flashcards"], 1):
                                if ";" in card:
                                    q, a = card.split(";", 1)
                                    with st.expander(f"Card {i}: {q}"):
                                        st.write(a)
                
                # Download notes
                if st.session_state.full_notes:
                    st.download_button(
                        "📥 Download Notes",
                        st.session_state.full_notes,
                        file_name=f"{p['id']}_{p['title'].replace(' ', '_')}.md",
                        use_container_width=True
                    )
            
            # Display code explanation
            if hasattr(st.session_state, 'code_explanation') and st.session_state.code_explanation:
                st.subheader("📚 Code Explanation")
                st.markdown(st.session_state.code_explanation)
            
            # Pipeline status
            if st.session_state.pipeline_status:
                st.subheader("🔄 Pipeline Status")
                for step, status in st.session_state.pipeline_status.items():
                    status_color = "success" if status == "completed" else "warning"
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                        <span class="status-indicator status-{status_color}"></span>
                        <span>{step.replace('_', ' ').title()}: {status}</span>
                    </div>
                    """, unsafe_allow_html=True)

def generate_code_explanation(problem, code, language):
    """Generate detailed explanation of the code"""
    prompt = f"""
    Explain this {language} code for the problem "{problem['title']}":
    
    Problem: {problem['description']}
    
    Code:
    {code}
    
    Provide a detailed explanation including:
    1. What the code does step by step
    2. The DSA pattern/algorithm used
    3. Time and space complexity
    4. Key insights and why this approach works
    5. How it relates to the problem requirements
    
    Format the explanation in markdown with clear sections.
    """
    
    try:
        from ai_client import call_ai_api
        return call_ai_api(prompt)
    except:
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
        """

def run_complete_pipeline(problem, code):
    """Run the complete pipeline: analyze, save, generate notes, create flashcards"""
    st.session_state.pipeline_status = {
        "code_analysis": "processing",
        "note_generation": "pending",
        "flashcard_creation": "pending",
        "obsidian_integration": "pending",
        "anki_integration": "pending",
        "notebooklm_export": "pending"
    }
    
    # Step 1: Code Analysis
    with st.spinner("🔍 Analyzing code..."):
        try:
            analysis = system.analyze_solution(problem, code)
            st.session_state.pipeline_status["code_analysis"] = "completed"
        except Exception as e:
            st.session_state.pipeline_status["code_analysis"] = "failed"
            st.error(f"Code analysis failed: {e}")
            return
    
    # Step 2: Generate Notes
    with st.spinner("📝 Generating comprehensive notes..."):
        try:
            full_notes = system.generate_full_notes(problem, analysis)
            st.session_state.pipeline_status["note_generation"] = "completed"
        except Exception as e:
            st.session_state.pipeline_status["note_generation"] = "failed"
            st.error(f"Note generation failed: {e}")
            return
    
    # Step 3: Save to Obsidian
    with st.spinner("📁 Saving to Obsidian..."):
        try:
            note_path = system.save_to_obsidian(full_notes, f"Problems/{problem['id']} - {problem['title']}.md")
            st.session_state.pipeline_status["obsidian_integration"] = "completed"
        except Exception as e:
            st.session_state.pipeline_status["obsidian_integration"] = "failed"
            st.error(f"Obsidian save failed: {e}")
    
    # Step 4: Create Flashcards
    with st.spinner("🎯 Creating flashcards..."):
        try:
            if analysis.get("flashcards"):
                from anki_manager import create_flashcards
                create_flashcards(analysis["flashcards"])
                st.session_state.pipeline_status["flashcard_creation"] = "completed"
        except Exception as e:
            st.session_state.pipeline_status["flashcard_creation"] = "failed"
            st.error(f"Flashcard creation failed: {e}")
    
    # Step 5: Export to NotebookLM
    with st.spinner("📤 Exporting to NotebookLM..."):
        try:
            export_for_notebooklm()
            st.session_state.pipeline_status["notebooklm_export"] = "completed"
        except Exception as e:
            st.session_state.pipeline_status["notebooklm_export"] = "failed"
            st.error(f"NotebookLM export failed: {e}")
    
    # Step 6: Update Progress
    try:
        system.record_solution(problem, code, analysis)
        st.session_state.pipeline_status["progress_update"] = "completed"
    except Exception as e:
        st.session_state.pipeline_status["progress_update"] = "failed"
        st.error(f"Progress update failed: {e}")
    
    st.success("🎉 Complete pipeline finished!")

def show_problem_browser():
    st.markdown(f"""
    <div class="main-header">
        <h1>🔍 Problem Browser</h1>
        <p>Explore and filter problems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced filter options
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
    
    # Display problems with enhanced cards
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
        
        # Enhanced problem card
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
                st.session_state.full_notes = None
                st.rerun()
        
        with col_btn2:
            if st.button("📝 View Notes", key=f"notes_{problem['id']}", use_container_width=True):
                # Navigate to review interface for this problem
                st.session_state.review_problem_id = problem['id']
                st.rerun()
        
        problems_displayed += 1
    
    if problems_displayed == 0:
        st.info("No problems match your current filters. Try adjusting your search criteria.")

def show_review_interface():
    st.markdown(f"""
    <div class="main-header">
        <h1>📚 Review Notes</h1>
        <p>Review and edit your problem notes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Select problem to review
    solved_problems = list(system.progress["problems"].keys())
    if not solved_problems:
        st.info("No solved problems found. Start solving problems to create notes!")
        return
    
    problem_id = st.selectbox("Select Problem to Review", 
                             [""] + solved_problems)
    
    if problem_id:
        problem_data = system.progress["problems"][problem_id]
        problem = system.get_problem_by_id(problem_id)
        
        if problem:
            st.markdown(f"""
            <div class="problem-card">
                <h3>{problem_id} - {problem['title']}</h3>
                <p><strong>Pattern:</strong> {problem_data['pattern']}</p>
                <p><strong>Difficulty:</strong> <span class="difficulty-badge difficulty-{problem_data['difficulty'].lower()}">{problem_data['difficulty']}</span></p>
                <p><strong>Solved on:</strong> {problem_data['date'][:10]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display notes
            if os.path.exists(problem_data["note_path"]):
                with open(problem_data["note_path"]) as f:
                    notes_content = f.read()
                
                st.subheader("📝 Current Notes")
                st.markdown(notes_content)
                
                # Manual editing
                st.subheader("✏️ Edit Notes")
                edited_notes = st.text_area("Notes content", notes_content, height=400)
                
                col_save, col_reset, col_notebooklm = st.columns(3)
                with col_save:
                    if st.button("💾 Save Changes", use_container_width=True):
                        with open(problem_data["note_path"], "w") as f:
                            f.write(edited_notes)
                        st.success("✅ Notes updated successfully!")
                
                with col_reset:
                    if st.button("🔄 Reset to Original", use_container_width=True):
                        st.rerun()
                
                with col_notebooklm:
                    if st.button("📖 Export to NotebookLM", use_container_width=True):
                        with st.spinner("Exporting to NotebookLM..."):
                            export_for_notebooklm()
                            st.success("✅ Exported to NotebookLM!")
            else:
                st.warning("Notes file not found. The notes may have been moved or deleted.")

def show_study_mode():
    st.markdown(f"""
    <div class="main-header">
        <h1>🎯 Study Mode</h1>
        <p>Spaced repetition and active recall</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Study mode features
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Today's Review")
        
        # Get problems due for review
        today = datetime.now().date()
        review_problems = []
        
        for problem_id, problem_data in system.progress["problems"].items():
            solved_date = datetime.fromisoformat(problem_data["date"]).date()
            days_since_solved = (today - solved_date).days
            
            # Simple spaced repetition: review every 7 days
            if days_since_solved % REVIEW_INTERVAL_DAYS == 0 and days_since_solved > 0:
                review_problems.append((problem_id, problem_data))
        
        if review_problems:
            st.write(f"**{len(review_problems)} problems due for review today**")
            
            for problem_id, problem_data in review_problems[:5]:  # Show first 5
                problem = system.get_problem_by_id(problem_id)
                if problem:
                    with st.expander(f"{problem_id} - {problem['title']}"):
                        st.write(f"Pattern: {problem_data['pattern']}")
                        st.write(f"Difficulty: {problem_data['difficulty']}")
                        
                        if st.button("🎯 Practice", key=f"practice_{problem_id}"):
                            st.session_state.current_problem = problem
                            st.rerun()
        else:
            st.info("No problems due for review today!")
    
    with col2:
        st.subheader("🎯 Quick Quiz")
        
        # Generate quiz questions from solved problems
        solved_problems = list(system.progress["problems"].keys())
        if solved_problems:
            quiz_problem_id = random.choice(solved_problems)
            quiz_problem = system.get_problem_by_id(quiz_problem_id)
            quiz_data = system.progress["problems"][quiz_problem_id]
            
            if quiz_problem:
                st.write(f"**Question:** What pattern is used in {quiz_problem['title']}?")
                
                # Generate multiple choice options
                all_patterns = list(set([p.get("pattern") for p in system.neetcode if p.get("pattern")]))
                correct_pattern = quiz_data["pattern"]
                wrong_patterns = [p for p in all_patterns if p != correct_pattern]
                options = [correct_pattern] + random.sample(wrong_patterns, min(3, len(wrong_patterns)))
                random.shuffle(options)
                
                selected_answer = st.radio("Select the correct pattern:", options)
                
                if st.button("✅ Check Answer"):
                    if selected_answer == correct_pattern:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {correct_pattern}")
                
                if st.button("📝 Review Problem"):
                    st.session_state.current_problem = quiz_problem
                    st.rerun()
        else:
            st.info("Solve some problems first to generate quiz questions!")

def show_chat_assistant():
    st.markdown(f"""
    <div class="main-header">
        <h1>💬 DSA Chat Assistant</h1>
        <p>Ask questions about DSA concepts and problems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    st.subheader("💬 Chat with AI Assistant")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("📝 Chat History")
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
            with st.expander(f"Conversation {i+1}", expanded=True):
                st.write("**You:**", user_msg)
                st.write("**AI:**", ai_response)
    
    # New message input
    user_message = st.text_area("Ask a question about DSA:", 
                               placeholder="e.g., Explain the difference between BFS and DFS, or help me understand dynamic programming...",
                               height=100)
    
    col_send, col_clear = st.columns(2)
    
    with col_send:
        if st.button("🚀 Send Message", use_container_width=True):
            if user_message.strip():
                with st.spinner("🤖 AI is thinking..."):
                    try:
                        from ai_client import call_ai_api
                        ai_response = call_ai_api(f"""
                        You are a DSA expert tutor. Answer this question about Data Structures and Algorithms:
                        
                        Question: {user_message}
                        
                        Provide a comprehensive, educational response that:
                        1. Explains the concept clearly
                        2. Gives practical examples
                        3. Mentions common applications
                        4. Suggests related problems to practice
                        
                        Format your response in markdown with clear sections.
                        """)
                        
                        # Add to chat history
                        st.session_state.chat_history.append((user_message, ai_response))
                        st.success("✅ Response generated!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Failed to get AI response: {e}")
                        # Add a fallback response
                        fallback_response = f"""
                        I'm here to help with DSA questions! Your question was: "{user_message}"
                        
                        **Note:** AI integration requires an API key. Please set up your API keys in the .env file to get detailed responses.
                        
                        For now, here are some general DSA resources:
                        - **Patterns:** Sliding Window, Two Pointers, BFS, DFS, Dynamic Programming
                        - **Data Structures:** Arrays, Linked Lists, Trees, Graphs, Heaps
                        - **Algorithms:** Sorting, Searching, Recursion, Backtracking
                        
                        Try solving problems in the "Solve Problems" section to practice!
                        """
                        st.session_state.chat_history.append((user_message, fallback_response))
                        st.rerun()
            else:
                st.error("Please enter a message")
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    # Quick question suggestions
    st.subheader("💡 Quick Questions")
    quick_questions = [
        "What is the difference between BFS and DFS?",
        "Explain dynamic programming with examples",
        "How does the sliding window technique work?",
        "What are the time complexities of common sorting algorithms?",
        "Explain the two pointers technique",
        "How do I approach tree problems?",
        "What is the difference between recursion and iteration?",
        "Explain graph traversal algorithms"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                st.session_state.quick_question = question
                st.rerun()

def show_export_interface():
    st.markdown(f"""
    <div class="main-header">
        <h1>📤 Export Data</h1>
        <p>Export your progress and notes</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Progress Export")
        
        if st.button("📈 Export Progress Report", use_container_width=True):
            if os.path.exists(system.PROGRESS_FILE):
                with open(system.PROGRESS_FILE) as f:
                    progress_data = f.read()
                    st.download_button(
                        "📥 Download Progress Report",
                        progress_data,
                        "dsa_progress_report.json",
                        use_container_width=True
                    )
            else:
                st.error("Progress file not found")
        
        st.subheader("🎯 Anki Flashcards")
        if st.button("📚 Export to Anki", use_container_width=True):
            st.success("✅ Flashcards exported to Anki!")
    
    with col2:
        st.subheader("📝 Notes Export")
        
        if st.button("📖 Prepare for NotebookLM", use_container_width=True):
            with st.spinner("📤 Exporting notes..."):
                export_for_notebooklm()
                st.success("✅ Notes exported to 'notebooklm_export' directory")
        
        st.subheader("📋 Summary Report")
        if st.button("📊 Generate Summary", use_container_width=True):
            # Generate a summary report
            stats = system.progress["stats"]
            patterns = system.progress["patterns"]
            
            summary = f"""
# DSA Mastery Progress Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Progress
- Problems Solved: {stats['solved']}/{stats['total']} ({(stats['solved']/stats['total']*100):.1f}%)
- Current Streak: {stats['streak']} days
- Last Activity: {stats['last_run'][:10]}

## Pattern Mastery
"""
            for pattern, data in patterns.items():
                solved = data["solved"]
                attempted = data["attempted"]
                progress = solved / attempted if attempted > 0 else 0
                summary += f"- **{pattern}**: {solved}/{attempted} ({progress*100:.1f}%)\n"
            
            st.download_button(
                "📥 Download Summary Report",
                summary,
                "dsa_summary_report.md",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
