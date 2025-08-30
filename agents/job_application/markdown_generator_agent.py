# agents/job_application/markdown_generator_agent.py

from autogen.agentchat import Agent
import logging
from datetime import datetime
from pathlib import Path
import re

class MarkdownGeneratorAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_scholarships_markdown(self, scholarships, cv_keywords):
        """Generate a markdown file with organized scholarship information"""
        
        # Create output directory if it doesn't exist
        output_dir = Path("data/generated_applications")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = output_dir / f"scholarships_{current_date}.md"
        
        # Start building the markdown content
        md_content = f"""# Chemistry & Science Education Scholarships

*Generated on: {datetime.now().strftime("%B %d, %Y at %H:%M")}*

## 🎯 Your Profile Keywords
Based on your CV analysis, the following keywords were used for matching:
**{', '.join(cv_keywords)}**

## 📊 Summary
- **Total Scholarships Found:** {len(scholarships)}
- **Best Matches:** {len([s for s in scholarships if s.get('fit_score', 0) >= 3])}
- **Sources Searched:** ScholarshipsDB, Scholarships for Development, FindAStudyProgram

---

## 🏆 Top Matched Scholarships
*Sorted by relevance to your background in chemistry, data analysis, and science education*

"""
        
        # Add table header
        md_content += """| Rank | Scholarship Title | Amount | Deadline | Fit Score | Matched Keywords | Source | Contact | Apply |
|------|-------------------|---------|----------|-----------|------------------|--------|---------|-------|
"""
        
        # Add scholarship rows
        for i, scholarship in enumerate(scholarships[:20], 1):  # Limit to top 20
            title = self.clean_text(scholarship.get("title", "Unknown"))
            amount = scholarship.get("amount", "Not specified")
            deadline = scholarship.get("deadline", "Not specified")
            fit_score = scholarship.get("fit_score", 0)
            matches = ", ".join(scholarship.get("cv_matches", [])[:5])  # Show top 5 matches
            source = scholarship.get("source", "Unknown")
            contact = scholarship.get("contact_email", "Not available")
            url = scholarship.get("url", "#")
            
            # Create apply link
            apply_link = f"[Apply]({url})" if url and url != "#" else "N/A"
            
            # Truncate long texts
            title = title[:50] + "..." if len(title) > 50 else title
            matches = matches[:40] + "..." if len(matches) > 40 else matches
            
            md_content += f"| {i} | {title} | {amount} | {deadline} | {fit_score} | {matches} | {source} | {contact} | {apply_link} |\n"
        
        # Add detailed descriptions section
        md_content += "\n---\n\n## 📋 Detailed Descriptions\n\n"
        
        for i, scholarship in enumerate(scholarships[:10], 1):  # Show details for top 10
            title = self.clean_text(scholarship.get("title", "Unknown"))
            description = self.clean_text(scholarship.get("description", "No description available"))
            url = scholarship.get("url", "#")
            contact = scholarship.get("contact_email", "Not available")
            fit_score = scholarship.get("fit_score", 0)
            matches = scholarship.get("cv_matches", [])
            
            md_content += f"""### {i}. {title}
**Fit Score:** {fit_score}/10 ⭐  
**Matched Keywords:** {', '.join(matches) if matches else 'None'}  
**Contact:** {contact}  
**Apply:** {url}

**Description:**  
{description}

---

"""
        
        # Add tips section
        md_content += """## 💡 Application Tips

### For Chemistry & Science Education Scholarships:
1. **Highlight your data analysis skills** - Many modern chemistry programs value computational skills
2. **Emphasize your educational background** - Your Universidad Nacional background is valuable
3. **Mention your TOEFL certification** - This demonstrates English proficiency for international programs
4. **Connect your Python/ML skills** - Show how they apply to chemical research and education
5. **Showcase any research projects** - Even if small, research experience is highly valued

### Next Steps:
1. Review the top-matched scholarships above
2. Prepare tailored application materials for each
3. Gather required documents (transcripts, references, etc.)
4. Set calendar reminders for application deadlines
5. Draft personalized essays highlighting relevant experience

### Keywords to Include in Applications:
Based on your CV and scholarship requirements, consider emphasizing:
- Data analysis and visualization in chemistry
- Educational technology and STEM teaching
- Research methodology and analytical skills
- Cross-cultural communication (Colombia → international)
- Computational chemistry and machine learning applications

---

*Generated by AgentsTeam Scholarship Scraper*  
*For updates, run the scholarship scraper again*
"""
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return str(filename)

    def generate_toefl_jobs_markdown(self, jobs, cv_keywords):
        """Generate a markdown file with TOEFL-relevant job information"""
        
        # Create output directory if it doesn't exist
        output_dir = Path("data/generated_applications")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = output_dir / f"toefl_jobs_{current_date}.md"
        
        # Start building the markdown content
        md_content = f"""# TOEFL Certification & Data Skills Jobs

*Generated on: {datetime.now().strftime("%B %d, %Y at %H:%M")}*

## 🎯 Your Profile Keywords
Based on your CV analysis, the following keywords were used for matching:
**{', '.join(cv_keywords)}**

## 📊 Summary
- **Total Jobs Found:** {len(jobs)}
- **Best Matches:** {len([j for j in jobs if j.get('fit_score', 0) >= 3])}
- **Sources Searched:** RemoteOK, Indeed, FlexJobs

---

## 💼 Top Matched Jobs
*Sorted by relevance to your TOEFL certification and data skills background*

"""
        
        # Add table header
        md_content += """| Rank | Job Title | Company | Location | Fit Score | Matched Keywords | Source | Apply |
|------|-----------|---------|----------|-----------|------------------|--------|-------|
"""
        
        # Add job rows
        for i, job in enumerate(jobs[:25], 1):  # Limit to top 25
            title = self.clean_text(job.get("title", "Unknown"))
            company = self.clean_text(job.get("company", "Unknown"))
            location = job.get("location", "Remote")
            fit_score = job.get("fit_score", 0)
            matches = ", ".join(job.get("cv_matches", [])[:5])  # Show top 5 matches
            source = job.get("source", "Unknown")
            url = job.get("url", "#")
            
            # Create apply link
            apply_link = f"[Apply]({url})" if url and url != "#" else "N/A"
            
            # Truncate long texts
            title = title[:40] + "..." if len(title) > 40 else title
            company = company[:25] + "..." if len(company) > 25 else company
            matches = matches[:35] + "..." if len(matches) > 35 else matches
            
            md_content += f"| {i} | {title} | {company} | {location} | {fit_score} | {matches} | {source} | {apply_link} |\n"
        
        # Add detailed descriptions section
        md_content += "\n---\n\n## 📋 Detailed Job Descriptions\n\n"
        
        for i, job in enumerate(jobs[:15], 1):  # Show details for top 15
            title = self.clean_text(job.get("title", "Unknown"))
            company = self.clean_text(job.get("company", "Unknown"))
            description = self.clean_text(job.get("description", "No description available"))
            url = job.get("url", "#")
            location = job.get("location", "Remote")
            fit_score = job.get("fit_score", 0)
            matches = job.get("cv_matches", [])
            
            md_content += f"""### {i}. {title} - {company}
**Location:** {location}  
**Fit Score:** {fit_score}/10 ⭐  
**Matched Keywords:** {', '.join(matches) if matches else 'None'}  
**Apply:** {url}

**Description:**  
{description}

---

"""
        
        # Add tips section
        md_content += """## 💡 Application Tips for TOEFL + Data Skills Jobs

### Leverage Your TOEFL Certification:
1. **Highlight English proficiency** - Mention your upcoming TOEFL certification prominently
2. **Emphasize bilingual abilities** - Spanish/English bilingual skills are valuable
3. **Show communication skills** - Connect your education background to communication

### Showcase Your Data Skills:
1. **Python experience** - Highlight your programming background
2. **Data analysis** - Emphasize your analytical and visualization skills
3. **Learning ability** - Show how you can quickly pick up new tools and technologies
4. **Educational background** - Your Universidad Nacional background demonstrates academic rigor

### For Entry-Level Positions:
1. **Emphasize willingness to learn** - Many employers value attitude over experience
2. **Highlight transferable skills** - Connect your education/research experience to job requirements
3. **Show reliability** - Demonstrate consistency and professionalism
4. **Include personal projects** - Any data analysis or Python projects you've done

### Application Strategy:
1. **Tailor each application** - Customize your resume and cover letter for each position
2. **Lead with strengths** - Put your data skills and English proficiency first
3. **Address the no-experience concern** - Frame your education and projects as relevant experience
4. **Show enthusiasm** - Express genuine interest in the role and company

### Keywords to Include in Applications:
- TOEFL certification / English proficiency
- Python programming and data analysis
- Bilingual communication (Spanish/English)
- Educational background and research skills
- Quick learner and detail-oriented
- Remote work capabilities

### Job Categories to Focus On:
- **Data Entry Specialist** - Perfect for showcasing attention to detail
- **ESL/English Tutor** - Leverage your TOEFL certification
- **Research Assistant** - Use your academic background
- **Customer Service (Bilingual)** - Combine language skills with service
- **Virtual Assistant** - Demonstrate organizational and communication skills
- **Junior Data Analyst** - Entry-level positions that value potential over experience

---

*Generated by AgentsTeam TOEFL Job Scraper*  
*For updates, run the job scraper again*
"""
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return str(filename)

    def clean_text(self, text):
        """Clean text for markdown formatting"""
        if not text:
            return "N/A"
        
        # Remove problematic characters for markdown tables
        text = str(text).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def receive_message(self, message):
        """Process requests to generate markdown files"""
        
        if message.get("type") == "scholarships":
            scholarships = message.get("scholarships", [])
            cv_keywords = message.get("cv_keywords", [])
            
            try:
                filename = self.generate_scholarships_markdown(scholarships, cv_keywords)
                return {
                    "type": "response",
                    "content": f"Scholarships markdown generated successfully: {filename}",
                    "filename": filename
                }
            except Exception as e:
                logging.error(f"Error generating scholarships markdown: {e}")
                return {
                    "type": "error",
                    "content": f"Error generating scholarships markdown: {e}"
                }
        
        elif message.get("type") == "toefl_jobs":
            jobs = message.get("jobs", [])
            cv_keywords = message.get("cv_keywords", [])
            
            try:
                filename = self.generate_toefl_jobs_markdown(jobs, cv_keywords)
                return {
                    "type": "response",
                    "content": f"TOEFL jobs markdown generated successfully: {filename}",
                    "filename": filename
                }
            except Exception as e:
                logging.error(f"Error generating TOEFL jobs markdown: {e}")
                return {
                    "type": "error",
                    "content": f"Error generating TOEFL jobs markdown: {e}"
                }
        
        return {"type": "noop", "content": "No action taken."}
