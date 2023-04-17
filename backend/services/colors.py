from pathlib import Path

import webcolors
from colorthief import ColorThief
from webcolors import rgb_to_hex


def hex_to_name(hex_color):
    try:
        color_name = webcolors.hex_to_name(hex_color)
    except ValueError:
        rgb_color = webcolors.hex_to_rgb(hex_color)
        color_name = _closest_color(rgb_color)
    return color_name


def _closest_color(requested_color):
    min_colors = {}

    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    return min_colors[min(min_colors.keys())]


def _load_image(image_path: str) -> tuple[int, int, int]:
    color_thief = ColorThief(image_path)

    return color_thief.get_color(quality=1)


def recognize_vehicle_color(image_path: str) -> str:
    dominant_color = _load_image(image_path)

    return rgb_to_hex(dominant_color)
