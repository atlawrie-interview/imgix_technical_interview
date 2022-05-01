import colorsys

# defined https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
R_RELATIVE_LUM_RATIO = 0.2126
G_RELATIVE_LUM_RATIO = 0.7152
B_RELATIVE_LUM_RATIO = 0.0722


def rgb_to_hex(rgb):
    """
    Converts a sgb value to hex.

    Parameters
    ----------
    rgb: tuple[float]
        A float representation of a color in rgb space.

    Returns
    -------
    str
        A hex string representation of a color in rgb space.
    """
    return '%02x%02x%02x' % (round(rgb[0]*255), round(rgb[1]*255), round(rgb[2]*255))

def contrast_ratio(luminance_x, luminance_y):
    """
    Calculates the contrast ratio defined at https://www.w3.org/TR/WCAG21/#contrast-enhanced

    Parameters
    ----------
    luminance_x: float
     
    luminance_y: float

    Returns
    -------
        The calculated contrast ratio. 

    """
    if luminance_x>luminance_y:
        return (luminance_x + 0.05)/(luminance_y + 0.05)
    return (luminance_y + 0.05)/(luminance_x + 0.05)

def max_contrast(luminance, ceiling = 4.5):
    """
    Calculates the max possible contrast for a given luminance less than or equal to a provided contrast ratio. 
    See https://www.w3.org/TR/WCAG21/#contrast-enhanced

    Parameters
    ----------
    luminance: float

    ceiling: float
        The upper bound of the contrast ratio.

    Returns
    -------
    float
        The max possible contrast less than or equal to ceiling.

    """
    zero_c = contrast_ratio(0.0, luminance)
    one_c = contrast_ratio(1.0, luminance)
    potential_contrast = max(zero_c, one_c)
    return min(potential_contrast, ceiling)

def contrast_to_luminance(contrast, lum):
    """
    Solves for the luminance value of a color when provided a known luminance and the known contrast ratio. 
    See https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    Parameters
    ----------
    contrast: float
    
    lum: float
        The known luminance.

    Returns
    -------
    float
        The unknown luminance.

    """
    x = 0.05*(20*lum*contrast + contrast - 1) #if lum is denominator
    y = (lum - 0.05*contrast + 0.05) / contrast #if lum is numerator

    if (y >= 0 and y <= 1):
        return y
    else:
        return x

def rgb_relative_lum(rgb):
    """
    Returns the relative luminance of a rgb color. See https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    Parameters
    ----------
    rgb: tuple[float]
        A tuple containing a float representation of a rgb color.

    Returns
    -------
    float
        The relative luminance.

    """
    if rgb[0] > 0.03928:
        r = ((rgb[0]+0.055)/1.055)**2.4
    else:
        r = rgb[0]/12.92
    
    if rgb[1] > 0.03928:
        g = ((rgb[1]+0.055)/1.055)**2.4
    else:
        g = rgb[1]/12.92

    if rgb[2] > 0.03928:
        b = ((rgb[2]+0.055)/1.055)**2.4
    else:
        b = rgb[2]/12.92
    
    return (r*R_RELATIVE_LUM_RATIO + g*G_RELATIVE_LUM_RATIO + b*B_RELATIVE_LUM_RATIO)

def contrast(rgb_a, rgb_b):
    """
    Calculates the contrast ratio between two rgb colors. 
    See https://www.w3.org/TR/WCAG21/#contrast-enhanced

    Parameters
    ----------
    rgb_a: tuple[float]
        A tuple containing a float representation of a rgb color.

    rgb_b: tuple[float]
        A tuple containing a float representation of a rgb color.

    Returns
    -------
    float
        The calculated contrast ratio.

    """
    return contrast_ratio(rgb_relative_lum(rgb_a), rgb_relative_lum(rgb_b))
    
def average_rgb(rgb_colors):
    """
    Averages colors in rgb space.

    Parameters
    ----------
    rgb_colors: list[tuple[float]]
        A list of float representations of rgb colors.

    Returns
    -------
    tuple[float]
        A float representation of the averaged rgb color
    """
    r_sum = 0.0
    g_sum = 0.0
    b_sum = 0.0
    for color in rgb_colors:
        r_sum += color[0]
        g_sum += color[1]
        b_sum += color[2]
    color_count = len(rgb_colors)
    return (r_sum/color_count, g_sum/color_count, b_sum/color_count)

def find_contrasting_color(colors, hue_shift, ratio, lum=None):
    """
    Returns a color that meets web accessibility contrast guidelines as best as possible when compared with the average luminance of the provided colors

    Parameters
    ----------
    colors: list[tuple[float]]
        A list of float representations of rgb colors.
        
    hue_shift: float
        A float specifying the percentage with which to shift the hue value of the returned color in comparison to the average rgb value of the colors

    ratio: float
        A float specifying the desired contrast ratio of the returned color compared to the provided luminance.

    lum: float
        A float specifying the luminance with which to evaluate the contrast ratio against. If this value is not provided, the luminance of the averaged rgb color is used. (default:None)

    Returns
    -------
    tuple[float]
        A float representation of a rgb color.
    """
    rgb = average_rgb(colors)
    if lum is None:
        lum = rgb_relative_lum(rgb)
    m_contrast = max_contrast(lum, ceiling=ratio)
    lum_p = contrast_to_luminance(m_contrast, lum)
    rgb_p = hsv_sweep(rgb, lum_p, hue_shift)

    return rgb_p

def hsv_sweep(rgb, lum, hue_shift):
    """
    Attempts to transform a rgb value along hsv colorspace so as to meet or exceed the provided luminance value. 
    Additionally shifts the hue value by a provided percentage to create an analogous color.

    Parameters
    ----------
    rgb: tuple[float]
        A float representation of the rgb color to transform.

    lum: float
        The desired relative luminance. See https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    hue_shift: float
        The percentage by which to shift the hue value of the provided rgb color.

    Returns
    -------
    tuple[float]
        A float representation of the transformed color.
    """

    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    h = (hsv[0] + hue_shift)%1 #Offset hue by hue_shift
    s = hsv[1]
    v = hsv[2]

    increasing = lum > .5
    
    
    s_diff = abs(round(s)-s)
    v_diff = abs(round(v)-v)
    if round(v) == 0: #Have saturation and value converge to the furthest boundary
        v_sign = 1
    else:
        v_sign = -1
    if round(s) == 0:
        s_sign = 1
    else:
        s_sign = -1
    if s_diff > v_diff:
        v_offset = 0.01 * v_sign #Iterate by a minimum of 1% each loop, guaranteeing max of 100 iterations
        if v_diff != 0:
            s_offset = (s_diff/v_diff) *0.01 * s_sign #Make sure the saturation and value offsets are proportional
        else:
            s_offset = s_diff *0.01 * s_sign

    else:
        s_offset = 0.01 * s_sign
        if s_diff != 0:
            v_offset = (v_diff/s_diff) *0.01 * v_sign
        else:
            v_offset = v_diff *0.01 * v_sign
    #Offset saturation and value each loop, with boundaries of 0 and 1
    while (s > 0 and s < 1) or (v > 0 and v < 1):
        s += s_offset
        v += v_offset

        if s > 1:
            s = 1
        elif s < 0:
            s = 0

        if v > 1:
            v = 1
        elif v < 0:
            v = 0
        
        lum_p = rgb_relative_lum(colorsys.hsv_to_rgb(h, s, v))
        #If we meet the minimum contrast ratio, return the contrasting color
        if increasing and lum_p >= lum:
            return colorsys.hsv_to_rgb(h, s, v)
        elif not increasing and lum_p <= lum:
            return colorsys.hsv_to_rgb(h, s, v)

    return colorsys.hsv_to_rgb(h, s, v)
