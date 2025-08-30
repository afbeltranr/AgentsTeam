# agents/job_application/toefl_job_scraper_agent.py

from autogen.agentchat import Agent
from utils.extract_keywords_from_pdf import extract_keywords_from_pdf
import requests
from bs4 import BeautifulSoup
import logging
import time
import re
from pathlib import Path

class TOEFLJobScraperAgent(Agent):
    def __init__(self, name, pdf_path, **kwargs):
        super().__init__(name=name, **kwargs)
        self.pdf_path = pdf_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def scrape_remoteok_toefl_jobs(self):
        """Scrape TOEFL-related jobs from RemoteOK"""
        jobs = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # TOEFL and English proficiency related search terms
        search_terms = ["english", "toefl", "esl", "data-entry", "customer-service", "virtual-assistant"]
        
        for term in search_terms:
            try:
                url = f"https://remoteok.com/remote-{term}-jobs"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_rows = soup.find_all("tr", class_="job")
                    
                    for job in job_rows[:5]:  # Limit to 5 per search term
                        try:
                            title = job.find("h2").text.strip()
                            company = job.find("h3").text.strip()
                            location_tag = job.find("div", class_="location")
                            location = location_tag.text.strip() if location_tag else "Remote"
                            link_tag = job.find("a", {"itemprop": "url"})
                            url = "https://remoteok.com" + link_tag["href"] if link_tag else None

                            if not url:
                                continue

                            # Get detailed job description
                            job_description = self.get_job_description(url)
                            
                            # Check if job mentions TOEFL, English proficiency, or entry-level data skills
                            if self.is_toefl_relevant(title, job_description):
                                jobs.append({
                                    "title": title,
                                    "company": company,
                                    "location": location,
                                    "url": url,
                                    "description": job_description,
                                    "source": "RemoteOK",
                                    "search_term": term
                                })

                        except Exception as e:
                            logging.warning(f"Skipping a job due to error: {e}")
                            continue
                
                time.sleep(2)  # Be respectful to the server
                
            except Exception as e:
                logging.error(f"Error scraping {term} from RemoteOK: {e}")
                continue
        
        return jobs

    def scrape_indeed_toefl_jobs(self):
        """Scrape TOEFL-related jobs from Indeed (simplified approach)"""
        jobs = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        search_queries = ["toefl english data entry", "english proficiency data analyst", "esl teacher remote"]
        
        for query in search_queries:
            try:
                formatted_query = query.replace(" ", "+")
                url = f"https://www.indeed.com/jobs?q={formatted_query}&l=remote"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Indeed job listings
                    job_cards = soup.find_all("div", class_=["job_seen_beacon", "result", "jobsearch-SerpJobCard"])
                    
                    for card in job_cards[:5]:  # Limit to 5 per query
                        try:
                            title_elem = card.find("h2", class_="jobTitle")
                            if not title_elem:
                                title_elem = card.find("a", {"data-jk": True})
                            
                            title = title_elem.get_text().strip() if title_elem else "Unknown Title"
                            
                            company_elem = card.find("span", class_="companyName")
                            company = company_elem.get_text().strip() if company_elem else "Unknown Company"
                            
                            # Get job link
                            link_elem = card.find("a", {"data-jk": True})
                            job_id = link_elem.get("data-jk") if link_elem else None
                            url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else ""
                            
                            # Get snippet description
                            desc_elem = card.find("div", class_=["job-snippet", "summary"])
                            description = desc_elem.get_text().strip() if desc_elem else "No description available"
                            
                            # Check if relevant for TOEFL certification
                            if self.is_toefl_relevant(title, description):
                                jobs.append({
                                    "title": title,
                                    "company": company,
                                    "location": "Remote",
                                    "url": url,
                                    "description": description,
                                    "source": "Indeed",
                                    "search_term": query
                                })
                            
                        except Exception as e:
                            logging.warning(f"Error parsing Indeed job: {e}")
                            continue
                
                time.sleep(3)  # Be more respectful to Indeed
                
            except Exception as e:
                logging.error(f"Error scraping Indeed for {query}: {e}")
                continue
        
        return jobs

    def scrape_flexjobs_toefl(self):
        """Scrape FlexJobs for English/TOEFL related positions"""
        jobs = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            # FlexJobs search for English/ESL/Data entry jobs
            search_terms = ["english-teacher", "esl-instructor", "data-entry", "virtual-assistant"]
            
            for term in search_terms:
                url = f"https://www.flexjobs.com/jobs/{term}"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    job_listings = soup.find_all("div", class_=["job", "job-listing", "search-result"])
                    
                    for job in job_listings[:4]:  # Limit to 4 per term
                        try:
                            title_elem = job.find(["h2", "h3", "h4", "a"])
                            title = title_elem.get_text().strip() if title_elem else "Unknown Title"
                            
                            company_elem = job.find("span", class_=["company", "employer"])
                            if not company_elem:
                                company_elem = job.find("div", class_="company")
                            company = company_elem.get_text().strip() if company_elem else "Unknown Company"
                            
                            # Get job link
                            link_elem = job.find("a")
                            link = link_elem.get("href") if link_elem else ""
                            if link and not link.startswith("http"):
                                link = "https://www.flexjobs.com" + link
                            
                            # Get description
                            desc_elem = job.find(["p", "div"], class_=["description", "summary", "snippet"])
                            description = desc_elem.get_text().strip() if desc_elem else "No description available"
                            
                            # Check relevance
                            if self.is_toefl_relevant(title, description):
                                jobs.append({
                                    "title": title,
                                    "company": company,
                                    "location": "Remote/Flexible",
                                    "url": link,
                                    "description": description,
                                    "source": "FlexJobs",
                                    "search_term": term
                                })
                            
                        except Exception as e:
                            logging.warning(f"Error parsing FlexJobs listing: {e}")
                            continue
                
                time.sleep(2)
                
        except Exception as e:
            logging.error(f"Error scraping FlexJobs: {e}")
        
        return jobs

    def get_job_description(self, job_url):
        """Get detailed job description from URL"""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(job_url, headers=headers)
            if response.status_code != 200:
                logging.warning(f"Failed to load job page: {job_url}")
                return ""
            soup = BeautifulSoup(response.text, "html.parser")
            desc_div = soup.find("div", class_="description")
            return desc_div.get_text(separator="\n").strip() if desc_div else ""
        except Exception as e:
            logging.error(f"Error fetching job description: {e}")
            return ""

    def is_toefl_relevant(self, title, description):
        """Check if job is relevant for someone with TOEFL certification and data skills"""
        text = (title + " " + description).lower()
        
        # TOEFL/English proficiency indicators
        toefl_keywords = [
            "toefl", "english proficiency", "english fluent", "native english", 
            "esl", "english teacher", "english tutor", "bilingual", "multilingual",
            "english communication", "english speaking", "english writing"
        ]
        
        # Entry-level data/tech keywords
        data_keywords = [
            "data entry", "data analyst", "data processing", "excel", "spreadsheet",
            "no experience", "entry level", "junior", "trainee", "recent graduate",
            "virtual assistant", "customer service", "administrative", "research assistant",
            "python", "sql", "data visualization", "analytics"
        ]
        
        # Check for TOEFL/English relevance
        has_english_req = any(keyword in text for keyword in toefl_keywords)
        
        # Check for data skills or entry-level positions
        has_data_aspect = any(keyword in text for keyword in data_keywords)
        
        # Also include jobs that mention specific skills from CV
        cv_skills = ["python", "data", "analysis", "visualization", "machine learning", "sql"]
        has_cv_skills = any(skill in text for skill in cv_skills)
        
        return has_english_req or (has_data_aspect and not "senior" in text and not "5+ years" in text) or has_cv_skills

    def check_cv_fit(self, job, cv_keywords):
        """Check how well the CV fits the job requirements"""
        job_text = (job["title"] + " " + job["description"]).lower()
        cv_keywords_lower = [kw.lower() for kw in cv_keywords]
        
        matches = []
        
        # Check direct keyword matches
        for cv_kw in cv_keywords_lower:
            if cv_kw in job_text:
                matches.append(cv_kw)
        
        # Add specific TOEFL-relevant skills
        toefl_skills = ["english", "communication", "teaching", "tutoring", "writing", "speaking"]
        for skill in toefl_skills:
            if skill in job_text and skill not in matches:
                matches.append(skill)
        
        return matches

    def receive_message(self, message):
        if "scrape" in message.get("content", "").lower():
            try:
                # Extract keywords from CV
                cv_keywords = extract_keywords_from_pdf(self.pdf_path)
                print(f"🧠 CV Keywords for TOEFL job matching: {cv_keywords}")
                
                print("🔍 Scraping TOEFL-relevant jobs from multiple sources...")
                
                jobs = []
                
                # Scrape from different sources
                jobs.extend(self.scrape_remoteok_toefl_jobs())
                time.sleep(3)
                jobs.extend(self.scrape_indeed_toefl_jobs())
                time.sleep(3)
                jobs.extend(self.scrape_flexjobs_toefl())
                
                # Remove duplicates and add CV fit analysis
                unique_jobs = []
                seen_titles = set()
                
                for job in jobs:
                    title_key = re.sub(r'[^a-zA-Z0-9]', '', job["title"].lower())
                    company_key = re.sub(r'[^a-zA-Z0-9]', '', job["company"].lower())
                    job_key = f"{title_key}_{company_key}"
                    
                    if job_key not in seen_titles:
                        seen_titles.add(job_key)
                        
                        # Check CV fit
                        matches = self.check_cv_fit(job, cv_keywords)
                        job["cv_matches"] = matches
                        job["fit_score"] = len(matches)
                        
                        unique_jobs.append(job)
                
                # Sort by fit score (highest first)
                unique_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
                
                print(f"💼 Found {len(unique_jobs)} unique TOEFL-relevant jobs")
                
                return {
                    "type": "response",
                    "content": f"TOEFL job scraping done. Found {len(unique_jobs)} relevant jobs.",
                    "jobs": unique_jobs,
                    "cv_keywords": cv_keywords
                }
                
            except Exception as e:
                logging.error(f"Error during TOEFL job scraping: {str(e)}")
                return {"content": f"Error during TOEFL job scraping: {str(e)}", "type": "error"}
        
        return {"type": "noop", "content": "No action taken."}
