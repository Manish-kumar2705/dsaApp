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
    "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack",
    "Binary Search", "Linked List", "Tree", "Trie", "Heap",
    "Backtracking", "Graph", "Dynamic Programming", "Greedy",
    "Math & Geometry", "Bit Manipulation"
]

# Define the recommended learning order for DSA patterns
DSA_LEARNING_ORDER = [
    "Arrays & Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Tries",
    "Heap / Priority Queue",
    "Backtracking",
    "Graphs",
    "Advanced Graphs",
    "1-D Dynamic Programming",
    "2-D Dynamic Programming",
    "Greedy",
    "Intervals",
    "Math & Geometry",
    "Bit Manipulation"
]

class DSAMasterySystem:
    """Core system for DSA practice and note management"""
    
    # Define the recommended learning order for DSA patterns
    DSA_LEARNING_ORDER = [
        "Arrays & Hashing",
        "Two Pointers",
        "Sliding Window",
        "Stack",
        "Binary Search",
        "Linked List",
        "Trees",
        "Tries",
        "Heap / Priority Queue",
        "Backtracking",
        "Graphs",
        "Advanced Graphs",
        "1-D Dynamic Programming",
        "2-D Dynamic Programming",
        "Greedy",
        "Intervals",
        "Math & Geometry",
        "Bit Manipulation"
    ]
    
    def __init__(self):
        """Initialize the system"""
        self.progress = self.load_progress()
        self.neetcode = self.load_neetcode()
        self.ensure_directories()
        self._ensure_patterns()
        
        # Initialize current pattern if not set
        if "current_pattern" not in self.progress["stats"]:
            self.progress["stats"]["current_pattern"] = self.get_all_patterns()[0]
        self._save_progress()

    def load_progress(self):
        """Load progress from file or create new if not exists"""
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading progress: {e}")
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
    
    def analyze_solution(self, problem, solution_code):
        """Analyze a solution for correctness, complexity, and generate improvement suggestions"""
        prompt = f"""You are a senior software engineer and DSA expert. Analyze this {problem['title']} solution:

CODE TO ANALYZE:
```
{solution_code}
```

PROBLEM LINK: {problem['url']}

Provide a detailed analysis in this format:
1. CORRECTNESS
- Is the solution logically correct?
- Does it handle edge cases?
- Any potential bugs or issues?

2. COMPLEXITY ANALYSIS
- Time complexity with explanation
- Space complexity with explanation
- Could we optimize further?

3. CODE QUALITY
- Code style and readability
- Variable naming
- Comments and documentation
- Any code smells?

4. APPROACH ANALYSIS
- What pattern/technique is used?
- Why is this approach good/bad?
- Alternative approaches?

5. LEARNING POINTS
- Key insights from this solution
- Common pitfalls to avoid
- Similar problems to practice

6. IMPROVEMENT SUGGESTIONS
- Specific ways to optimize
- Better approaches to consider
- Code quality improvements

Format your response in Markdown with clear sections and code examples where relevant.
"""
        return call_ai_api(prompt)

    def generate_full_notes(self, problem, analysis):
        """Generate comprehensive DSA notes including problem, solution, and analysis"""
        prompt = f"""You are a DSA expert creating detailed study notes. Generate comprehensive notes for this problem:

PROBLEM: {problem['title']}
URL: {problem['url']}
PATTERN: {problem.get('pattern', 'Unknown')}

ANALYSIS:
{analysis}

Create detailed notes in this format:

# {problem['title']}

## Problem Understanding
- Clear explanation of the problem
- Key constraints and requirements
- Example walkthrough with visualization
- Edge cases to consider

## Approach
- Intuition behind the solution
- Step-by-step solution strategy
- Why this approach works
- Pattern recognition tips

## Solution Breakdown
- Detailed code explanation
- Key steps highlighted
- Important variables/data structures
- Critical algorithm steps

## Complexity Analysis
- Time complexity with explanation
- Space complexity with explanation
- Optimization possibilities

## Implementation Details
- Code implementation tips
- Common pitfalls to avoid
- Best practices to follow
- Important edge cases

## Learning Points
- Key takeaways
- Similar problems
- Pattern application
- Interview tips

## Code
```java
// Include fully commented solution
```

Format in clean Markdown with:
- Clear headings
- Bullet points for readability
- Code snippets where helpful
- Visual explanations if needed

Make it comprehensive but focused - each section should provide unique value."""
        return call_ai_api(prompt)

    def generate_code_explanation(self, problem, code, language):
        """Generate a detailed explanation of the code solution"""
        prompt = f"""As a DSA expert, explain this {problem['title']} solution in detail:

CODE:
```{language}
{code}
```

Provide a thorough explanation in this format:

1. SOLUTION OVERVIEW
- High-level approach
- Key algorithm/data structures used
- Why this approach works

2. CODE WALKTHROUGH
- Line-by-line explanation
- Key variables and their roles
- Critical sections highlighted
- Edge case handling

3. COMPLEXITY ANALYSIS
- Time complexity breakdown
- Space complexity breakdown
- Optimization opportunities

4. IMPLEMENTATION INSIGHTS
- Clever tricks used
- Important decisions explained
- Alternative approaches
- Potential improvements

5. LEARNING POINTS
- Key takeaways
- Similar patterns
- Common mistakes to avoid
- Interview tips

Make it detailed but clear, using:
- Simple language
- Step-by-step explanations
- Examples where helpful
- Clear formatting

Focus on helping others understand both the approach and implementation details."""
        return call_ai_api(prompt)

    def auto_detect_pattern(self, problem):
        """Auto-detect the DSA pattern for a problem"""
        prompt = f"""As a DSA expert, analyze this problem and determine its core pattern:

PROBLEM: {problem['title']}
URL: {problem['url']}

Available patterns:
{', '.join(self.DSA_LEARNING_ORDER)}

Determine:
1. Primary pattern used
2. Why this pattern fits
3. Any secondary patterns

Return ONLY the primary pattern name exactly as shown in the list above. No explanation needed."""
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
        
        self._save_progress()
        
        return full_notes

    def _save_progress(self):
        """Save progress to file"""
        try:
            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")

    def update_progress(self, problem_id, status, pattern=None):
        """Update progress for a problem"""
        if problem_id not in self.progress["problems"]:
            self.progress["problems"][problem_id] = {}
        
        self.progress["problems"][problem_id].update({
            "status": status,
            "date": datetime.now().isoformat(),
            "pattern": pattern
        })
        
        # Update pattern stats
        if pattern:
            if pattern not in self.progress["patterns"]:
                self.progress["patterns"][pattern] = {"solved": 0, "attempted": 0}
            if status.lower() == "completed":
                self.progress["patterns"][pattern]["solved"] += 1
            self.progress["patterns"][pattern]["attempted"] += 1
        
        # Update global stats
        self.progress["stats"]["solved"] = len([p for p in self.progress["problems"].values() if p.get("status", "").lower() == "completed"])
        self.progress["stats"]["last_run"] = datetime.now().isoformat()
        
        self._save_progress()

    def get_progress(self):
        """Get current progress stats"""
        return {
            "total_problems": len(self.neetcode),
            "solved": self.progress["stats"]["solved"],
            "streak": self.progress["stats"].get("streak", 0),
            "patterns": self.progress["patterns"],
            "last_run": self.progress["stats"]["last_run"]
        }

    def get_patterns(self):
        """Return a sorted list of all patterns in the problem set."""
        return self.get_all_patterns()

    def get_all_patterns(self):
        """Get list of all available patterns"""
        return sorted(list(set([p.get("pattern", "") for p in self.neetcode if p.get("pattern")])))

    def get_problems_by_pattern(self, pattern=None):
        """Get all problems for a specific pattern"""
        if pattern is None or pattern.lower() == "any":
            return self.neetcode
        return [p for p in self.neetcode if str(p.get("pattern", "")).lower() == pattern.lower()]

    def get_next_pattern(self):
        """Return the next pattern with unsolved problems, or None if all done."""
        patterns = self.get_all_patterns()
        for pattern in patterns:
            problems = self.get_problems_by_pattern(pattern)
            if any(str(p.get("status", "")).lower() != "completed" for p in problems):
                return pattern
        return None

    def _ensure_patterns(self):
        """Ensure every problem has a pattern assigned"""
        # Define category to pattern mapping
        category_to_pattern = {
            "Arrays": "Arrays & Hashing",
            "Two Pointers": "Two Pointers",
            "Sliding Window": "Sliding Window",
            "Stack": "Stack",
            "Binary Search": "Binary Search",
            "Linked List": "Linked List",
            "Trees": "Tree",
            "Tries": "Trie",
            "Heap/Priority Queue": "Heap",
            "Backtracking": "Backtracking",
            "Graphs": "Graph",
            "Advanced Graphs": "Graph",
            "1-D DP": "Dynamic Programming",
            "2-D DP": "Dynamic Programming",
            "Greedy": "Greedy",
            "Intervals": "Arrays & Hashing",
            "Math & Geometry": "Math & Geometry",
            "Bit Manipulation": "Bit Manipulation"
        }
        
        for problem in self.neetcode:
            if not problem.get("pattern"):
                # Use category mapping as fallback if no pattern is set
                category = problem.get("category", "")
                problem["pattern"] = category_to_pattern.get(category, category)
                
                # If still no pattern, try to detect it
                if not problem["pattern"]:
                    problem["pattern"] = self.auto_detect_pattern(problem)
        
        # Save updated problems
        with open(NEETCODE_FILE, "w") as f:
            json.dump(self.neetcode, f, indent=2)

    def get_current_pattern(self):
        """Get the current pattern being studied"""
        return self.progress["stats"].get("current_pattern", self.get_all_patterns()[0])

    def set_current_pattern(self, pattern):
        """Set the current pattern to study"""
        if pattern in self.get_all_patterns():
            self.progress["stats"]["current_pattern"] = pattern
            self._save_progress()
            return True
        return False

    def get_next_unsolved_in_pattern(self, pattern):
        """Get the next unsolved problem in the given pattern"""
        if not pattern:
            return None
        pattern_problems = self.get_problems_by_pattern(pattern)
        for problem in pattern_problems:
            if str(problem.get("status", "")).lower() != "completed":
                return problem
        return None

    def get_learning_order(self):
        """Get the recommended learning order for DSA patterns"""
        return self.DSA_LEARNING_ORDER
    
    def get_pattern_index(self, pattern):
        """Get the index of a pattern in the learning order"""
        try:
            return self.DSA_LEARNING_ORDER.index(pattern)
        except ValueError:
            return -1
    
    def get_today_problem(self, pattern=None):
        """Return the planned problem for today: next unsolved in selected pattern (or next pattern if not specified)"""
        if pattern is None:
            pattern = self.get_next_pattern()
        return self.get_next_unsolved_in_pattern(pattern)
    
    def generate_dsa_note(self, problem, solution_code):
        """Generate a comprehensive DSA note for the given problem and solution"""
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
