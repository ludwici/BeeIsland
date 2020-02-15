import sys
import unittest
sys.path.append('../')
from src.Bee import Bee


class TestEntities(unittest.TestCase):
    def test_xp_1(self):
        b = Bee(1)
        xp = 160
        b.give_xp(xp)
        self.assertEqual(b.current_xp, 10)

    def test_xp_2(self):
        b = Bee(1)
        b.give_xp(70)
        self.assertEqual(b.current_level, 1)
        b.give_xp(100)
        self.assertEqual(b.current_level, 2)
        self.check_xp(b)

    def test_bee(self):
        b = Bee(1)
        b.give_xp(150)

    def check_xp(self, b):
        self.assertGreater(b.current_xp, 0)
        self.assertGreater(b.current_level, 0)
        self.assertGreater(b.current_hp, 0)

        self.assertLessEqual(b.current_xp, b.max_xp)
        self.assertLessEqual(b.current_level, b.max_level)
        self.assertLessEqual(b.current_hp, b.max_hp)


if __name__ == '__main__':
    unittest.main()
