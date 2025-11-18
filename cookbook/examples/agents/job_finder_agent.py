"""Job Finder Agent
This agent analyzes an uploaded resume to extract experience duration, job titles, and relevant skills. Based on this information, it searches for current job openings that closely match the user’s background. The agent evaluates each job by comparing required skills and experience, then returns a verified list of matching positions in a clean markdown table.

How to Use:
Run the script and provide the file path to your resume when prompted. The agent will scan the document and generate a table of relevant job openings—including job title, required experience, and a match percentage—based on your resume."""

from agno.agent import Agent
from agno.models.groq import Groq
from textwrap import dedent
from agno.media import File

file_path = File(filepath=input("Input the file location: "))

job_finder =  Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description=dedent("""
    You are job finder who scans the uploaded file for the experience section and find out the duration of each of the position.
    Then find the job openings online with the relevant job title based on the experience gathered from the experience section and skills section in the attached pdf."""
    ),
    instructions=[
        "Give the links of the job openings in the markdown table format.",
        "The table should contain job title, experience required, and Percentage with which the job is matching to the resume.",
        "Calculate the percentage match based on the number of skills and experience match",
        "Just give me the results nothing else",
        "Verify the links and give just the working ones",
        "Try to generate atleast 7 results"
    ]

)

try:
  response= job_finder.run(f"Scan the resume at {file_path} and find me the matching jobs"
                "return them as a markdown table")
  print(response.content)
except Exception as e:
  print("ERROR from agent:", repr(e))
