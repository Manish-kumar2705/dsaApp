import os
import shutil
from config import OBSIDIAN_VAULT

def export_for_notebooklm():
    """Prepare notes for NotebookLM import"""
    export_dir = "notebooklm_export"
    os.makedirs(export_dir, exist_ok=True)
    
    # Copy pattern primers
    patterns_src = os.path.join(OBSIDIAN_VAULT, "Patterns")
    patterns_dest = os.path.join(export_dir, "Patterns")
    if os.path.exists(patterns_src):
        shutil.copytree(patterns_src, patterns_dest, dirs_exist_ok=True)
    
    # Copy problem notes
    problems_src = os.path.join(OBSIDIAN_VAULT, "Problems")
    problems_dest = os.path.join(export_dir, "Problems")
    if os.path.exists(problems_src):
        shutil.copytree(problems_src, problems_dest, dirs_exist_ok=True)
    
    # Create index file
    with open(os.path.join(export_dir, "!index.md"), "w") as f:
        f.write("# DSA Mastery Collection\n\n")
        f.write("## Patterns\n")
        for file in os.listdir(patterns_dest):
            if file.endswith(".md"):
                f.write(f"- [[Patterns/{file}]]\n")
        
        f.write("\n## Problems\n")
        for file in os.listdir(problems_dest):
            if file.endswith(".md"):
                f.write(f"- [[Problems/{file}]]\n")
    
    print(f"Exported to {export_dir} for NotebookLM import")
