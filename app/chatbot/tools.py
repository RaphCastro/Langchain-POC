from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolExecutor

load_dotenv()


tools = [TavilySearchResults(max_results=1)]
tool_executor = ToolExecutor(tools)
