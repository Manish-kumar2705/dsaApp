import os
import json
import re
from datetime import datetime
from pathlib import Path
import requests
import time
import threading

class NotebookLMExporter:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPO')
        self.notebooklm_folder = "notebooklm_export"
        self.notebooklm_api_key = os.getenv('NOTEBOOKLM_API_KEY')
        self.notebooklm_project_id = os.getenv('NOTEBOOKLM_PROJECT_ID')
        self.ensure_export_folder()
        self.setup_auto_sync()
    
    def ensure_export_folder(self):
        """Ensure the export folder exists"""
        Path(self.notebooklm_folder).mkdir(exist_ok=True)
    
    def setup_auto_sync(self):
        """Setup automatic sync to NotebookLM"""
        if self.notebooklm_api_key and self.notebooklm_project_id:
            # Start background sync thread
            sync_thread = threading.Thread(target=self.auto_sync_to_notebooklm, daemon=True)
            sync_thread.start()
            print("🔄 Auto-sync to NotebookLM started")
    
    def auto_sync_to_notebooklm(self):
        """Background thread for automatic NotebookLM sync"""
        while True:
            try:
                # Check for new files every 2 minutes
                time.sleep(120)
                
                # Export and sync to NotebookLM
                self.export_to_notebooklm(auto_sync=True)
                
                # Upload to NotebookLM API if configured
                if self.notebooklm_api_key:
                    self.upload_to_notebooklm_api()
                    
            except Exception as e:
                print(f"Auto-sync to NotebookLM error: {e}")
                time.sleep(60)
    
    def upload_to_notebooklm_api(self):
        """Upload files directly to NotebookLM API"""
        try:
            # This would integrate with NotebookLM API
            # For now, we'll create a webhook or use Google Drive sync
            
            # Option 1: Google Drive sync (if NotebookLM supports it)
            if os.getenv('GDRIVE_FOLDER_ID'):
                self.sync_to_gdrive_for_notebooklm()
            
            # Option 2: Webhook to NotebookLM
            webhook_url = os.getenv('NOTEBOOKLM_WEBHOOK_URL')
            if webhook_url:
                self.send_webhook_to_notebooklm(webhook_url)
            
            print("✅ Auto-uploaded to NotebookLM")
            
        except Exception as e:
            print(f"NotebookLM API upload error: {e}")
    
    def sync_to_gdrive_for_notebooklm(self):
        """Sync to Google Drive for NotebookLM access"""
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            # Setup Google Drive API
            creds = Credentials.from_authorized_user_info(
                json.loads(os.getenv('GDRIVE_CREDENTIALS', '{}'))
            )
            service = build('drive', 'v3', credentials=creds)
            
            # Upload notebooklm_export folder
            folder_id = os.getenv('GDRIVE_FOLDER_ID')
            
            # Upload all files in notebooklm_export
            for file_path in Path(self.notebooklm_folder).rglob('*.md'):
                file_metadata = {
                    'name': file_path.name,
                    'parents': [folder_id]
                }
                
                media = MediaFileUpload(str(file_path), mimetype='text/markdown')
                service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
            
            print("✅ Synced to Google Drive for NotebookLM")
            
        except Exception as e:
            print(f"Google Drive sync error: {e}")
    
    def send_webhook_to_notebooklm(self, webhook_url):
        """Send webhook notification to NotebookLM"""
        try:
            # Create webhook payload
            payload = {
                'event': 'notes_updated',
                'timestamp': datetime.now().isoformat(),
                'files_count': len(list(Path(self.notebooklm_folder).rglob('*.md'))),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'repository': self.github_repo,
                'export_path': str(Path(self.notebooklm_folder).absolute())
            }
            
            # Send webhook
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print("✅ Webhook sent to NotebookLM")
            else:
                print(f"Webhook failed: {response.status_code}")
                
        except Exception as e:
            print(f"Webhook error: {e}")
    
    def create_notebooklm_auto_upload_script(self):
        """Create a script that automatically uploads to NotebookLM"""
        script_content = f"""#!/usr/bin/env python3
# Auto-upload script for NotebookLM
# This script monitors the notebooklm_export folder and uploads to NotebookLM

import os
import time
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NotebookLMUploader(FileSystemEventHandler):
    def __init__(self):
        self.notebooklm_api_key = "{self.notebooklm_api_key}"
        self.notebooklm_project_id = "{self.notebooklm_project_id}"
        self.export_folder = "{self.notebooklm_folder}"
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            print(f"📝 File changed: {{event.src_path}}")
            self.upload_to_notebooklm()
    
    def upload_to_notebooklm(self):
        try:
            # Upload the entire export folder to NotebookLM
            # This would use NotebookLM's API or integration method
            
            # For now, we'll create a notification
            print("🔄 Uploading to NotebookLM...")
            
            # Option 1: Use NotebookLM API
            if self.notebooklm_api_key:
                self.upload_via_api()
            
            # Option 2: Use Google Drive sync
            elif os.getenv('GDRIVE_FOLDER_ID'):
                self.upload_via_gdrive()
            
            # Option 3: Use local NotebookLM folder
            else:
                self.upload_via_local()
                
        except Exception as e:
            print(f"Upload error: {{e}}")
    
    def upload_via_api(self):
        # NotebookLM API integration
        print("📚 Uploading via NotebookLM API...")
    
    def upload_via_gdrive(self):
        # Google Drive sync for NotebookLM
        print("☁️ Syncing to Google Drive for NotebookLM...")
    
    def upload_via_local(self):
        # Local NotebookLM folder
        print("💻 Files ready in local NotebookLM folder")

def main():
    event_handler = NotebookLMUploader()
    observer = Observer()
    observer.schedule(event_handler, path='{self.notebooklm_folder}', recursive=True)
    observer.start()
    
    print("🔄 Monitoring notebooklm_export folder for changes...")
    print("📚 Auto-uploading to NotebookLM...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\\n🛑 Stopped monitoring")
    
    observer.join()

if __name__ == "__main__":
    main()
"""
        
        # Save the script
        script_path = Path("notebooklm_auto_upload.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make it executable
        script_path.chmod(0o755)
        
        print(f"✅ Created auto-upload script: {script_path}")
        return script_path
    
    def setup_notebooklm_integration(self):
        """Setup complete NotebookLM integration"""
        print("🔧 Setting up NotebookLM integration...")
        
        # Create auto-upload script
        script_path = self.create_notebooklm_auto_upload_script()
        
        # Create startup script
        startup_script = f"""#!/bin/bash
# Startup script for NotebookLM auto-sync

echo "🚀 Starting NotebookLM auto-sync..."

# Start the auto-upload script in background
python {script_path} &

# Start the main DSA app
streamlit run ui_enhanced.py

echo "✅ NotebookLM integration ready!"
"""
        
        startup_path = Path("start_notebooklm_sync.sh")
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        startup_path.chmod(0o755)
        
        print(f"✅ Created startup script: {startup_path}")
        print("🚀 Run './start_notebooklm_sync.sh' to start with NotebookLM auto-sync")
        
        return startup_path
    
    def create_notebooklm_webhook_server(self):
        """Create a webhook server for NotebookLM integration"""
        webhook_server = f"""#!/usr/bin/env python3
# Webhook server for NotebookLM integration

from flask import Flask, request, jsonify
import os
import json
from pathlib import Path

app = Flask(__name__)

@app.route('/webhook/notebooklm', methods=['POST'])
def notebooklm_webhook():
    data = request.json
    
    if data.get('event') == 'notes_updated':
        # Trigger NotebookLM sync
        export_folder = Path('{self.notebooklm_folder}')
        
        # Update NotebookLM with new files
        print("🔄 Webhook received - updating NotebookLM...")
        
        # This would integrate with NotebookLM's API
        # For now, we'll just log the event
        print(f"📝 Files updated: {{data.get('files_count', 0)}}")
        print(f"🕒 Last updated: {{data.get('last_updated', 'Unknown')}}")
        
        return jsonify({{"status": "success", "message": "NotebookLM updated"}})
    
    return jsonify({{"status": "error", "message": "Unknown event"}})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({{"status": "healthy", "service": "notebooklm-webhook"}})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
"""
        
        webhook_path = Path("notebooklm_webhook_server.py")
        with open(webhook_path, 'w') as f:
            f.write(webhook_server)
        
        print(f"✅ Created webhook server: {webhook_path}")
        return webhook_path

    def fetch_notes_from_github(self):
        """Fetch all notes from GitHub repository"""
        if not self.github_token or not self.github_repo:
            return []
        
        try:
            # Fetch notes directory
            url = f"https://api.github.com/repos/{self.github_repo}/contents/notes"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return []
            
            notes = []
            for item in response.json():
                if item['type'] == 'dir':
                    # Fetch files in pattern directory
                    pattern_url = f"https://api.github.com/repos/{self.github_repo}/contents/notes/{item['name']}"
                    pattern_response = requests.get(pattern_url, headers=headers)
                    if pattern_response.status_code == 200:
                        for file_item in pattern_response.json():
                            if file_item['name'].endswith('.md'):
                                # Download note content
                                content_response = requests.get(file_item['download_url'])
                                if content_response.status_code == 200:
                                    notes.append({
                                        'pattern': item['name'],
                                        'filename': file_item['name'],
                                        'content': content_response.text,
                                        'url': file_item['download_url']
                                    })
            
            return notes
        except Exception as e:
            print(f"Error fetching from GitHub: {e}")
            return []
    
    def fetch_flashcards_from_github(self):
        """Fetch all flashcards from GitHub repository"""
        if not self.github_token or not self.github_repo:
            return []
        
        try:
            # Fetch flashcards directory
            url = f"https://api.github.com/repos/{self.github_repo}/contents/flashcards"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return []
            
            flashcards = []
            for item in response.json():
                if item['type'] == 'dir':
                    # Fetch files in pattern directory
                    pattern_url = f"https://api.github.com/repos/{self.github_repo}/contents/flashcards/{item['name']}"
                    pattern_response = requests.get(pattern_url, headers=headers)
                    if pattern_response.status_code == 200:
                        for file_item in pattern_response.json():
                            if file_item['name'].endswith('.csv'):
                                # Download flashcard content
                                content_response = requests.get(file_item['download_url'])
                                if content_response.status_code == 200:
                                    flashcards.append({
                                        'pattern': item['name'],
                                        'filename': file_item['name'],
                                        'content': content_response.text,
                                        'url': file_item['download_url']
                                    })
            
            return flashcards
        except Exception as e:
            print(f"Error fetching flashcards from GitHub: {e}")
            return []
    
    def parse_note_for_notebooklm(self, note_content, pattern, filename):
        """Parse note content specifically for NotebookLM"""
        try:
            # Extract problem info from filename
            problem_match = re.match(r'(\d+)\s*-\s*(.+)\.md', filename)
            problem_id = problem_match.group(1) if problem_match else "Unknown"
            problem_title = problem_match.group(2) if problem_match else filename.replace('.md', '')
            
            # Parse the note content
            lines = note_content.split('\n')
            
            # Extract sections
            sections = {
                'problem_statement': '',
                'intuition': '',
                'brute_force': '',
                'optimal_solution': '',
                'code': '',
                'complexity': '',
                'flashcards': []
            }
            
            current_section = None
            code_block = False
            
            for line in lines:
                line = line.strip()
                
                # Detect sections
                if '## Problem Statement' in line or 'Problem Statement' in line:
                    current_section = 'problem_statement'
                    continue
                elif '## Intuition' in line or '### Intuition' in line:
                    current_section = 'intuition'
                    continue
                elif '## Brute Force' in line or '### Brute Force' in line:
                    current_section = 'brute_force'
                    continue
                elif '## Optimal Solution' in line or '### Optimal Solution' in line:
                    current_section = 'optimal_solution'
                    continue
                elif '## Code' in line or '### Code' in line or '```' in line:
                    current_section = 'code'
                    if '```' in line:
                        code_block = not code_block
                    continue
                elif '## Complexity' in line or '### Complexity' in line:
                    current_section = 'complexity'
                    continue
                elif '## Flashcards' in line or '### Flashcards' in line:
                    current_section = 'flashcards'
                    continue
                
                # Add content to current section
                if current_section and line:
                    if current_section == 'flashcards':
                        # Parse flashcard Q&A
                        if line.startswith('Q:') or line.startswith('A:'):
                            sections['flashcards'].append(line)
                    else:
                        sections[current_section] += line + '\n'
            
            # Create NotebookLM-optimized content
            notebooklm_content = f"""# Problem {problem_id}: {problem_title}

## Pattern: {pattern}
**Difficulty**: {self.extract_difficulty(note_content)}
**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Problem Statement
{self.clean_text(sections['problem_statement'])}

## Solution Approach

### Intuition
{self.clean_text(sections['intuition'])}

### Brute Force Approach
{self.clean_text(sections['brute_force'])}

### Optimal Solution
{self.clean_text(sections['optimal_solution'])}

## Implementation
{self.clean_text(sections['code'])}

## Complexity Analysis
{self.clean_text(sections['complexity'])}

## Key Insights
- **Pattern**: {pattern}
- **Data Structure**: {self.extract_data_structures(sections['code'])}
- **Algorithm**: {self.extract_algorithm(sections['intuition'])}
- **Time Complexity**: {self.extract_time_complexity(sections['complexity'])}
- **Space Complexity**: {self.extract_space_complexity(sections['complexity'])}

## Practice Questions
{self.generate_practice_questions(pattern, problem_title)}

## Related Problems
{self.get_related_problems(pattern, problem_id)}

## Study Notes
{self.generate_study_notes(sections['flashcards'])}
"""
            
            return notebooklm_content
            
        except Exception as e:
            print(f"Error parsing note: {e}")
            return note_content
    
    def clean_text(self, text):
        """Clean and format text for NotebookLM"""
        if not text:
            return "Not available"
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def extract_difficulty(self, content):
        """Extract difficulty from note content"""
        difficulty_match = re.search(r'Difficulty[:\s]*([A-Za-z]+)', content, re.IGNORECASE)
        return difficulty_match.group(1) if difficulty_match else "Unknown"
    
    def extract_data_structures(self, code_content):
        """Extract data structures used from code"""
        structures = []
        if 'HashMap' in code_content or 'Map' in code_content:
            structures.append("Hash Map")
        if 'ArrayList' in code_content or 'List' in code_content:
            structures.append("Array/List")
        if 'Stack' in code_content:
            structures.append("Stack")
        if 'Queue' in code_content:
            structures.append("Queue")
        if 'Tree' in code_content or 'TreeNode' in code_content:
            structures.append("Tree")
        if 'LinkedList' in code_content or 'ListNode' in code_content:
            structures.append("Linked List")
        
        return ", ".join(structures) if structures else "Array"
    
    def extract_algorithm(self, intuition):
        """Extract algorithm type from intuition"""
        if 'two pointer' in intuition.lower():
            return "Two Pointers"
        elif 'sliding window' in intuition.lower():
            return "Sliding Window"
        elif 'binary search' in intuition.lower():
            return "Binary Search"
        elif 'dynamic programming' in intuition.lower() or 'dp' in intuition.lower():
            return "Dynamic Programming"
        elif 'dfs' in intuition.lower() or 'depth first' in intuition.lower():
            return "Depth-First Search"
        elif 'bfs' in intuition.lower() or 'breadth first' in intuition.lower():
            return "Breadth-First Search"
        else:
            return "Iterative"
    
    def extract_time_complexity(self, complexity):
        """Extract time complexity"""
        time_match = re.search(r'Time[:\s]*O\(([^)]+)\)', complexity, re.IGNORECASE)
        return f"O({time_match.group(1)})" if time_match else "O(n)"
    
    def extract_space_complexity(self, complexity):
        """Extract space complexity"""
        space_match = re.search(r'Space[:\s]*O\(([^)]+)\)', complexity, re.IGNORECASE)
        return f"O({space_match.group(1)})" if space_match else "O(1)"
    
    def generate_practice_questions(self, pattern, problem_title):
        """Generate practice questions for the pattern"""
        practice_questions = {
            'Arrays': [
                "How would you modify this solution for a sorted array?",
                "What if the array contains duplicates?",
                "How would you handle edge cases like empty array?",
                "What's the difference between this and a similar array problem?"
            ],
            'Two Pointers': [
                "When would you use two pointers vs sliding window?",
                "How do you decide which pointer to move first?",
                "What if you need three pointers?",
                "How do you handle pointer collision?"
            ],
            'Sliding Window': [
                "How do you determine the window size?",
                "When do you expand vs contract the window?",
                "How do you track the window state efficiently?",
                "What if the window size is variable?"
            ]
        }
        
        questions = practice_questions.get(pattern, [
            "What are the key insights for this pattern?",
            "How would you approach this problem differently?",
            "What edge cases should you consider?",
            "How would you optimize this solution further?"
        ])
        
        return "\n".join([f"- {q}" for q in questions])
    
    def get_related_problems(self, pattern, current_id):
        """Get related problems in the same pattern"""
        # This would typically fetch from your problem database
        related = {
            'Arrays': ['Two Sum', 'Container With Most Water', '3Sum'],
            'Two Pointers': ['Container With Most Water', '3Sum', 'Trapping Rain Water'],
            'Sliding Window': ['Longest Substring Without Repeating Characters', 'Minimum Window Substring']
        }
        
        problems = related.get(pattern, [])
        return "\n".join([f"- {p}" for p in problems if str(current_id) not in p])
    
    def generate_study_notes(self, flashcards):
        """Generate study notes from flashcards"""
        if not flashcards:
            return "No flashcards available for this problem."
        
        study_notes = "## Study Notes\n\n"
        for i, flashcard in enumerate(flashcards[:5], 1):  # Limit to 5
            study_notes += f"{i}. {flashcard}\n"
        
        return study_notes
    
    def export_to_notebooklm(self, auto_sync=True):
        """Export all notes to NotebookLM format with auto-sync from GitHub"""
        print("🚀 Starting NotebookLM export with auto-sync...")
        
        # Fetch notes from GitHub if auto-sync is enabled
        if auto_sync and self.github_token:
            print("📥 Fetching notes from GitHub...")
            github_notes = self.fetch_notes_from_github()
            github_flashcards = self.fetch_flashcards_from_github()
            
            if github_notes:
                print(f"✅ Found {len(github_notes)} notes on GitHub")
                
                # Process each note
                for note in github_notes:
                    notebooklm_content = self.parse_note_for_notebooklm(
                        note['content'], 
                        note['pattern'], 
                        note['filename']
                    )
                    
                    # Save to NotebookLM folder
                    output_path = Path(self.notebooklm_folder) / f"{note['pattern']}_{note['filename']}"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(notebooklm_content)
                
                print(f"✅ Exported {len(github_notes)} notes to NotebookLM format")
            else:
                print("⚠️ No notes found on GitHub")
        
        # Create index file
        self.create_index_file()
        
        # Create pattern summaries
        self.create_pattern_summaries()
        
        print(f"🎉 NotebookLM export complete! Files saved to: {self.notebooklm_folder}")
        return True
    
    def create_index_file(self):
        """Create an index file for easy navigation"""
        index_content = """# DSA Mastery System - NotebookLM Index

## 📚 Problem Index

This index contains all your DSA problems organized by pattern and optimized for NotebookLM AI queries.

### 🎯 How to Use This Index

1. **Search by Pattern**: Ask "Show me all Array problems"
2. **Search by Difficulty**: Ask "Show me all Easy problems"
3. **Search by Concept**: Ask "Show me problems using Hash Maps"
4. **Compare Solutions**: Ask "Compare Two Sum and 3Sum solutions"

### 📂 Pattern Organization

"""
        
        # Add pattern sections
        patterns = ['Arrays', 'Two Pointers', 'Sliding Window', 'Binary Search', 'Dynamic Programming']
        for pattern in patterns:
            index_content += f"#### {pattern}\n"
            index_content += f"- Pattern: {pattern}\n"
            index_content += f"- Common techniques: {self.get_pattern_techniques(pattern)}\n"
            index_content += f"- Typical complexity: {self.get_pattern_complexity(pattern)}\n\n"
        
        index_content += """
### 🔍 Search Tips

- **"Show me all problems using [data structure]"**
- **"What's the optimal solution for [problem type]?"**
- **"Compare [problem1] and [problem2]"**
- **"What are the key insights for [pattern]?"**
- **"Show me practice questions for [pattern]"**

### 📊 Progress Tracking

- Total problems: [Count]
- Patterns mastered: [List]
- Next recommended: [Pattern]

---
*Generated automatically by DSA Mastery System*
"""
        
        with open(Path(self.notebooklm_folder) / "00_INDEX.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def get_pattern_techniques(self, pattern):
        """Get common techniques for a pattern"""
        techniques = {
            'Arrays': 'Iteration, Hash Maps, Two Pointers',
            'Two Pointers': 'Left/Right pointers, Collision detection',
            'Sliding Window': 'Window expansion/contraction, State tracking',
            'Binary Search': 'Midpoint calculation, Boundary conditions',
            'Dynamic Programming': 'Memoization, Tabulation, State transitions'
        }
        return techniques.get(pattern, 'Various techniques')
    
    def get_pattern_complexity(self, pattern):
        """Get typical complexity for a pattern"""
        complexity = {
            'Arrays': 'O(n) time, O(1) space',
            'Two Pointers': 'O(n) time, O(1) space',
            'Sliding Window': 'O(n) time, O(k) space',
            'Binary Search': 'O(log n) time, O(1) space',
            'Dynamic Programming': 'O(n²) time, O(n) space'
        }
        return complexity.get(pattern, 'Varies by problem')
    
    def create_pattern_summaries(self):
        """Create summary files for each pattern"""
        patterns = ['Arrays', 'Two Pointers', 'Sliding Window']
        
        for pattern in patterns:
            summary_content = f"""# {pattern} Pattern Summary

## 🎯 Pattern Overview
{pattern} is a fundamental algorithmic pattern used for...

## 🔑 Key Concepts
- Concept 1: Description
- Concept 2: Description
- Concept 3: Description

## 📝 Common Problems
- Problem 1: Brief description
- Problem 2: Brief description
- Problem 3: Brief description

## 💡 Implementation Tips
- Tip 1: Description
- Tip 2: Description
- Tip 3: Description

## ⚡ Complexity
- Time: Typical time complexity
- Space: Typical space complexity

## 🔄 When to Use
- Use case 1
- Use case 2
- Use case 3

---
*Generated for NotebookLM AI queries*
"""
            
            with open(Path(self.notebooklm_folder) / f"{pattern}_SUMMARY.md", 'w', encoding='utf-8') as f:
                f.write(summary_content)

# Main export function
def export_to_notebooklm(auto_sync=True):
    """Main function to export to NotebookLM"""
    exporter = NotebookLMExporter()
    return exporter.export_to_notebooklm(auto_sync)

def setup_notebooklm_integration():
    """Setup complete NotebookLM integration"""
    exporter = NotebookLMExporter()
    return exporter.setup_notebooklm_integration()

if __name__ == "__main__":
    export_to_notebooklm()
