from langchain.tools import tool


@tool
def cctv_image_analysis():
    """
    Useful for when you need to analyze an image.
    """
    return "CCTV Image Analysis"


@tool
def smart_home_control():
    """
    Useful for when you need to control smart home devices.
    """
    return "Smart Home Control"


@tool
def who_are_you():
    """
    Useful for when you need to know who you are.
    """
    return "You are artificial assistant Grace"
