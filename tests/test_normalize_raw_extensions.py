import os
import tempfile
import unittest

from app import Main_Window


class TestNormalizeRawExtensions(unittest.TestCase):
    """The Anima requires sound file names to end in '.RAW' (case sensitive).

    normalize_raw_extensions() must return a list of paths whose file names
    all end in exactly '.RAW', without renaming the user's original files.
    See https://github.com/jramboz/tintalle/issues/42
    """

    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def _make_file(self, name: str, content: bytes = b'\x00\x01') -> str:
        path = os.path.join(self.dir, name)
        with open(path, 'wb') as f:
            f.write(content)
        return path

    def test_lowercase_extension_is_uppercased(self):
        src = self._make_file('hum_0.raw', b'abc')
        result = Main_Window.normalize_raw_extensions([src])
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]), 'hum_0.RAW')

    def test_copy_has_same_content(self):
        src = self._make_file('hum_0.raw', b'abc')
        result = Main_Window.normalize_raw_extensions([src])
        with open(result[0], 'rb') as f:
            self.assertEqual(f.read(), b'abc')

    def test_mixed_case_extension_is_uppercased(self):
        src = self._make_file('CLASH_1_0.Raw')
        result = Main_Window.normalize_raw_extensions([src])
        self.assertEqual(os.path.basename(result[0]), 'CLASH_1_0.RAW')

    def test_correct_extension_returns_original_path(self):
        src = self._make_file('BEEP.RAW')
        result = Main_Window.normalize_raw_extensions([src])
        self.assertEqual(result, [src])

    def test_original_file_is_not_renamed(self):
        src = self._make_file('swing.raw')
        Main_Window.normalize_raw_extensions([src])
        self.assertTrue(os.path.exists(src))

    def test_non_raw_extension_left_untouched(self):
        src = self._make_file('readme.txt')
        result = Main_Window.normalize_raw_extensions([src])
        self.assertEqual(result, [src])

    def test_order_is_preserved(self):
        a = self._make_file('a.raw')
        b = self._make_file('B.RAW')
        c = self._make_file('c.Raw')
        result = Main_Window.normalize_raw_extensions([a, b, c])
        self.assertEqual([os.path.basename(p) for p in result],
                         ['a.RAW', 'B.RAW', 'c.RAW'])
        self.assertEqual(result[1], b)


if __name__ == '__main__':
    unittest.main()
