# agents/job_application//job_scraper_agent.py

from autogen.agentchat import Agent
from utils.extract_keywords_from_pdf import extract_keywords_from_pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

class JobScraperAgent(Agent):
    def __init__(self, name, pdf_path, output_csv="applications.csv", **kwargs):
        super().__init__(name=name, **kwargs)
        self.pdf_path = pdf_path
        self.output_csv = output_csv

    def scrape_jobs(self, keywords):
        search_query = "+".join(keywords[:5])  # Limit to first 5 keywords
        url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location=Remote"

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # No GUI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        jobs = []
        job_cards = driver.find_elements(By.CLASS_NAME, "base-search-card")

        for card in job_cards:
            title_elem = card.find_element(By.CLASS_NAME, "base-search-card__title")
            company_elem = card.find_element(By.CLASS_NAME, "base-search-card__subtitle")
            location_elem = card.find_element(By.CLASS_NAME, "job-search-card__location")

            jobs.append({
                "title": title_elem.text.strip(),
                "company": company_elem.text.strip(),
                "location": location_elem.text.strip(),
                "url": card.get_attribute("href"),
            })

        driver.quit()

        # Save to CSV
        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "url"])
            writer.writeheader()
            writer.writerows(jobs)

        return len(jobs)

    def receive_message(self, message):
        if "scrape" in message.get("content", "").lower():
            try:
                keywords = extract_keywords_from_pdf(self.pdf_path)
                n_jobs = self.scrape_jobs(keywords)
                return {"content": f"Scraping done. Found {n_jobs} jobs.", "type": "response"}
            except Exception as e:
                return {"content": f"Error during scraping: {str(e)}", "type": "error"}
        else:
            return {"content": "No action taken.", "type": "noop"}
