# agents/job_application/cv_cl_generator_agent.py

from autogen.agentchat import Agent
import logging

class CVCLGeneratorAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_cv_and_cl(self, resume_keywords, job):
        # ✅ Placeholder for actual CV/CL generation logic
        job_keywords = self.extract_keywords_from_job(job)
        matching_keywords = set(resume_keywords) & set(job_keywords)
        logging.info(f"Matching keywords for job '{job['title']}' at {job['company']}: {matching_keywords}")
        
        cv = f"Custom CV for {job['title']} at {job['company']}\nMatched Keywords: {', '.join(matching_keywords)}"
        cover_letter = f"Dear {job['company']},\n\nI’m excited to apply for the {job['title']} role. I bring experience in {', '.join(matching_keywords)}.\n\nSincerely,\n[Your Name]"

        return cv, cover_letter

    def extract_keywords_from_job(self, job):
        # 🧪 Stub — ideally scrape full job description from `job['url']`
        title_keywords = job["title"].lower().split()
        company_keywords = job["company"].lower().split()
        return list(set(title_keywords + company_keywords))

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
    # Simulate call with mock job and resume keywords
    mock_message = {
        "type": "response",
        "keywords": ["python", "sql", "machine", "learning"],
        "jobs": [
            {"title": "Data Scientist", "company": "OpenAI", "location": "Remote", "url": "https://remoteok.com/job/openai"},
            {"title": "ML Engineer", "company": "DeepMind", "location": "Remote", "url": "https://remoteok.com/job/deepmind"}
        ]
    }
    agent = CVCLGeneratorAgent(name="CVCLGenerator")
    return agent.receive_message(mock_message)
# agents/job_application/cv_cl_generator_agent.py

from autogen.agentchat import Agent
import logging
import re

class CVCLGeneratorAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def extract_keywords_from_text(self, text):
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())  # Words longer than 3 chars
        stopwords = {"with", "from", "this", "that", "have", "will", "your", "about"}
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
    # No need for mock — assume scraper is run beforehand
    pass
