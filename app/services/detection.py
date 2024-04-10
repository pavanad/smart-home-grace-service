import logging

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from numpy.core.numeric import ndarray

from app.settings import BASE_DIR


class ObjectDetection:

    THRESHOLD = 0.65
    MODELS_DIR = f"{BASE_DIR}/app/services/model"

    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("Creating object detection service")

        self.__frame = None
        self.__annotated_frame = None
        self.__detector = self.__get_object_detection_model()

    @property
    def annotated_frame(self) -> ndarray:
        return self.__annotated_frame

    def __get_object_detection_model(self):
        self.__logger.info("Loading object detection model")

        model_filename = f"{self.MODELS_DIR}/efficientdet.tflite"
        with open(model_filename, "rb") as model_file:
            model_data = model_file.read()

        base_options = python.BaseOptions(model_asset_buffer=model_data)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, score_threshold=0.5
        )
        return vision.ObjectDetector.create_from_options(options)

    def __show_results(self, detection_result):

        margin = 10  # pixels
        text_color = (255, 0, 0)  # red
        image = np.copy(self.__frame.numpy_view())

        for detection in detection_result.detections:

            # draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, text_color, 3)

            # draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            result_text = category_name + " (" + str(probability) + ")"
            text_location = (margin + bbox.origin_x, margin + 10 + bbox.origin_y)
            cv2.putText(
                image,
                result_text,
                text_location,
                cv2.FONT_HERSHEY_PLAIN,
                1,
                text_color,
                1,
            )

        self.__annotated_frame = image

    def set_frame(self, frame: ndarray, channel: int = 1):
        """Set frame from the video."""
        self.__frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    def detect(self) -> list:
        response = []
        detection_result = self.__detector.detect(self.__frame)
        for detection in detection_result.detections:
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            if probability >= self.THRESHOLD:
                response.append({"category": category_name, "probability": probability})

        self.__show_results(detection_result)

        return response
