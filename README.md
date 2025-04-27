# AgentsTeam

I found AutogenCore as an application of the codebase2tutorial project. It is a framework for building and running multi-agent systems. The framework is designed to be flexible and extensible, allowing developers to create custom agents and environments.

my main goal is to create a multi-agent system that can use knowledge about my skills, job experience, education and data projects to generate tailored resume and cover letters for job applications. While one agent will be responsible for web scrapping the job portals for job offers, another agent will be responsible for generating the resume and cover letters. The agents will communicate with each other to ensure that the generated documents are relevant to the job offers found by the web scrapping agent. I think another agent will be be needed to do the actual application process, whether it be directly in the job portal or via email. I will also need to create a database to store the job offers and the generated documents, so that I can keep track of my applications and their status. 

hence, the folder structure is as follows:
```
/agents
/documents
/applications.csv
/utils
