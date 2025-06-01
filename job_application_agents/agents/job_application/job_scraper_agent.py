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

    def scrape_jobs(self, keywords):
        query = "-".join(keywords[:3])  # Use top 3 keywords for the query
        url = f"https://remoteok.com/remote-{query}-jobs"

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to retrieve job listings. Status code: {response.status_code}")
            return 0

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
                url = "https://remoteok.com" + link_tag["href"] if link_tag else "N/A"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                })
            except Exception as e:
                logging.warning(f"Skipping a job due to error: {e}")
                continue

        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "url"])
            writer.writeheader()
            writer.writerows(jobs)

        logging.info(f"Scraped {len(jobs)} jobs from RemoteOK.")
        return len(jobs)

    def receive_message(self, message):
        if "scrape" in message.get("content", "").lower():
            try:
                keywords = extract_keywords_from_pdf(self.pdf_path)
                print(f"🧠 Extracted keywords: {keywords}") 
                n_jobs = self.scrape_jobs(keywords)
                return {"content": f"Scraping done. Found {n_jobs} jobs.", "type": "response"}
            except Exception as e:
                logging.error(f"Error during scraping: {str(e)}")
                return {"content": f"Error during scraping: {str(e)}", "type": "error"}
        else:
            return {"content": "No action taken.", "type": "noop"}

def run_daily():
    pdf_path = Path("documents/resumes/CV.pdf")  # Update path if needed
    agent = JobScraperAgent(name="JobScraper", pdf_path=str(pdf_path))
    return agent.receive_message({"content": "scrape", "type": "command"})
