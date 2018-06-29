import json
import unittest
from backend.ecommerce import Ecommerce


class EcommerceTest(unittest.TestCase):
    def _testing_level_base(self, level):
        with open('{}/output.json'.format(level)) as output_json:
            self.assertEqual(Ecommerce(level).create_output(), json.load(output_json))

    def test_level1(self):
        self._testing_level_base(level='level1')

    def test_level2(self):
        self._testing_level_base(level='level2')

    def test_level3(self):
        self._testing_level_base(level='level2')


if __name__ == '__main__':
    unittest.main()
