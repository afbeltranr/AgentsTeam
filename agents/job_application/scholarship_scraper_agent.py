# agents/job_application/scholarship_scraper_agent.py

from autogen.agentchat import Agent
from utils.extract_keywords_from_pdf import extract_keywords_from_pdf
import requests
from bs4 import BeautifulSoup
import logging
import time
import re
from pathlib import Path
from datetime import datetime

class ScholarshipScraperAgent(Agent):
    def __init__(self, name, pdf_path, **kwargs):
        super().__init__(name=name, **kwargs)
        self.pdf_path = pdf_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def scrape_scholarships_db(self, keywords):
        """Scrape scholarships from ScholarshipsDB (chemistry and science education focused)"""
        scholarships = []
        
        # Chemistry and science education related search terms
        search_terms = ["chemistry", "science education", "stem", "chemical sciences", "educational sciences"]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        for term in search_terms:
            try:
                url = f"https://www.scholarshipsdb.net/scholarships-in-{term.replace(' ', '-')}"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Look for scholarship listings
                    scholarship_items = soup.find_all("div", class_=["scholarship-item", "scholarship", "result-item"])
                    
                    for item in scholarship_items[:10]:  # Limit to 10 per search term
                        try:
                            title_elem = item.find(["h2", "h3", "h4", "a"])
                            title = title_elem.get_text().strip() if title_elem else "Unknown Title"
                            
                            # Get link
                            link_elem = item.find("a")
                            link = link_elem.get("href") if link_elem else ""
                            if link and not link.startswith("http"):
                                link = "https://www.scholarshipsdb.net" + link
                            
                            # Get description
                            desc_elem = item.find(["p", "div"], class_=["description", "summary", "excerpt"])
                            description = desc_elem.get_text().strip() if desc_elem else "No description available"
                            
                            # Try to extract deadline and amount
                            deadline = self.extract_deadline(item.get_text())
                            amount = self.extract_amount(item.get_text())
                            
                            scholarships.append({
                                "title": title,
                                "description": description[:300] + "..." if len(description) > 300 else description,
                                "url": link,
                                "deadline": deadline,
                                "amount": amount,
                                "source": "ScholarshipsDB",
                                "search_term": term,
                                "contact_email": self.extract_email(item.get_text())
                            })
                            
                        except Exception as e:
                            logging.warning(f"Error parsing scholarship item: {e}")
                            continue
                
                time.sleep(2)  # Be respectful to the server
                
            except Exception as e:
                logging.error(f"Error scraping {term}: {e}")
                continue
        
        return scholarships

    def scrape_scholarships_for_development(self):
        """Scrape scholarships from Scholarships for Development"""
        scholarships = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        search_terms = ["chemistry", "science-education", "stem-education", "chemical-engineering"]
        
        for term in search_terms:
            try:
                url = f"https://www.scholarshipsfordevelopment.com/scholarships/{term}/"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Look for scholarship listings
                    scholarship_items = soup.find_all("article", class_=["post", "scholarship"])
                    if not scholarship_items:
                        scholarship_items = soup.find_all("div", class_=["scholarship-item", "scholarship-card"])
                    
                    for item in scholarship_items[:8]:  # Limit to 8 per search term
                        try:
                            title_elem = item.find(["h2", "h3", "h4"])
                            if not title_elem:
                                title_elem = item.find("a")
                            title = title_elem.get_text().strip() if title_elem else "Unknown Title"
                            
                            # Get link
                            link_elem = item.find("a")
                            link = link_elem.get("href") if link_elem else ""
                            if link and not link.startswith("http"):
                                link = "https://www.scholarshipsfordevelopment.com" + link
                            
                            # Get description
                            desc_elem = item.find(["p", "div"], class_=["excerpt", "description", "summary"])
                            if not desc_elem:
                                desc_elem = item.find("p")
                            description = desc_elem.get_text().strip() if desc_elem else "No description available"
                            
                            # Extract additional info
                            deadline = self.extract_deadline(item.get_text())
                            amount = self.extract_amount(item.get_text())
                            
                            scholarships.append({
                                "title": title,
                                "description": description[:300] + "..." if len(description) > 300 else description,
                                "url": link,
                                "deadline": deadline,
                                "amount": amount,
                                "source": "Scholarships for Development",
                                "search_term": term,
                                "contact_email": self.extract_email(item.get_text())
                            })
                            
                        except Exception as e:
                            logging.warning(f"Error parsing scholarship item: {e}")
                            continue
                
                time.sleep(2)  # Be respectful to the server
                
            except Exception as e:
                logging.error(f"Error scraping {term}: {e}")
                continue
        
        return scholarships

    def scrape_findastudyprogram(self):
        """Scrape scholarships from FindAStudyProgram"""
        scholarships = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            # Search for chemistry and science education scholarships
            url = "https://www.findastudyprogram.org/scholarships/chemistry"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Look for scholarship listings
                scholarship_items = soup.find_all("div", class_=["scholarship", "program-item", "result"])
                
                for item in scholarship_items[:10]:
                    try:
                        title_elem = item.find(["h2", "h3", "h4", "a"])
                        title = title_elem.get_text().strip() if title_elem else "Unknown Title"
                        
                        # Get link
                        link_elem = item.find("a")
                        link = link_elem.get("href") if link_elem else ""
                        if link and not link.startswith("http"):
                            link = "https://www.findastudyprogram.org" + link
                        
                        # Get description
                        desc_elem = item.find(["p", "div"], class_=["description", "summary"])
                        description = desc_elem.get_text().strip() if desc_elem else "No description available"
                        
                        # Extract additional info
                        deadline = self.extract_deadline(item.get_text())
                        amount = self.extract_amount(item.get_text())
                        
                        scholarships.append({
                            "title": title,
                            "description": description[:300] + "..." if len(description) > 300 else description,
                            "url": link,
                            "deadline": deadline,
                            "amount": amount,
                            "source": "FindAStudyProgram",
                            "search_term": "chemistry",
                            "contact_email": self.extract_email(item.get_text())
                        })
                        
                    except Exception as e:
                        logging.warning(f"Error parsing scholarship item: {e}")
                        continue
            
        except Exception as e:
            logging.error(f"Error scraping FindAStudyProgram: {e}")
        
        return scholarships

    def extract_deadline(self, text):
        """Extract deadline information from text"""
        deadline_patterns = [
            r"deadline[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
            r"due[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
            r"apply by[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
            r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
            r"deadline[:\s]*([A-Za-z]+ \d{1,2}, \d{4})",
            r"due[:\s]*([A-Za-z]+ \d{1,2}, \d{4})"
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Not specified"

    def extract_amount(self, text):
        """Extract scholarship amount from text"""
        amount_patterns = [
            r"\$[\d,]+",
            r"USD [\d,]+",
            r"€[\d,]+",
            r"£[\d,]+",
            r"up to \$[\d,]+",
            r"maximum \$[\d,]+",
            r"[\d,]+ USD",
            r"[\d,]+ EUR"
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"

    def extract_email(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else "Not available"

    def check_cv_fit(self, scholarship, cv_keywords):
        """Check how well the CV fits the scholarship requirements"""
        scholarship_text = (scholarship["title"] + " " + scholarship["description"]).lower()
        
        # Chemistry and science education related keywords
        relevant_keywords = [
            "chemistry", "chemical", "science", "education", "teaching", "stem", 
            "research", "laboratory", "analytical", "organic", "inorganic", 
            "physical chemistry", "biochemistry", "materials", "environmental",
            "data", "analysis", "python", "visualization", "machine learning"
        ]
        
        cv_keywords_lower = [kw.lower() for kw in cv_keywords]
        matches = []
        
        for keyword in relevant_keywords:
            if keyword in scholarship_text and any(kw in keyword or keyword in kw for kw in cv_keywords_lower):
                matches.append(keyword)
        
        # Also check direct CV keyword matches
        for cv_kw in cv_keywords_lower:
            if cv_kw in scholarship_text and cv_kw not in matches:
                matches.append(cv_kw)
        
        return matches

    def receive_message(self, message):
        if "scrape" in message.get("content", "").lower():
            try:
                # Extract keywords from CV
                cv_keywords = extract_keywords_from_pdf(self.pdf_path)
                print(f"🧠 CV Keywords for scholarship matching: {cv_keywords}")
                
                # Scrape from multiple sources
                print("🔍 Scraping scholarships from multiple sources...")
                
                scholarships = []
                
                # Scrape from different sources
                scholarships.extend(self.scrape_scholarships_db(cv_keywords))
                time.sleep(3)
                scholarships.extend(self.scrape_scholarships_for_development())
                time.sleep(3)
                scholarships.extend(self.scrape_findastudyprogram())
                
                # Remove duplicates based on title similarity
                unique_scholarships = []
                seen_titles = set()
                
                for scholarship in scholarships:
                    title_key = re.sub(r'[^a-zA-Z0-9]', '', scholarship["title"].lower())
                    if title_key not in seen_titles:
                        seen_titles.add(title_key)
                        
                        # Check CV fit
                        matches = self.check_cv_fit(scholarship, cv_keywords)
                        scholarship["cv_matches"] = matches
                        scholarship["fit_score"] = len(matches)
                        
                        unique_scholarships.append(scholarship)
                
                # Sort by fit score (highest first)
                unique_scholarships.sort(key=lambda x: x["fit_score"], reverse=True)
                
                print(f"🎓 Found {len(unique_scholarships)} unique scholarships")
                
                return {
                    "type": "response",
                    "content": f"Scholarship scraping done. Found {len(unique_scholarships)} scholarships.",
                    "scholarships": unique_scholarships,
                    "cv_keywords": cv_keywords
                }
                
            except Exception as e:
                logging.error(f"Error during scholarship scraping: {str(e)}")
                return {"content": f"Error during scholarship scraping: {str(e)}", "type": "error"}
        
        return {"type": "noop", "content": "No action taken."}
