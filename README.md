
# Job Application Multi-Agent System

If you want to apply for jobs using a multi-agent system, this repository is for you. 

Currently this repository is a proof of concept, that uses two agents in collaboration to complete the task of looking for jobs using web scrapping, and creating a customized cover letter for each job. these two agents are:


- **`job_scraper_agent.py`**: This agent is responsible for finding relevant job listings by scraping job boards (currently RemoteOK) using the `BeautifulSoup` library. It extracts job titles, companies, descriptions, and URLs. The agent is modular and can be extended to support additional job boards. It also fetches detailed job descriptions and saves the results for further processing.

- **`cv_cl_generator_agent.py`**: This agent takes the job listings found by the scraper and analyzes your resume (extracting keywords from your PDF). It matches your skills to each job description, then automatically generates a customized CV and a tailored cover letter for each job, highlighting the most relevant skills and experience for the position.

## Features

- Job scrapping from REmoteOK

## Job Applications History
<!-- AUTO-UPDATE:START -->

| # | Job Title | Company | Cover Letter Preview |
|---|-----------|---------|-----------------------|
| 1 | [Lead Data Engineer](https://remoteok.com/remote-jobs/remote-lead-data-engineer-open-architects-1093295) | Open Architects | Dear Open Architects,  I am applying for the Lead Data En... |

<!-- AUTO-UPDATE:END -->

