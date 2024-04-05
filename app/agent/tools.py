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
    Useful for when you need to know who you are and what your skills are.
    """
    return """
    Meet Grace - Your Smart Assistant for a Connected Home.
    Hello! I'm Grace, your smart assistant for a connected home.
    My name, "Grace", stands for "Generative AI Recognition And Control Expert",
    reflecting my ability to understand and control your home using generative AI.
    I'm here to help with environment analysis, smart home device control,
    and image analysis.
    """
