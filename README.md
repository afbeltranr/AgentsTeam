
# Job Application Multi-Agent System

If you want to apply for jobs using a multi-agent system, this repository is for you. 

Currently this repository is a proof of concept, that uses two agents in collaboration to complete the task of looking for jobs using web scrapping, and creating a customized cover letter for each job. these two agents are:


- **`job_scraper_agent.py`**: This agent is responsible for finding relevant job listings by scraping job boards (currently RemoteOK) using the `BeautifulSoup` library. It extracts job titles, companies, descriptions, and URLs. The agent is modular and can be extended to support additional job boards. It also fetches detailed job descriptions and saves the results for further processing.

- **`cv_cl_generator_agent.py`**: This agent takes the job listings found by the scraper and analyzes your resume (extracting keywords from your PDF). It matches your skills to each job description, then automatically generates a customized CV and a tailored cover letter for each job, highlighting the most relevant skills and experience for the position.

- **`scholarship_scraper_agent.py`**: This agent searches for scholarships tailored to chemistry and science education backgrounds. It scrapes multiple scholarship databases, analyzes your CV for keyword matching, and identifies the best-fit opportunities. Results include scholarship amounts, deadlines, contact emails, and fit scores.

- **`toefl_job_scraper_agent.py`**: This agent specifically looks for jobs that value TOEFL certification and data skills with no experience required. It targets entry-level positions perfect for someone with English proficiency, data analysis skills, and educational background.

- **`markdown_generator_agent.py`**: This agent creates organized markdown reports with tables containing detailed information about scholarships and jobs, including contact information, application tips, and strategic advice.

## Features

- Job scrapping from RemoteOK
- Scholarship search from multiple databases (ScholarshipsDB, Scholarships for Development, FindAStudyProgram)
- TOEFL-specific job hunting across RemoteOK, Indeed, and FlexJobs
- CV keyword extraction and matching
- Organized markdown reports with application strategies

## Usage

### Original Job Application System
```bash
python run_jobs.py
```

### New Features

#### 🎓 Scholarship Search (Chemistry & Science Education)
Search for scholarships tailored to your chemistry and science education background:
```bash
python run_scholarships.py
```

#### 💼 TOEFL Jobs Search (Entry-Level Data Skills)
Find jobs that value TOEFL certification and data skills with no experience required:
```bash
python run_toefl_jobs.py
```

#### 🚀 Run Both New Features
Execute both scholarship and TOEFL job searches:
```bash
python run_new_features.py
```

### Output
All searches generate organized markdown reports in `data/generated_applications/`:
- `scholarships_YYYY-MM-DD.md` - Comprehensive scholarship opportunities with contact emails
- `toefl_jobs_YYYY-MM-DD.md` - TOEFL-relevant job opportunities with application tips

## Requirements
Make sure to install all dependencies:
```bash
pip install -r requirements.txt
```

## Job Applications History
<!-- AUTO-UPDATE:START -->

| # | Job Title | Company | Cover Letter Preview |
|---|-----------|---------|-----------------------|
| 1 | [Work from Home Customer Service Assistant](https://remoteok.com/remote-jobs/remote-work-from-home-customer-service-assistant-washing-state-pharmacy-association-1093884) | Washing State Pharmacy Association | Dear Washing State Pharmacy Association,  I am applying f... |

<!-- AUTO-UPDATE:END -->

