# run_jobs.py

from agents.job_application.job_scraper_agent import JobScraperAgent
from agents.job_application.cv_cl_generator_agent import CVCLGeneratorAgent
from datetime import datetime
from pathlib import Path
import json
import os

# ✅ Config-style constant
RESUME_PATH = Path("documents/resumes/CV.pdf")

def run_jobs():
    print("🧠 Starting job application pipeline...\n")

    try:
        job_scraper = JobScraperAgent(name="JobScraper", pdf_path=str(RESUME_PATH))
        print("🔍 Running job scraper...")
        scraper_result = job_scraper.receive_message({"content": "scrape", "type": "command"})
    except Exception as e:
        print(f"❌ Failed to run job scraper: {e}")
        return

    if scraper_result.get("type") != "response" or "jobs" not in scraper_result or not scraper_result["jobs"]:
        print("⚠️ No jobs found.")
        return

    try:
        print(f"📝 Generating CVs and Cover Letters for {len(scraper_result['jobs'])} jobs...")
        cvcl_generator = CVCLGeneratorAgent(name="CVCLGenerator")
        generator_result = cvcl_generator.receive_message(scraper_result)
    except Exception as e:
        print(f"❌ CV/CL generation failed: {e}")
        return

    if generator_result.get("type") != "response":
        print("❌ Generator failed to return valid results.")
        return

    results = generator_result["results"]

    for idx, result in enumerate(results):
        job = result["job"]
        print("=" * 60)
        print(f"📌 {idx+1}. {job['title']} at {job['company']}")
        print(f"🔗 {job['url']}")
        print(f"🧾 CV:\n{result['cv']}\n")
        print(f"✉️ Cover Letter:\n{result['cover_letter']}")
        print("=" * 60 + "\n")

    # ✅ Save to dated output folder
    output_dir = Path("data/generated_applications") / datetime.now().strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "applications.json"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"📁 Saved to: {output_path}")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")

if __name__ == "__main__":
    run_jobs()
