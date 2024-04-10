import logging
import os

from langchain.tools import tool

from app.services.bot import BotTelegram
from app.services.detection.yolo import YoloDetection
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
    Use when the user asks to identify objects, people, animals, cars, etc.
    The tool will analyze and return all objects detected in the image from each camera.
    """
    response = {}
    detection = YoloDetection()
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
def cctv_list_cameras():
    """
    Useful when you need to list all the cameras in the house.
    Use only if the user wants to know which cameras are available.
    The tool will return a list of all the cameras in the house.
    """
    list_cameras = [camera["name"] for camera in get_list_cameras()]
    names_cameras = f"\n".join(list_cameras)

    return f"Here are the list of cameras:\n{names_cameras}\n"
