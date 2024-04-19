import os

import requests


class HomeAssistantClient:

    BASE_URL = "http://192.168.0.3:8123"
    HA_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")

    def __init__(self):
        self.__host = ""
        self.__header = self.__get_header()

    def __get_header(self) -> dict:
        return {
            "Authorization": f"Bearer {self.HA_TOKEN}",
            "content-type": "application/json",
        }
