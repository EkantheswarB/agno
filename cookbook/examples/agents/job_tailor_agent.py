"""Job Tailoring Agent – Resume & Application Personalization

This agent extracts the job description from a provided posting URL, analyzes it alongside your resume, and produces a fully tailored application package. It identifies skill gaps, suggests resume edits, and generates a targeted cover letter and LinkedIn pitch based on the role requirements.

Prerequisites:
- Install required dependencies: pip install scrapegraph-py agno groq
- Ensure your resume file path is correctly set in the script
- Provide a valid job posting URL when prompted
"""

from agno.agent import Agent
from agno.models.groq import Groq
from textwrap import dedent
from agno.media import File
from agno.tools.scrapegraph import ScrapeGraphTools

resume_path = File(filepath="Input the file location")

job_url = input ("Paste the link of the Job Posting: ").strip()

job_tailor = Agent(
    name="Job Application maker",
    enable_agentic_memory=True,
    model=Groq("llama-3.3-70b-versatile"),
    tools=[ScrapeGraphTools(enable_markdownify=True,enable_smartscraper=True,enable_crawl=False)],
    description=dedent("""
        You are a resume tailoring expert. You:
        - Extract the job description from the job URL using tools.
        - Compare it with the attached resume (PDF).
        - Suggest targeted changes and write a cover letter + LinkedIn pitch."""  ),
    instructions=[
        "Always use `smartscraper` (and optionally `markdownify`) ONLY with the job URL I provide.",
        "NEVER use `smartscraper` on the resume. The resume is attached as a file, not a URL.",
        "First, call `smartscraper` with the job URL to extract the full job description.",
        "Then, analyze the job description together with the attached resume.",
         "Give the results in a neatly formatted way.",
        "Only give the results, nothing else.",
        "Be truthful and don't make any irrelevant changes.",
        "Be concise and specific in the cover letter.",
        "Fill in the details of the company and position title from the job description",
    ]
)

prompt = f"""The job posting URL is:

{job_url}

Steps:
1. Use the `smartscraper` tool with this URL to extract the FULL job description
   (role, responsibilities, requirements, qualifications, company info).
2. Then, using my attached resume (PDF), do the following:
   - Extract key skills / requirements from the JD.
   - Create a table with:
        * Job Requirement / Skill
        * Does my resume cover it? (Yes/No) + what to add/edit
   - Suggest concrete bullet-point edits to my resume.
   - Write a short tailored cover letter (150–200 words).
   - Write a short LinkedIn connection/pitch message (3–4 sentences).
"""

response = job_tailor.run(prompt,files=[resume_path])
print(response.content)
