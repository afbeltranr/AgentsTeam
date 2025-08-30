# run_scholarships.py

from agents.job_application.scholarship_scraper_agent import ScholarshipScraperAgent
from agents.job_application.markdown_generator_agent import MarkdownGeneratorAgent
from pathlib import Path
import json

# ✅ Config-style constant
RESUME_PATH = Path("documents/resumes/CV.pdf")

def run_scholarships():
    print("🎓 Starting scholarship search pipeline...\n")

    try:
        # Initialize scholarship scraper
        scholarship_scraper = ScholarshipScraperAgent(name="ScholarshipScraper", pdf_path=str(RESUME_PATH))
        print("🔍 Running scholarship scraper...")
        scraper_result = scholarship_scraper.receive_message({"content": "scrape", "type": "command"})
    except Exception as e:
        print(f"❌ Failed to run scholarship scraper: {e}")
        return

    if scraper_result.get("type") != "response" or "scholarships" not in scraper_result or not scraper_result["scholarships"]:
        print("⚠️ No scholarships found.")
        return

    scholarships = scraper_result["scholarships"]
    cv_keywords = scraper_result["cv_keywords"]
    
    print(f"📊 Found {len(scholarships)} scholarships total")
    print(f"🎯 Top matches (fit score ≥ 3): {len([s for s in scholarships if s.get('fit_score', 0) >= 3])}")

    try:
        # Generate markdown report
        print("📝 Generating markdown report...")
        markdown_generator = MarkdownGeneratorAgent(name="MarkdownGenerator")
        generator_result = markdown_generator.receive_message({
            "type": "scholarships",
            "scholarships": scholarships,
            "cv_keywords": cv_keywords
        })
    except Exception as e:
        print(f"❌ Markdown generation failed: {e}")
        return

    if generator_result.get("type") != "response":
        print("❌ Markdown generator failed to return valid results.")
        return

    print(f"✅ Scholarship report generated: {generator_result['filename']}")
    
    # Show summary of top scholarships
    print("\n" + "="*80)
    print("🏆 TOP SCHOLARSHIP MATCHES")
    print("="*80)
    
    top_scholarships = [s for s in scholarships if s.get('fit_score', 0) >= 2][:5]
    
    for i, scholarship in enumerate(top_scholarships, 1):
        title = scholarship.get("title", "Unknown")
        amount = scholarship.get("amount", "Not specified")
        deadline = scholarship.get("deadline", "Not specified")
        fit_score = scholarship.get("fit_score", 0)
        matches = scholarship.get("cv_matches", [])
        source = scholarship.get("source", "Unknown")
        
        print(f"\n{i}. {title}")
        print(f"   💰 Amount: {amount}")
        print(f"   📅 Deadline: {deadline}")
        print(f"   ⭐ Fit Score: {fit_score}/10")
        print(f"   🎯 Matched Keywords: {', '.join(matches[:5])}")
        print(f"   📍 Source: {source}")
        print(f"   🔗 URL: {scholarship.get('url', 'N/A')}")
    
    print(f"\n📄 Full report with all {len(scholarships)} scholarships available in: {generator_result['filename']}")
    print("💡 Check the markdown file for detailed descriptions, contact emails, and application tips!")

if __name__ == "__main__":
    run_scholarships()
