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
def cctv_send_images(cam_selected: str = "all"):
    """
    Useful when you want to send images from security
    cameras (CCTV) in the house to the requesting user.
    To use the tool, you need to provide the one parameter: [camera].
    For example to send the image from the camera named "Social Gate",
    you would need the input "Social Gate".
    If user not provide the camera name, the tool will send the
    image from all cameras.
    """
    chat_id = os.environ.get("USER_CHAT_ID", None)
    if chat_id is None:
        return "Please provide chat_id"

    logger.info(f"Sending images to chat_id: {chat_id}")

    bot.set_chat_id(chat_id)
    list_cameras = get_list_cameras()
    response = {"success": [], "error": []}

    sanitity_cam_selected = cam_selected.replace(" ", "").lower()
    for camera in list_cameras:
        try:
            name = camera["name"].replace(" ", "").lower()
            if sanitity_cam_selected not in name and sanitity_cam_selected != "all":
                continue
            video_stream.set_rtsp_url(camera["url"])
            frame = video_stream.get_frame()
            bot.send_photo(frame)
            response["success"].append(camera["name"])
        except Exception as e:
            logger.error(f"Error sending image from camera {camera['name']}: {e}")
            response["error"].append(camera["name"])

    results = any([response["success"], response["error"]])
    if not results:
        return "No images were sent."

    return f"""
    Result of sending images:
    Success: {response["success"]}
    Error: {response["error"]}
    """


@tool
def cctv_image_analysis(cam_selected: str = "all"):
    """
    Useful when you need to analyze images from security cameras using computer vision.
    Use when the user asks to identify objects, people, animals, cars, etc.
    The tool will analyze and return all objects detected in the image from each camera.
    To use the tool, you need to provide the one parameter: [camera].
    For example to analyze the image from the camera named "Social Gate",
    you would need the input "Social Gate".
    If user not provide the camera name, the tool will analyze the image
    from all cameras.
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
                send_results = any(
                    [camera["name"] in cam_selected, cam_selected == "all"]
                )
                if send_results:
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
    Useful when you need only to list all the cameras in the house.
    Never use to analyze cameras. The tool will return a list of all
    the cameras in the house.
    """
    logger.info("Listing all the cameras in the house")
    list_cameras = [camera["name"] for camera in get_list_cameras()]

    response = "Here are the list of cameras:\n"
    for camera in list_cameras:
        response += f"- {camera}\n"

    return response
