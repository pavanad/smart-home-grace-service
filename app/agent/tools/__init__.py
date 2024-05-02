from .about import who_are_you
from .cctv import cctv_image_analysis, cctv_list_cameras, cctv_send_images
from .general import web_search
from .home import (
    smart_home_gate_state,
    smart_home_light_set_state,
    smart_home_lights_state,
)


def get_tools() -> list:
    return [
        who_are_you,
        cctv_image_analysis,
        cctv_list_cameras,
        cctv_send_images,
        web_search,
        smart_home_gate_state,
        smart_home_light_set_state,
        smart_home_lights_state,
    ]
