from cgi import test
from imgix import urlhelper
from .colorutils import find_contrasting_color, rgb_to_hex
import json
import requests

def _palette_url(domain, path, color_count):
    """
    Returns a imgix URL with the palette parameter.

    Parameters
    ----------
    domain: str
        Domain to use for URLS

    path: str
        Path to desired image

    color_count: int
        The size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors

    Returns
    -------
    str

    """
    color_params = {"palette" : "json", "colors": color_count}
    img_url = urlhelper.UrlHelper(domain, path, params=color_params, include_library_param=False)
    return(img_url)

def _palette_dict(domain, path, color_count=6):
    """
    Returns a dict representation of the retreived palette json. The "colors" key has been modified to return a dict with integer keys, rather than a list,
    to allow for easy back and forth between the default palette and the dominance palette.

    Parameters
    ----------
    domain: str
        Domain to use for URLS

    path: str
        Path to desired image

    color_count: int
        The size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors (default: 6)

    Returns
    -------
    dict


    """
    r = requests.get(_palette_url(domain, path, color_count))
    if r.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got " + str(r.status_code))
    pal_response = json.loads(r.text)
    colors = pal_response["colors"]
    pal_dict = {"colors" : dict(zip(range(0, len(colors)), colors)), "dominant_colors" : pal_response["dominant_colors"], 'average_luminance' : pal_response["average_luminance"]}
    return pal_dict

def _color_dict(palettes, dominance):
    """
    Returns the retrieved color palette.

    Parameters
    ----------
    palettes: dict
        A dict representing the default palette and the dominance palette.

    dominance: bool
        A boolean specifying whether the user wishes to recieve the dominance palette if possible.

    Returns
    -------
    dict
        A dict representation of the requested color palette. If the dominance palette is requested but is unavailable, returns the default palette instead.

    """
    if dominance and palettes["dominant_colors"].values():
        return palettes["dominant_colors"]
    return palettes["colors"]

def request_palette(domain, path, color_count=6, dominance=False):
    """
    Returns a color palette leveraging the imgix palette parameter. See https://docs.imgix.com/apis/rendering/color-palette/palette

    Parameters
    ----------
    domain: str
        Domain to use for URLs

    path: str
        Path to desired image

    color_count: int
        The size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors (default: 6)

    dominance: bool
        A boolean specifying whether the user wishes to recieve the dominance palette if possible (default: False)

    Returns
    -------
    dict
        Returns a dict representation of the color palette. If the dominance palette is requested but is unavailable, returns the default palette instead, indexed by integer keys.

    """
    pal_dict = _palette_dict(domain, path, color_count)
    return _color_dict(pal_dict, dominance)
    

def overlay_color(domain, path, color_count=6, dominance=False, hue_shift = 0.15, contrast_ratio = 4.5):
    """
    Returns a color that meets web accessibility contrast guidelines as best as possible when compared with the average luminance of the requested palette.

    Parameters
    ----------
    domain: str
        Domain to use for URLs

    path: str
        Path to desired image

    color_count: int
        The size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors (default: 6)

    dominance: bool
        A boolean specifying whether the user wishes to use the dominance palette if possible (default: False)

    hue_shift: float
        A float specifying the percentage with which to shift the hue value of the returned color in comparison to the average rgb value of the palette. (default: 0.15)

    contrast_ratio = float
        A float representing the ideal contrast ratio for the returned color. See https://www.w3.org/TR/WCAG21/#contrast-enhanced (default: 4.5)

    Returns
    -------
    dict
        A dictionary representation of a color.

    """
    pal_dict = _palette_dict(domain, path, color_count)
    pal = _color_dict(pal_dict, dominance).values()
    a_lum = pal_dict["average_luminance"]
    colors = []
    for color in pal:
        if color is not None:
            colors.append((color["red"], color["green"], color["blue"]))
    
    overlay = find_contrasting_color(colors, hue_shift, contrast_ratio, lum=a_lum)
    return {"red":overlay[0], "green":overlay[1], "blue":overlay[2], "hex": "#" + rgb_to_hex(overlay)}