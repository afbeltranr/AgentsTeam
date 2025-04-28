# run_scholarships.py
from agents.scholarship_application.scholarship_scraper_agent import ScholarshipScraperAgent
from agents.scholarship_application.scholarship_application_agent import ScholarshipApplicationAgent
from agents.scholarship_application.analyzer_agent import ScholarshipAnalyzerAgent

def main():
    scraper = ScholarshipScraperAgent()
    scholarships = scraper.scrape_scholarships(portal_name="Scholarships.com")

    analyzer = ScholarshipAnalyzerAgent()
    applicant = ScholarshipApplicationAgent()

    for scholarship in scholarships:
        if analyzer.analyze_fit(scholarship, user_profile={}):
            resume_path = "documents/resumes/your_resume.pdf"
            cover_letter_path = "documents/scholarships_letters/your_letter.pdf"
            applicant.apply_to_scholarship(scholarship, resume_path, cover_letter_path)

if __name__ == "__main__":
    main()
