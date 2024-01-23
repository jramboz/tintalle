# All the color math here is taken from reverse-engineering the Sabertec Configurator
# https://sabertec.net/configurator/index.html. I honeslty only vaguely understand how
# the math works. But it does seem to work!

import math

class RGBColor:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b

class XYZColor:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

# LED color and luminance values
_LEDs = {
    'r': {
        'color': RGBColor(255, 35, 0),
        'luminance': 0.752
    },
    'g': {
        'color': RGBColor(0, 255, 40),
        'luminance': 0.976
    },
    'b': {
        'color': RGBColor(0, 90, 255),
        'luminance': 0.38
    },
    'w': {
        'color': RGBColor(255, 255, 255),
        'luminance': 2.572
    }
}

def _adjust_for_LED(intensity: int, LED: dict) -> tuple[RGBColor, float]:
    '''Adjusts an RBGColor value to account for LED color and luminance.
    Input: single RBGColor and an LED specification (dictionary with RBGColor and luminance float).
    Returns: tuple - (RBGColor, intensity float)'''
    return (
        LED['color'],
        intensity / 255 * LED['luminance']
    )

def _convert_xyz_to_rgb(x, y, z=254):
    '''Adapted from Sabertec configurator'''
    # Normalize z to the range [0, 1]
    normalized_z = (z / 254).__round__(2)

    # Calculate intermediate values based on normalized z
    intermediate_x = (normalized_z / y) * x
    intermediate_y = (normalized_z / y) * (1 - x - y)

    # Convert from XYZ to RGB using the matrix transformation
    r = 1.656492 * intermediate_x - 0.354851 * normalized_z - 0.255038 * intermediate_y
    g = 0.707196 * -intermediate_x + 1.655397 * normalized_z + 0.036152 * intermediate_y
    b = 0.051713 * intermediate_x - 0.121364 * normalized_z + 1.01153 * intermediate_y

    # Normalize RGB values to the range [0, 1]
    if b < r and g < r and 1 < r:
        g /= r
        b /= r
        r = 1
    elif b < g and r < g and 1 < g:
        r /= g
        b /= g
        g = 1
    elif r < b and g < b and 1 < b:
        r /= b
        g /= b
        b = 1

    # Apply gamma correction
    r = 12.92 * r if r <= 0.0031308 else 1.055 * (r ** (1 / 2.4)) - 0.055
    g = 12.92 * g if g <= 0.0031308 else 1.055 * (g ** (1 / 2.4)) - 0.055
    b = 12.92 * b if b <= 0.0031308 else 1.055 * (b ** (1 / 2.4)) - 0.055

    # Convert RGB values to the range [0, 255]
    r = round(255 * r)
    g = round(255 * g)
    b = round(255 * b)

    # Ensure RGB values are not NaN
    if math.isnan(r): r = 0
    if math.isnan(g): g = 0
    if math.isnan(b): b = 0

    # Return RGB values as an array
    return [r, g, b]

def _convert_rgb_to_xy(red, green, blue):
    '''Adapted from Sabertec configurator'''
    # Apply gamma correction to the RGB values
    red = math.pow((red + 0.055) / 1.055, 2.4) if 0.04045 < red else red / 12.92
    green = math.pow((green + 0.055) / 1.055, 2.4) if 0.04045 < green else green / 12.92
    blue = math.pow((blue + 0.055) / 1.055, 2.4) if 0.04045 < blue else blue / 12.92
    # Calculate intermediate values
    a = 0.664511 * red + 0.154324 * green + 0.162028 * blue
    t = 0.283881 * red + 0.668433 * green + 0.047685 * blue
    u = 88e-6 * red + 0.07231 * green + 0.986039 * blue
    # Calculate i and o
    i = a / (a + t + u)
    o = t / (a + t + u)
    # Handle NaN values
    if math.isnan(i): 
        i = 0
    if math.isnan(o): 
        o = 0
    return [i, o]

def get_mixed_color(r: int, g: int, b: int, w: int) -> list[int]:
    '''Returns the mixed color (as tuple of RGB 0-255 values) for the input RGBW values.
    Input: RGBW values as int (0-255). This function automatically adjusts for LED color values.'''
    
    # Get adjustment factors based on LED values.
    color_list_RGB = []
    color_list_RGB.append(_adjust_for_LED(r, _LEDs['r']))
    color_list_RGB.append(_adjust_for_LED(g, _LEDs['g']))
    color_list_RGB.append(_adjust_for_LED(b, _LEDs['b']))
    color_list_RGB.append(_adjust_for_LED(w, _LEDs['w']))

    # For each LED, convert it to XYZ color space.
    # Then use the intensity value to transform in XYZ space to get the final color for that LED
    color_list_XYZ =[]
    for color, intensity in color_list_RGB:
        tmp_x, tmp_y = _convert_rgb_to_xy(color.r, color.g, color.b)
        x = tmp_x * (intensity / tmp_y)
        y = intensity
        z = (intensity / tmp_y) * (1 - tmp_x - tmp_y)
        color_list_XYZ.append(XYZColor(x, y, z))

    # combine the colors in XYZ space
    x_sum = sum(map(
        lambda c: c.x,
        color_list_XYZ))
    y_sum = sum(map(
        lambda c: c.y,
        color_list_XYZ))
    z_sum = sum(map(
        lambda c: c.z,
        color_list_XYZ))
    if not x_sum and not y_sum and not z_sum:
        return [0, 0, 0]
    x_final = x_sum / (x_sum + y_sum + z_sum)
    y_final = y_sum / (x_sum + y_sum + z_sum)
    intensity = max(0, min(1, y_sum))
    final_rgb = _convert_xyz_to_rgb(x_final, y_final, 253 * intensity + 1)

    return(final_rgb)
