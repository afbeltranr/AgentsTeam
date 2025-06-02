# run_jobs.py

from agents.job_application.job_scraper_agent import JobScraperAgent
from agents.job_application.cv_cl_generator_agent import CVCLGeneratorAgent
from pathlib import Path
import json

def run_jobs():
    # Step 1: Run job scraper
    pdf_path = Path("documents/resumes/CV.pdf")
    job_scraper = JobScraperAgent(name="JobScraper", pdf_path=str(pdf_path))

    print("🔍 Running job scraper...")
    scraper_result = job_scraper.receive_message({"content": "scrape", "type": "command"})

    if scraper_result.get("type") != "response" or "jobs" not in scraper_result:
        print("❌ Job scraper failed or returned no jobs.")
        return

    # Step 2: Run CV/CL generator
    print(f"📝 Generating CVs and Cover Letters for {len(scraper_result['jobs'])} jobs...")
    cvcl_generator = CVCLGeneratorAgent(name="CVCLGenerator")
    generator_result = cvcl_generator.receive_message(scraper_result)

    if generator_result.get("type") != "response":
        print("❌ CV/CL Generator failed.")
        return

    results = generator_result["results"]
    print(f"✅ Generated {len(results)} CV and cover letter pairs.\n")

    # Step 3: Print summaries
    for idx, result in enumerate(results):
        job = result["job"]
        print("=" * 60)
        print(f"📌 {idx+1}. {job['title']} at {job['company']}")
        print(f"🔗 URL: {job['url']}")
        print(f"🧾 CV:\n{result['cv']}\n")
        print(f"✉️ Cover Letter:\n{result['cover_letter']}")
        print("=" * 60 + "\n")

    # Optional: Save to JSON
    with open("data/generated_applications.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("📁 Saved results to data/generated_applications.json")

if __name__ == "__main__":
    run_jobs()
