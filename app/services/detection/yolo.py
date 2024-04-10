import logging

import cv2
import numpy as np
from numpy.core.numeric import ndarray

from app.settings import BASE_DIR


class YoloDetection:

    MIN_WIDTH = 1080
    MODELS_DIR = f"{BASE_DIR}/app/services/models/yolov3"

    def __init__(self):
        self.__frame = None
        self.__annotated_frame = None
        self.__layer_names = None
        self.__labels = self.__get_labels()
        self.__colors = self.__get_colors()
        self.__detector = self.__get_yolo_detector()

        self.__logger = logging.getLogger(__name__)
        self.__logger.info("Creating yolo detection object")

    @property
    def annotated_frame(self) -> ndarray:
        return self.__annotated_frame

    def __get_labels(self) -> list:
        """Load the COCO class labels our YOLO model was trained on.

        Returns:
            list: list of the labels
        """
        path = f"{self.MODELS_DIR}/coco.names"
        labels = open(path).read().strip().split("\n")
        return labels

    def __get_colors(self) -> list:
        """Initialize a list of colors to represent each possible class label.

        Returns:
            list: list of the colors
        """
        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(self.__labels), 3), dtype="uint8")
        return colors

    def __get_yolo_detector(self):
        # derive the paths to the YOLO weights and model configuration
        config_path = f"{self.MODELS_DIR}/yolov3.cfg"
        weights_path = f"{self.MODELS_DIR}/yolov3.weights"

        # load our YOLO object detector trained on COCO dataset (80 classes)
        net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # determine only the *output* layer names that we need from YOLO
        self.__layer_names = net.getLayerNames()
        self.__layer_names = [
            self.__layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()
        ]
        return net

    def __show_results(self, layer_outputs) -> list:

        threshold = 0.3
        confidence_max = 0.65

        boxes = []
        confidences = []
        class_ids = []

        (h, w) = self.__frame.shape[:2]

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > confidence_max:
                    box = detection[0:4] * np.array([w, h, w, h])
                    (center_x, center_y, width, height) = box.astype("int")

                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        results = []
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_max, threshold)
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in self.__colors[class_ids[i]]]
                cv2.rectangle(self.__frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.__labels[class_ids[i]], confidences[i])
                cv2.putText(
                    self.__frame,
                    text,
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                )
                results.append(
                    {
                        "category": self.__labels[class_ids[i]],
                        "probability": confidences[i],
                    }
                )
        return results

    def set_frame(self, frame: ndarray):
        """Set frame from the video."""
        self.__frame = frame
        self.__annotated_frame = frame

    def detect(self) -> list:
        """Detect objects in the image."""

        if self.__frame is None:
            return []

        height, width = self.__frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            self.__frame, 1.0 / 255.0, (416, 416), swapRB=True, crop=False
        )
        self.__detector.setInput(blob)
        layer_outputs = self.__detector.forward(self.__layer_names)
        results = self.__show_results(layer_outputs)

        return results
