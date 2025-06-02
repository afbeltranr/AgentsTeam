# agents/job_application/job_scraper_agent.py

from autogen.agentchat import Agent
from utils.extract_keywords_from_pdf import extract_keywords_from_pdf
import requests
from bs4 import BeautifulSoup
import csv
import logging
from pathlib import Path

class JobScraperAgent(Agent):
    def __init__(self, name, pdf_path, output_csv="data/applications.csv", **kwargs):
        super().__init__(name=name, **kwargs)
        self.pdf_path = pdf_path
        self.output_csv = output_csv

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_job_description(self, job_url):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(job_url, headers=headers)
            if response.status_code != 200:
                logging.warning(f"Failed to load job page: {job_url}")
                return ""
            soup = BeautifulSoup(response.text, "html.parser")
            desc_div = soup.find("div", class_="description")  # RemoteOK uses 'description' class
            return desc_div.get_text(separator="\n").strip() if desc_div else ""
        except Exception as e:
            logging.error(f"Error fetching job description: {e}")
            return ""

    def scrape_jobs(self, keywords):
        query = "-".join(keywords[:3])
        url = f"https://remoteok.com/remote-{query}-jobs"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to retrieve job listings. Status code: {response.status_code}")
            return 0, []

        soup = BeautifulSoup(response.text, "html.parser")
        job_rows = soup.find_all("tr", class_="job")

        jobs = []

        for job in job_rows:
            try:
                title = job.find("h2").text.strip()
                company = job.find("h3").text.strip()
                location_tag = job.find("div", class_="location")
                location = location_tag.text.strip() if location_tag else "Remote"
                link_tag = job.find("a", {"itemprop": "url"})
                url = "https://remoteok.com" + link_tag["href"] if link_tag else None

                if not url:
                    continue

                job_description = self.get_job_description(url)

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                    "description": job_description
                })

            except Exception as e:
                logging.warning(f"Skipping a job due to error: {e}")
                continue

        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "url", "description"])
            writer.writeheader()
            writer.writerows(jobs)

        logging.info(f"Scraped {len(jobs)} jobs from RemoteOK.")
        return len(jobs), jobs

    def receive_message(self, message):
        if "scrape" in message.get("content", "").lower():
            try:
                keywords = extract_keywords_from_pdf(self.pdf_path)
                print(f"🧠 Extracted keywords: {keywords}") 
                n_jobs, jobs = self.scrape_jobs(keywords)
                return {
                    "type": "response",
                    "content": f"Scraping done. Found {n_jobs} jobs.",
                    "jobs": jobs,
                    "keywords": keywords
                }
            except Exception as e:
                logging.error(f"Error during scraping: {str(e)}")
                return {"content": f"Error during scraping: {str(e)}", "type": "error"}
        return {"type": "noop", "content": "No action taken."}

def run_daily():
    pdf_path = Path("documents/resumes/CV.pdf")
    agent = JobScraperAgent(name="JobScraper", pdf_path=str(pdf_path))
    return agent.receive_message({"content": "scrape", "type": "command"})
