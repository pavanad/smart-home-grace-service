import os

import requests


class HomeAssistantClient:

    def __init__(self):
        self.__host = os.getenv("HOME_ASSISTANT_HOST")
        self.__token = os.getenv("HOME_ASSISTANT_TOKEN")
        self.__header = self.__get_header()

    def __get_header(self) -> dict:
        return {
            "Authorization": f"Bearer {self.__token}",
            "content-type": "application/json",
        }

    def __get_states_filter(self, entity: str) -> list:
        url = f"{self.__host}/api/states"
        response = requests.get(url, headers=self.__header)
        data = response.json()
        entity_list = [
            {
                "entity_id": item.get("entity_id"),
                "state": item.get("state"),
                "friendly_name": item["attributes"].get("friendly_name"),
                "last_changed": item.get("last_changed"),
                "last_updated": item.get("last_updated"),
            }
            for item in data
            if entity in item["entity_id"]
        ]
        return entity_list

    def get_lights(self) -> list:
        return self.__get_states_filter("light.")

    def get_sensors(self) -> list:
        return self.__get_states_filter("sensor.")

    def get_switches(self) -> list:
        return self.__get_states_filter("switch.")
