import logging
import os

from langchain.tools import tool

from app.services.bot import BotTelegram
from app.services.detection import ObjectDetection
from app.services.video import VideoStream
from app.settings import get_list_cameras

bot = BotTelegram()
video_stream = VideoStream()
logger = logging.getLogger(__name__)


@tool
def cctv_send_images():
    """
    Useful when you want to send images from security
    cameras (CCTV) in the house to the requesting user.
    Use when the user asks to identify objects, people, animals, cars, etc.
    """
    chat_id = os.environ.get("USER_CHAT_ID", None)
    if chat_id is None:
        return "Please provide chat_id"

    logger.info(f"Sending images to chat_id: {chat_id}")

    bot.set_chat_id(chat_id)
    list_cameras = get_list_cameras()
    response = {"success": [], "error": []}

    for camera in list_cameras:
        try:
            video_stream.set_rtsp_url(camera["url"])
            frame = video_stream.get_frame()
            bot.send_photo(frame)
            response["success"].append(camera["name"])
        except Exception as e:
            logger.error(f"Error sending image from camera {camera['name']}: {e}")
            response["error"].append(camera["name"])

    return f"""
    Result of sending images:
    Success: {response["success"]}
    Error: {response["error"]}
    """


@tool
def cctv_image_analysis():
    """
    Useful when you need to analyze images from security cameras using computer vision.
    The tool will analyze and return all objects detected in the image from each camera.
    """
    response = {}
    detection = ObjectDetection()
    list_cameras = get_list_cameras()
    chat_id = os.environ.get("USER_CHAT_ID", None)

    logger.info(f"Analyzing images from cameras: {list_cameras}")

    for camera in list_cameras:
        try:
            video_stream.set_rtsp_url(camera["url"])
            frame = video_stream.get_frame()

            detection.set_frame(frame)
            results = detection.detect()
            response[camera["name"]] = results

            if results:
                bot.set_chat_id(chat_id)
                bot.send_photo(detection.annotated_frame)

        except Exception as e:
            logger.error(f"Error analyzing image from camera {camera['name']}: {e}")

    return f"""
    Here are the results of the camera analyses:
    {response}
    """


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

    logger.info("Sending who are you message")

    return """
    Meet Grace - Your Smart Assistant for a Connected Home.
    Hello! I'm Grace, your smart assistant for a connected home.
    My name, "Grace", stands for "Generative AI Recognition And Control Expert",
    reflecting my ability to understand and control your home using generative AI.
    I'm here to help with environment analysis, smart home device control,
    and image analysis.
    """
