import os
import json
import random
import re
from datetime import datetime
from pathlib import Path
from config import *
from ai_client import call_ai_api
from anki_manager import create_flashcards

class DSAMasterySystem:
    def __init__(self):
        self.progress = self.load_progress()
        self.neetcode = self.load_neetcode()
        self.ensure_directories()
    
    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE) as f:
                return json.load(f)
        return {
            "problems": {},
            "patterns": {},
            "stats": {
                "solved": 0,
                "total": 150,
                "streak": 0,
                "last_run": datetime.now().isoformat()
            }
        }
    
    def load_neetcode(self):
        with open(NEETCODE_FILE) as f:
            return json.load(f)
    
    def ensure_directories(self):
        Path(OBSIDIAN_VAULT).mkdir(parents=True, exist_ok=True)
        Path(OBSIDIAN_VAULT, "Patterns").mkdir(exist_ok=True)
        Path(OBSIDIAN_VAULT, "Problems").mkdir(exist_ok=True)
    
    def get_unsolved_problems(self, difficulty=None):
        """Get all unsolved problems with optional difficulty filter"""
        return [p for p in self.neetcode 
                if str(p.get("status", "")).lower() != "completed"
                and (difficulty is None or p.get("difficulty", "").lower() == difficulty.lower() if difficulty else True)]
    
    def get_random_unsolved(self, difficulty=None):
        """Get random unsolved problem with optional difficulty filter"""
        unsolved = self.get_unsolved_problems(difficulty)
        return random.choice(unsolved) if unsolved else None
    
    def get_problem_by_id(self, problem_id):
        """Get problem by ID (e.g., 'LC1')"""
        return next((p for p in self.neetcode if p.get("id") == problem_id), None)
    
    def auto_detect_pattern(self, problem):
        """Use AI to detect pattern from problem description"""
        prompt = f"""
        Based on this problem description, identify the primary DSA pattern:
        Title: {problem['title']}
        Description: {problem['description']}
        
        Respond ONLY with the pattern name from this list:
        Sliding Window, Two Pointers, BFS, DFS, Dynamic Programming, 
        Binary Search, Hash Map, Stack, Queue, Linked List, Tree, Graph, 
        Heap, Trie, Backtracking, Greedy, Bit Manipulation.
        """
        return call_ai_api(prompt).strip()
    
    def analyze_solution(self, problem, solution_code):
        """Analyze and correct user's solution with AI"""
        prompt = f"""
        Problem: {problem['title']}
        Description: {problem['description']}
        
        User's Solution:
        {solution_code}
        
        Tasks:
        1. Check if solution is correct (return boolean)
        2. If incorrect, provide fixed optimal solution
        3. Add detailed inline comments
        4. Explain approach and complexity
        5. Compare with brute force solution
        6. Highlight 2 common mistakes
        7. Create 3 flashcards (Q;A format)
        
        Return JSON format:
        {{
            "correct": bool,
            "fixed_code": str,
            "annotated_code": str,
            "approach_summary": str,
            "complexity": str,
            "brute_force": str,
            "mistakes": [str],
            "flashcards": [str]
        }}
        """
        return json.loads(call_ai_api(prompt))
    
    def generate_full_notes(self, problem, analysis):
        """Generate comprehensive notes with multiple approaches"""
        prompt = f"""
        For problem {problem['title']} ({problem['id']}), create comprehensive notes including:
        1. Problem summary
        2. Brute force approach with code and complexity
        3. Optimal approach with code and complexity
        4. Key insights and pattern identification
        5. Edge cases
        6. 5 Anki flashcards (Q;A format)
        
        Format as Markdown with clear sections.
        """
        return call_ai_api(prompt)
    
    def save_to_obsidian(self, content, path):
        """Save file to Obsidian vault"""
        full_path = Path(OBSIDIAN_VAULT) / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return str(full_path)
    
    def record_solution(self, problem, solution, analysis):
        """Record solution in progress database"""
        # Auto-detect pattern if not set
        if "pattern" not in problem or not problem["pattern"]:
            problem["pattern"] = self.auto_detect_pattern(problem)
        
        # Generate full notes
        full_notes = self.generate_full_notes(problem, analysis)
        note_path = self.save_to_obsidian(
            full_notes, 
            f"Problems/{problem['id']} - {problem['title']}.md"
        )
        
        # Save flashcards
        if 'flashcards' in analysis:
            create_flashcards(analysis['flashcards'])
        
        # Update problem status in neetcode list
        for p in self.neetcode:
            if p.get("id") == problem.get("id"):
                p["status"] = "Completed"
                break
        
        # Save updated neetcode list
        with open(NEETCODE_FILE, "w") as f:
            json.dump(self.neetcode, f, indent=2)
        
        # Update progress file for stats tracking
        self.progress["problems"][problem["id"]] = {
            "solved": True,
            "date": datetime.now().isoformat(),
            "pattern": problem["pattern"],
            "difficulty": problem["difficulty"],
            "note_path": note_path,
            "analysis": analysis
        }
        
        # Update pattern stats
        pattern_data = self.progress["patterns"].setdefault(problem["pattern"], {
            "solved": 0,
            "attempted": 0
        })
        pattern_data["solved"] += 1
        pattern_data["attempted"] += 1
        
        # Update global stats
        self.progress["stats"]["solved"] = len([p for p in self.progress["problems"].values() if p["solved"]])
        self.progress["stats"]["streak"] += 1
        self.progress["stats"]["last_run"] = datetime.now().isoformat()
        
        with open(PROGRESS_FILE, "w") as f:
            json.dump(self.progress, f, indent=2)
        
        return full_notes
