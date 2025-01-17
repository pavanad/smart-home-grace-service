import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)


@tool
def who_are_you():
    """
    Useful for when you need to know who you are and what your skills are.
    """

    logger.info("Sending who are you message")

    return """
    Meet Grace - Your Smart Assistant.
    Hello! I'm Grace, your smart assistant.
    My name, "Grace", stands for "Generative AI Recognition And Control Expert",
    reflecting my ability to understand and control your home using generative AI.
    I'm here to help with sensor analysis, smart home device control,
    and image analysis.
    """
