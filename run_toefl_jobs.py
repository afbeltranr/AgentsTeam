# run_toefl_jobs.py

from agents.job_application.toefl_job_scraper_agent import TOEFLJobScraperAgent
from agents.job_application.markdown_generator_agent import MarkdownGeneratorAgent
from pathlib import Path
import json

# ✅ Config-style constant
RESUME_PATH = Path("documents/resumes/CV.pdf")

def run_toefl_jobs():
    print("💼 Starting TOEFL jobs search pipeline...\n")

    try:
        # Initialize TOEFL job scraper
        toefl_job_scraper = TOEFLJobScraperAgent(name="TOEFLJobScraper", pdf_path=str(RESUME_PATH))
        print("🔍 Running TOEFL job scraper...")
        scraper_result = toefl_job_scraper.receive_message({"content": "scrape", "type": "command"})
    except Exception as e:
        print(f"❌ Failed to run TOEFL job scraper: {e}")
        return

    if scraper_result.get("type") != "response" or "jobs" not in scraper_result or not scraper_result["jobs"]:
        print("⚠️ No TOEFL-relevant jobs found.")
        return

    jobs = scraper_result["jobs"]
    cv_keywords = scraper_result["cv_keywords"]
    
    print(f"📊 Found {len(jobs)} TOEFL-relevant jobs total")
    print(f"🎯 Top matches (fit score ≥ 3): {len([j for j in jobs if j.get('fit_score', 0) >= 3])}")

    try:
        # Generate markdown report
        print("📝 Generating markdown report...")
        markdown_generator = MarkdownGeneratorAgent(name="MarkdownGenerator")
        generator_result = markdown_generator.receive_message({
            "type": "toefl_jobs",
            "jobs": jobs,
            "cv_keywords": cv_keywords
        })
    except Exception as e:
        print(f"❌ Markdown generation failed: {e}")
        return

    if generator_result.get("type") != "response":
        print("❌ Markdown generator failed to return valid results.")
        return

    print(f"✅ TOEFL jobs report generated: {generator_result['filename']}")
    
    # Show summary of top jobs
    print("\n" + "="*80)
    print("💼 TOP TOEFL JOB MATCHES")
    print("="*80)
    
    top_jobs = [j for j in jobs if j.get('fit_score', 0) >= 2][:5]
    
    for i, job in enumerate(top_jobs, 1):
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        location = job.get("location", "Remote")
        fit_score = job.get("fit_score", 0)
        matches = job.get("cv_matches", [])
        source = job.get("source", "Unknown")
        
        print(f"\n{i}. {title}")
        print(f"   🏢 Company: {company}")
        print(f"   📍 Location: {location}")
        print(f"   ⭐ Fit Score: {fit_score}/10")
        print(f"   🎯 Matched Keywords: {', '.join(matches[:5])}")
        print(f"   📱 Source: {source}")
        print(f"   🔗 URL: {job.get('url', 'N/A')}")
    
    print(f"\n📄 Full report with all {len(jobs)} jobs available in: {generator_result['filename']}")
    print("💡 Check the markdown file for detailed descriptions and application tips!")

if __name__ == "__main__":
    run_toefl_jobs()
