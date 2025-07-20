import os
import json
import random
import re
from datetime import datetime
from pathlib import Path
from config import *
from ai_client import call_ai_api
from anki_manager import create_flashcards

# Add this master pattern list at the top of the class
DSA_MASTER_PATTERNS = [
    "Sliding Window", "Two Pointers", "BFS", "DFS", "Dynamic Programming",
    "Binary Search", "Hash Map", "Stack", "Queue", "Linked List", "Tree", "Graph",
    "Heap", "Trie", "Backtracking", "Greedy", "Bit Manipulation"
]

# Recommended learning order for DSA patterns
DSA_LEARNING_ORDER = [
    "Arrays", "Hash Map", "Two Pointers", "Sliding Window", "Stack", "Queue", "Linked List",
    "Binary Search", "Tree", "Heap", "Trie", "Backtracking", "Greedy", "Bit Manipulation",
    "BFS", "DFS", "Graph", "Dynamic Programming"
]

class DSAMasterySystem:
    def __init__(self):
        self.progress = self.load_progress()
        self.neetcode = self.load_neetcode()
        self.ensure_directories()
        self._ensure_patterns()
    
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
    
    def get_all_problems(self):
        """Get all problems"""
        return self.neetcode
    
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
        """Save file to Obsidian vault, expanding ~ to user home directory"""
        full_path = Path(OBSIDIAN_VAULT).expanduser() / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
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

    def get_patterns(self):
        """Return a sorted list of all patterns in the problem set."""
        patterns = set()
        for p in self.neetcode:
            if p.get("pattern"):
                patterns.add(p["pattern"])
        return sorted(list(patterns))

    def get_problems_by_pattern(self, pattern):
        """Return all problems for a given pattern."""
        return [p for p in self.neetcode if p.get("pattern") == pattern]

    def get_next_pattern(self):
        """Return the next pattern with unsolved problems, or None if all done."""
        patterns = self.get_patterns()
        for pattern in patterns:
            problems = self.get_problems_by_pattern(pattern)
            if any(str(p.get("status", "")).lower() != "completed" for p in problems):
                return pattern
        return None

    def _ensure_patterns(self):
        # For each problem, if pattern is missing/empty, use category as fallback
        for p in self.neetcode:
            if not p.get("pattern") or not str(p["pattern"]).strip():
                p["pattern"] = p.get("category", "Uncategorized")

    def get_all_patterns(self):
        # Return all patterns in master list, plus any extra from the data
        patterns = set(DSA_MASTER_PATTERNS)
        for p in self.neetcode:
            if p.get("pattern"):
                patterns.add(p["pattern"])
        return sorted(list(patterns))

    def get_problems_by_pattern(self, pattern):
        # Return all problems for a given pattern, ordered by id
        return sorted([p for p in self.neetcode if p.get("pattern") == pattern], key=lambda p: p.get("id", ""))

    def get_next_unsolved_in_pattern(self, pattern):
        # Return the next unsolved problem in the given pattern, ordered by id
        problems = self.get_problems_by_pattern(pattern)
        for p in problems:
            if str(p.get("status", "")).lower() != "completed":
                return p
        return None

    def get_today_problem(self, pattern=None):
        # Return the planned problem for today: next unsolved in selected pattern (or next pattern if not specified)
        if not pattern:
            pattern = self.get_next_pattern()
        if not pattern:
            return None, None
        problem = self.get_next_unsolved_in_pattern(pattern)
        return pattern, problem

    def get_learning_order_patterns(self):
        # Return patterns in recommended learning order, then any extras
        patterns_in_data = set(p.get("pattern") for p in self.neetcode if p.get("pattern"))
        ordered = [p for p in DSA_LEARNING_ORDER if p in patterns_in_data]
        extras = sorted(list(patterns_in_data - set(ordered)))
        return ordered + extras

    def generate_dsa_note(self, problem, solution_code):
        """
        Generate a world-class DSA note and flashcards for a problem using AI.
        The note includes:
        - YAML frontmatter (pattern, tags, last reviewed, etc.)
        - Problem statement and at least one example
        - 2-3 hints
        - Intuition (as a separate section before the code)
        - General pattern approach
        - Brute force solution (with code and inline comments)
        - Best/optimal solution (with code and inline comments, and Java knowledge as code comments)
        - Step-by-step breakdown after the code
        - Key insights and edge cases
        - Complexity
        - 5-7 flashcards (Q&A)
        """
        prompt = f'''
You are an expert DSA teacher and interviewer. For the following LeetCode problem, generate a world-class study note for a student who wants to master DSA and ace interviews. The note must:

- Start with YAML frontmatter including:
  pattern: {problem.get('pattern', '')}
  tags: [{problem.get('category', '')}, {problem.get('difficulty', '')}]
  last_reviewed: ""
  revision_status: "new"

- Give the problem statement and at least one example input/output.

- Give 2–3 hints to help the student think about the problem.

- Write a section on intuition (how to approach the problem, what to look for) as a separate section BEFORE the code block.

- Write a section on the general approach for this pattern (how to solve similar problems).

- Show the brute force solution (with code, and all comments INSIDE the code block as inline comments). Briefly explain why it’s brute force and its limitations.

- Show the best/optimal solution (with code, and all comments INSIDE the code block as inline comments for every step/block).
  - At the top or bottom of the code, include a commented-out section listing all Java methods/classes/concepts used, with 1–2 line explanations for each.
  - After the code, break down the solution step-by-step in plain English.
  - Highlight what makes this solution optimal.

- List key insights and edge cases as bullet points.

- Give time and space complexity.

- End with 5–7 high-quality Anki flashcards (Q;A format).

- Use only ### or #### for headings, never # or ##.
- Use --- to separate major sections.

Format the note as Markdown, with clear sections, smaller headings, bullet points, and horizontal dividers (---) between major sections. The best solution section should be the highlight and most detailed.

Problem Title: {problem['title']}
LeetCode Link: {problem['url']}
Difficulty: {problem['difficulty']}
Pattern: {problem.get('pattern', '')}

User's Java Solution (if any):
```java
{solution_code.strip() if solution_code else '// No user solution provided'}
```
'''
        note_md = call_ai_api(prompt)
        # Extract flashcards (Q;A) from the note (simple heuristic: lines starting with Q: or similar)
        flashcards = []
        for line in note_md.splitlines():
            if ";" in line and line.count(";") == 1:
                q, a = line.split(";", 1)
                if len(q.strip()) > 0 and len(a.strip()) > 0:
                    flashcards.append(f"{q.strip()};{a.strip()}")
        return note_md, flashcards

    def save_dsa_note_and_flashcards(self, problem, note_md, flashcards):
        """
        Save the note to Obsidian, add flashcards to Anki, and always export for NotebookLM. Update progress with note path, flashcards, and export status. Handle errors but do not stop the pipeline. Return a dict with status for UI feedback.
        """
        result = {"obsidian": False, "anki": False, "notebooklm": False, "note_path": None, "error": None}
        try:
            # Save note to Obsidian
            note_path = self.save_to_obsidian(
                note_md,
                f"Problems/{problem['id']} - {problem['title']}.md"
            )
            result["obsidian"] = True
            result["note_path"] = note_path
        except Exception as e:
            result["error"] = f"Obsidian save failed: {e}"
        try:
            # Save flashcards to Anki
            if flashcards:
                create_flashcards(flashcards)
                result["anki"] = True
        except Exception as e:
            result["error"] = (result["error"] or "") + f" Anki export failed: {e}"
        try:
            # Always export for NotebookLM
            from notebooklm_export import export_for_notebooklm
            export_for_notebooklm()
            result["notebooklm"] = True
        except Exception as e:
            result["error"] = (result["error"] or "") + f" NotebookLM export failed: {e}"
        # Update progress
        if "problems" in self.progress:
            if problem["id"] not in self.progress["problems"]:
                self.progress["problems"][problem["id"]] = {}
            self.progress["problems"][problem["id"]]["note_path"] = result["note_path"] if result["obsidian"] else None
            self.progress["problems"][problem["id"]]["flashcards"] = flashcards
            self.progress["problems"][problem["id"]]["notebooklm_exported"] = result["notebooklm"]
        return result
