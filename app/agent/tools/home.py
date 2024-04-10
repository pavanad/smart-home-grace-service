from langchain.tools import tool


@tool
def smart_home_control():
    """
    Useful for when you need to control smart home devices.
    """
    return "Smart Home Control"
