import logging

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from numpy.core.numeric import ndarray

from app.settings import BASE_DIR


class ObjectDetection:

    MODELS_DIR = f"{BASE_DIR}/app/services/model"

    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("Creating object detection service")

        self.__detector = self.__get_object_detection_model()

    def __get_object_detection_model(self):
        self.__logger.info("Loading object detection model")

        model_filename = f"{self.MODELS_DIR}/efficientdet.tflite"
        with open(model_filename, "rb") as model_file:
            model_data = model_file.read()
            print(model_data)

        base_options = python.BaseOptions(model_asset_buffer=model_data)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, score_threshold=0.5
        )
        return vision.ObjectDetector.create_from_options(options)

    def set_frame(self, frame: ndarray, channel: int = 1):
        """Set frame from the video."""
        self.__frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.__original = self.__frame.copy()

    def detect(self):
        detection_result = self.__detector.detect(self.__frame)
        print(detection_result)
