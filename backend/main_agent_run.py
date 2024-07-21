from dotenv import load_dotenv
import agentops
from crewai import Crew
from search_agents import search_agents
from search_tasks import SearchTasks


def main():
    # Load environment variables from .env file
    load_dotenv()
    agentops.init(tags=["crew-search-assistant"])

    print("Initializing Search Assistant Crew...")
    search_query = "men business casual chinos under $50"
    context = [{"user_query": search_query}]

    tasks =SearchTasks()
    agents = search_agents()

    # create agents
    user_query_agent = agents.user_query_analyzer()
    query_writer_agent = agents.query_writer()
    search_results_agent = agents.search_results()
    synthesis_agent = agents.synthesis()

    # create tasks
    user_query_task = tasks.query_analysis(user_query_agent )
    query_writer_task = tasks.query_writer(query_writer_agent)
    search_results_task = tasks.search_results(search_results_agent)
    synthesis_task = tasks.synthesis(synthesis_agent)


    query_writer_task.context = [user_query_task]
    search_results_task.context = [query_writer_task]
    synthesis_task.context = [search_results_task]

    crew = Crew(
        agents = [user_query_agent, query_writer_agent, search_results_agent, synthesis_agent],
        tasks = [user_query_task, query_writer_task, search_results_task, synthesis_task],
        context = context,
        process = "sequential",
        verbose = False
    )

    result = crew.kickoff(inputs={'query': search_query})
    print(result)

if __name__ == "__main__":
    main()