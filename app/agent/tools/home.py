from langchain.tools import tool

from app.services.home_assistant import HomeAssistantClient

client = HomeAssistantClient()


@tool
def smart_home_lights_state():
    """
    Useful for when you need to get status of the light devices or entities
    from the smart home.
    """
    results = ""
    lights = get_filtered_lights()
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


@tool
def smart_home_light_set_state(entity: str, state: str):
    """
    Useful for when you need to set state of the light devices or entities
    from the smart home.
    To use the tool, you need to provide the two parameter: [entity, state].
    For example to set the state of the light named "Living Room",
    you would need the input "Living Room" and the state "on" or "off".
    """
    lights = get_filtered_lights()
    entity_name = entity.replace(" ", "").lower()
    for item in lights:
        name = item.get("friendly_name")
        if name and entity_name in name.replace(" ", "").lower():
            client.set_entity_state(item["entity_id"], state)
            return f"The state of {name} has been set to {state}."

    return f"No light device was found with the name: {entity}"


@tool
def smart_home_gate_state():
    """
    Useful for when you need to get status of the gate from the smart home.
    """
    results = ""
    sensors = client.get_binary_sensor()
    for item in sensors:
        name = item.get("friendly_name")
        if name and "Port" in name:
            results += f"""
            Name: {item["friendly_name"]}
            Entity ID: {item["entity_id"]}
            State: {item["state"]}
            """

    return f"""
    Here are the results of the smart home gates state:
    {results}
    """


def get_filtered_lights() -> list:
    filtered_switches = [
        item
        for item in client.get_switches()
        if not any(sub in item["entity_id"] for sub in ["led_", "camera_", "analise_"])
    ]
    lights = client.get_lights()
    lights.extend(filtered_switches)
    return lights
