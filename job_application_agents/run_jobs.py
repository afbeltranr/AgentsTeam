from agents.job_application.job_scraper_agent import run_daily as run_scraper
from agents.job_application.application_agent import run_daily as run_applicator
from agents.job_application.cv_cl_generator_agent import run_daily as run_cv_generator
from agents.job_application.project_advisor_agent import run_daily as run_project_advisor  # ✅ fixed

def main():
    print("🔍 Running job scraper agent...")
    run_scraper()

    print("📄 Generating tailored resumes and cover letters...")
    run_cv_generator()

    print("📬 Submitting applications...")
    run_applicator()

    print("💡 Suggesting a personalized portfolio project...")
    run_project_advisor()

    print("✅ All agents finished successfully.")

if __name__ == "__main__":
    main()
