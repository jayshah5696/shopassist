from crewai import Agent
from textwrap import dedent
from search_tools import Search_Tools
from langchain_groq import ChatGroq
llm_default = chat = ChatGroq(
    temperature=0.1,
    model="llama3-8b-8192"
)

class search_agents():
    def user_query_analyzer(self):
        return Agent(
            role='query Assistant',
            goal='Provide structured query analysis based on user query',
            tools=[],
            backstory=dedent(
                """
                Based on each user query, 
                the query assistant provides a structured analysis of the query to identify key elements such as product category,
                user intent, price sensitivity, and more.
                This analysis helps in refining product recommendation serach queries and improving the overall user experience.
                """
            ),
            verbose=False,
            llm = llm_default
        )
    
    def query_writer(self):
        return Agent(
            role='Query Writer',
            goal='Generate a well-structured product search query based on the analysis',
            tools=[],
            backstory=dedent(
                """
                The Query Writer generates a well-structured product search query based on the analysis of the user query.
                This query is designed to retrieve relevant results from the reddit and capture the user's intent effectively.
                """
            ),
            verbose=False,
            llm = llm_default
        )
    
    def search_results(self):
        return Agent(
            role='Search Results Assistant',
            goal='Retrieve and present the top 5 most relevant product recommendations',
            tools=Search_Tools.tools(),
            backstory=dedent(
                """
                The Search Results Assistant retrieves and presents the top 5 most relevant product recommendations to the user.
                The results are based on the structured search query generated earlier and aim to provide the user with a concise list of product options.
                """
            ),
            verbose=False,
            llm = llm_default
        )
    
    def synthesis(self):
        return Agent(
            role='Synthesis Assistant',
            goal='Generate a coherent response with product recommendations and key features',
            tools=[],
            backstory=dedent(
                """
                The Synthesis Assistant generates a coherent response that provides product recommendations, highlights key features, 
                and addresses the user's needs effectively. This response is based on the user query, analysis, and search results.
                Put it all togehter in a clear table format. with the following columns:
                product name | brand | price | features | link to product page | why recommended
                """
            ),
            verbose=False,
            llm = llm_default
        )