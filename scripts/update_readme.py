import json
from datetime import datetime
from pathlib import Path

README_PATH = Path("README.md")
APPLICATIONS_JSON = Path("data/generated_applications") / datetime.today().strftime("%Y-%m-%d") / "applications.json"

def generate_summary_table(applications):
    lines = ["| # | Job Title | Company | Cover Letter Preview |",
             "|---|-----------|---------|-----------------------|"]
    for i, item in enumerate(applications, 1):
        job = item["job"]
        preview = item["cover_letter"].replace("\n", " ").strip()
        preview = preview if len(preview) < 60 else preview[:57] + "..."
        lines.append(f"| {i} | [{job['title']}]({job['url']}) | {job['company']} | {preview} |")
    return "\n".join(lines)

def update_readme(applications):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- AUTO-UPDATE:START -->"
    end_tag = "<!-- AUTO-UPDATE:END -->"

    if start_tag not in content or end_tag not in content:
        print("Missing AUTO-UPDATE tags in README.md")
        return

    summary_table = generate_summary_table(applications)
    new_content = content.split(start_tag)[0] + start_tag + "\n\n" + summary_table + "\n\n" + end_tag + content.split(end_tag)[1]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    if not APPLICATIONS_JSON.exists():
        print("No applications.json found for today.")
    else:
        with open(APPLICATIONS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        update_readme(data)
