from langchain.tools import tool

from app.services.home_assistant import HomeAssistantClient


@tool
def smart_home_lights_state():
    """
    Useful for when you need to get status of the light devices or entities
    from the smart home.
    """
    results = ""
    client = HomeAssistantClient()

    filtered_switches = [
        item
        for item in client.get_switches()
        if not any(sub in item["entity_id"] for sub in ["led_", "camera_", "analise_"])
    ]
    lights = client.get_lights()
    lights.extend(filtered_switches)

    for item in lights:
        results += f"""
        Name: {item["friendly_name"]}
        Entity ID: {item["entity_id"]}
        State: {item["state"]}
        """

    return f"""
    Here are the results of the smart home lights state:
    {results}
    """
