import logging

from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

logger = logging.getLogger(__name__)


@tool
def web_search(query: str):
    """Useful for when you need to search the internet for information."""
    logger.info(f"Searching for: {query}")
    return TavilySearchResults().invoke({"query": query})
