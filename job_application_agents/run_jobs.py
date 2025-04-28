# run_jobs.py
from agents.job_application.job_scraper_agent import JobScraperAgent
from agents.job_application.application_agent import ApplicationAgent
from agents.job_application.cv_cl_generator_agent import CVCLGeneratorAgent

def main():
    scraper = JobScraperAgent()
    jobs = scraper.scrape_jobs(portal_name="LinkedIn")

    cv_cl_generator = CVCLGeneratorAgent()

    applicant = ApplicationAgent()
    for job in jobs:
        resume_path, cover_letter_path = cv_cl_generator.generate_documents(job)
        applicant.apply_to_job(job, resume_path, cover_letter_path)

if __name__ == "__main__":
    main()
