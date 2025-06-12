# agents/job_application/cv_cl_generator_agent.py

from autogen.agentchat import Agent
import logging
import re

class CVCLGeneratorAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def extract_keywords_from_text(self, text):
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())  # Words with ≥4 letters
        stopwords = {"with", "from", "this", "that", "have", "will", "your", "about", "using", "also"}
        return [w for w in words if w not in stopwords]

    def generate_cv_and_cl(self, resume_keywords, job):
        job_keywords = self.extract_keywords_from_text(job.get("description", ""))
        matching = set(resume_keywords) & set(job_keywords)

        logging.info(f"Matched {len(matching)} keywords for '{job['title']}' at {job['company']}'")

        cv = f"Custom CV for {job['title']} at {job['company']}\n\nSkills matched: {', '.join(matching)}"
        cl = f"""Dear {job['company']},

I am applying for the {job['title']} role. My experience aligns with your needs in {', '.join(matching)}.

Sincerely,
[Your Name]
"""
        return cv, cl

    def receive_message(self, message):
        if message.get("type") != "response" or "jobs" not in message:
            return {"type": "noop", "content": "No jobs received for CV/CL generation."}

        resume_keywords = message.get("keywords", [])
        jobs = message["jobs"]

        results = []
        for job in jobs:
            cv, cl = self.generate_cv_and_cl(resume_keywords, job)
            results.append({
                "job": job,
                "cv": cv,
                "cover_letter": cl
            })

        return {
            "type": "response",
            "content": f"Generated {len(results)} CV/CL pairs.",
            "results": results
        }

def run_daily():
    # ❌ No mock data — assumes scraper has already been run and connected
    pass
