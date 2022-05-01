
# imgix-palette

`imgix-palette` is a small python library for generating palettes and overlay colors from [imgix](https://www.imgix.com/) image URLs

---
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Dependencies
- [imgix-python](https://github.com/imgix/imgix-python)
- [requests](https://docs.python-requests.org/en/latest/)

## Installation

``` bash
pip install \path\to\imgix_technical\
```

## Usage

Both functions heavily leverage the imgix [palette](https://docs.imgix.com/apis/rendering/color-palette/palette) parameter.

### imgix_palette.palette.palette_request

Returns a dict representing a color palette leveraging the imgix palette parameter. See https://docs.imgix.com/apis/rendering/color-palette/palette

#### Parameters
`domain` : A string specifying the domain to use for URLs

`path` : A string specifying a path to the desired image

`color_count` : An optional int specifying the size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors

`dominance` : An optional boolean specifying whether the user wishes to recieve the dominance palette if possible.

``` python
>>> from imgix_palette import palette
>>> palette.request_palette("static.imgix.net", "treefrog.jpg")
'{0: {'red': 1, 'hex': '#ffd806', 'blue': 0.0235294, 'green': 0.847059}, 
1: {'red': 0.423529, 'hex': '#6cca9a', 'blue': 0.603922, 'green': 0.792157}, 
2: {'red': 0.0470588, 'hex': '#0ca46e', 'blue': 0.431373, 'green': 0.643137}, 
3: {'red': 0.0117647, 'hex': '#039776', 'blue': 0.462745, 'green': 0.592157}, 
4: {'red': 0.337255, 'hex': '#566363', 'blue': 0.388235, 'green': 0.388235}, 
5: {'red': 0.27451, 'hex': '#463a4a', 'blue': 0.290196, 'green': 0.227451}}'

```

### imgix_palette.palette.overlay_color

Returns a dict representing a suitable color to be overlayed over a specified image. Uses https://www.w3.org/TR/WCAG21/#contrast-enhanced as a criterion for success, and optionally shifts the hue value to an analagous color.

#### Parameters
`domain` : A string specifying the domain to use for URLs

`path` : A string specifying a path to the desired image

`color_count` : An optional int specifying the size of the default palette. See https://docs.imgix.com/apis/rendering/color-palette/colors

`dominance` : An optional boolean specifying whether the user wishes to use the dominance palette if possible.

`hue_shift` : An optional float specifying the percentage by which to shift the hue of the overlay color.

`contrast_ratio` : An optional float specifying the desired contrast ratio.

``` python
>>> from imgix_palette import palette
>>> palette.overlay_color("static.imgix.net", "treefrog.jpg")
'{'red': 0.05762207385373725, 'green': 0.1999999999999993, 'blue': 0.008470583999999929, 'hex': '#0f3302'}

```

## License
Published under [The MIT License](https://opensource.org/licenses/MIT)
