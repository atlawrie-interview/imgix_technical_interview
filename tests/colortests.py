
import unittest
from imgix_palette import colorutils

white = (1.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0)

class TestColorUtils(unittest.TestCase):
    def test_hex_conversion(self):
        self.assertEqual("0080ff", colorutils.rgb_to_hex((0.0, 0.5, 1.0)))
        self.assertEqual("ffffff", colorutils.rgb_to_hex(white))
        self.assertEqual("000000", colorutils.rgb_to_hex(black))

    def test_contrast_ratio(self):
        self.assertEqual(colorutils.contrast_ratio(0, 0), 1)
        self.assertEqual(colorutils.contrast_ratio(1.0, 0), 21)

    def test_relative_lum(self):
        self.assertEqual(colorutils.rgb_relative_lum(black), 0)
        self.assertEqual(colorutils.rgb_relative_lum(white), 1)
        
    def test_average_rgb(self):
        self.assertEqual(colorutils.average_rgb((black, white)), (0.5, 0.5, 0.5))

    def test_contrast(self):
        self.assertEqual(21, colorutils.contrast(white, black))

    def test_max_contrast(self):
        self.assertEqual(4.5, colorutils.max_contrast(0.0))

    def test_contrast_to_luminance(self):
        self.assertEqual(1.0, colorutils.contrast_to_luminance(21, 0.0))

    def test_contrasting_color(self):
        colors = [(223/255, 240/255, 216/255)]
        ratio = 4.5
        contrasting_color = colorutils.find_contrasting_color(colors, .15, ratio)
        self.assertLessEqual(ratio, colorutils.contrast(colors[0], contrasting_color))


if __name__ == '__main__':
    unittest.main()
