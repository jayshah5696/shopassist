import os
from langchain.agents import tool
from dotenv import load_dotenv
from multion.client import MultiOn

load_dotenv()
multion_client = MultiOn(api_key=os.getenv("MULTION_API_KEY"),
                         agentops_api_key=os.environ.get("AGENTOPS_API_KEY"))

# from multion.client import MultiOn
class Search_Tools:
    @tool("Google Search Tool")
    def google_search_tool(query: str) -> str:
        """
        STRING input expected
        This tool takes a user query, searches on Google using Multion API,
        and retrieves top 5 results and its content that can help address the user query .
        input is query string and output is a list of dictionaries containing title, description and url of the search results.
        """
        # Perform the search using the Multion client
        # response = multion_client.browse(
        #     cmd=query,
        #     url="https://www.google.com",
        #     max_steps=5,
        #     include_screenshot=False
        # )
        retrieve_response = multion_client.retrieve(
        cmd=query,
        url="https://www.google.com",
        fields=["title", "description", "url"],
        local=False)

        # Check if the request was successful
        if retrieve_response.status == "DONE":
            results = (retrieve_response.dict()['data'])
            return results
        else:
            return f"Error: {retrieve_response.status} - {retrieve_response.message}"


    def tools():
        return [Search_Tools.google_search_tool]
