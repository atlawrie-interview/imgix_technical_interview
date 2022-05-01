from turtle import color
import unittest

from imgix_palette import palette

f_path = "treefrog.jpg"
f_domain = "static.imgix.net"

class TestPalette(unittest.TestCase):
    
    def test_palette_url(self):
        self.assertEqual("https://static.imgix.net/treefrog.jpg?colors=1&palette=json", str(palette._palette_url(f_domain, f_path, 1)))

    def test_request_palette(self):
        self.assertDictEqual(palette.request_palette(f_domain, f_path, color_count=1), {0: {'red': 1, 'hex': '#ffd806', 'blue': 0.0235294, 'green': 0.847059} })

    def test_color_dict(self):
        self.assertDictEqual(palette._color_dict(palette._palette_dict(f_domain, f_path, color_count=1), False), {0: {'red': 1, 'hex': '#ffd806', 'blue': 0.0235294, 'green': 0.847059}})

    def test_pal_dict(self):
        self.assertDictEqual(palette._palette_dict(f_domain, f_path, color_count=1), {'colors': {0: {'red': 1, 'hex': '#ffd806', 'blue': 0.0235294, 'green': 0.847059}}, 'dominant_colors': {'vibrant': {'red': 1, 'hex': '#ffd806', 'blue': 0.0235294, 'green': 0.847059}, 'muted_light': {'red': 0.827451, 'hex': '#d3cfb6', 'blue': 0.713725, 'green': 0.811765}, 'muted': {'red': 0.317647, 'hex': '#51b38f', 'blue': 0.560784, 'green': 0.701961}, 'vibrant_dark': {'red': 0.00392157, 'hex': '#018f53', 'blue': 0.32549, 'green': 0.560784}, 'vibrant_light': {'red': 0.635294, 'hex': '#a2e0da', 'blue': 0.854902, 'green': 0.878431}, 'muted_dark': {'red': 0.172549, 'hex': '#2c5556', 'blue': 0.337255, 'green': 0.333333}}, 'average_luminance': 0.296168} )
        
    def test_overlay_color(self):
        self.assertDictEqual(palette.overlay_color(f_domain, f_path, color_count = 1), {'red': 0.05762207385373725, 'green': 0.1999999999999993, 'blue': 0.008470583999999929, 'hex': '#0f3302'})

if __name__ == '__main__':
    unittest.main()


