from crewai import Task
from textwrap import dedent



class SearchTasks():
    def query_analysis(self,agent):
        return Task(
            description=dedent(
                """
                Based on User each user query, please provide the following analysis:

                    1.  Main Product Category: Identify the primary product category the user is interested in.
                    2.  Specific Features: List any specific features or attributes mentioned in the query.
                    3.  User Intent: Determine if the user is: a) Browsing/Exploring b) Looking for a specific item c) Comparing products d) Seeking advice/recommendations
                    4.  Price Sensitivity: Note any mentions of budget or price range.
                    Please provide your analysis in a clear, concise format. This information will be used to refine our product recommendation algorithm.

                USER QUERY = original query: {query}
                provide the analysis in a clear, concise format
                """
            ),
            agent=agent,
            expected_output="A deteailed analysis of the user query.",
            context=None,
            async_execution=False)
        
    def query_writer(self, agent):
        return Task(
            description=dedent(
                """
                Based on the analysis of the user query, please generate a well-structured product search query that can be used to retrieve relevant results from the product database.

                original query: {query}

                Please generate a reddit search query that captures the user's intent and preferences effectively.
                put it in a single clear sentence
                """
            ),
            agent=agent,
            expected_output="A well-structured product search query based on the analysis.",
            context = None,
            async_execution=False)
    

    def search_results(self, agent):
        return Task(
            description=dedent(
                """
                Based on the structured search query, retrieve and present the top 5 most relevant product recommendations to the user.
                """
            ),
            agent=agent,
            expected_output="The top 5 most relevant product recommendations.",
            context = None,
            async_execution=False)
    
    def synthesis(self, agent):
        return Task(
            description=dedent(
                """
                Based on the user query, analysis, and search results, generate a coherent response that provides product recommendations, highlights key features, and addresses the user's needs effectively.
                """
            ),
            agent=agent,
            expected_output="A coherent response with product recommendations and key features.",
            context = None, 
            async_execution=False)


