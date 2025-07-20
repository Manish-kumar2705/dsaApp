import pandas as pd
import json

def extract_neetcode_json(xlsx_path, sheet_name="Neetcode List", output_json="neetcode_150.json"):
    # Load the Excel sheet
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    
    # Clean and prepare data
    # Assuming columns: Category, Name, Status, Link, Notes, Comment, Doubt
    problems = []
    for idx, row in df.iterrows():
        problem = {
            "id": f"NC{idx+1}",
            "category": row.get("Category", ""),
            "title": row.get("Name", ""),
            "status": row.get("Status", ""),
            "url": row.get("Link", ""),
            "notes": row.get("Notes", ""),
            "comment": row.get("Comment", ""),
            "doubt": row.get("Doubt", ""),
            "description": row.get("Notes", ""),  # Using Notes as description placeholder
            "difficulty": "Medium",  # Default difficulty, can be updated later
            "pattern": ""  # To be auto-detected
        }
        problems.append(problem)
    
    # Save to JSON
    with open(output_json, "w") as f:
        json.dump(problems, f, indent=2)
    print(f"Extracted {len(problems)} problems to {output_json}")

if __name__ == "__main__":
    extract_neetcode_json("Amazon_Interview_Prep_Plan2.xlsx")
