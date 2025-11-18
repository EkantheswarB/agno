from agno.agent import Agent
from agno.models.groq import Groq
from textwrap import dedent

resume_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description=dedent("""
        You are a resume maker who can identify the commonly required skills for a particular job.
        You take the position name and return the most commonly listed skills for that position.
    """),
    instructions=[
        "Return the answer as a markdown table.",
        "The table should have at least these columns: Skill, Category.",
        "Show just the table, nothing else.",
    ],
    markdown=True,
)

prompt = input("Hey can you tell me the position you are applying for: ")

try:
    response = resume_agent.run(
        f"List the most commonly required skills for the position '{prompt}'. "
        f"Return them as a markdown table with columns Skill and Category."
    )
    print(response.content)
except Exception as e:
    print("ERROR from agent:", repr(e))
