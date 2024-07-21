from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_groq import ChatGroq
import dotenv
import os
dotenv.load_dotenv()
llm_default = chat = ChatGroq(
    temperature=0.1,
    model="llama3-70b-8192"
)

# Define a custom tool using the `tool` decorator
@tool("Basic Search Assistant Tool")
def search_assistant_tool(query: str) -> str:
    """
    This tool takes a user query and generates a structured output.
    """
    # Implement the logic for the search assistant tool
    # For simplicity, let's assume it returns a formatted string
    return f"Structured output for query: {query}"

# Define the agent with the custom tool
search_agent = Agent(
    role='Search Assistant',
    goal='Provide structured search results based on user queries',
    tools=[search_assistant_tool],
    verbose=True,
    llm = llm_default
)

# Define the task for the agent
search_task = Task(
    description='Process the user query and generate structured output',
    agent=search_agent,
    expected_output='A structured response based on the user query'
)

# Form the crew with a sequential process
search_crew = Crew(
    agents=[search_agent],
    tasks=[search_task],
    process=Process.sequential,
    verbose=True
)

# Example of kicking off the crew with a sample query
result = search_crew.kickoff(inputs={'query': 'Latest trends in AI'})
print(result)


