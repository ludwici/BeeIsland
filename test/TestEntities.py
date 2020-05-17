import sys
import unittest
sys.path.append('../')
from src.BeeNest import BeeNest
from src.BeeFamily.Bee import Bee


class TestEntities(unittest.TestCase):
    def test_bee_xp_1(self):
        b = Bee(1)
        xp = 160
        b.give_xp(xp)
        self.assertEqual(b.current_xp, 61)

    def test_nest_xp_1(self):
        n = BeeNest(1)
        xp = 3
        n.give_xp(xp)
        # print(n.current_level)
        n.give_xp(xp)
        # print(n.current_level)
        self.test_nest_min_max(n)

    def test_bee_xp_2(self):
        b = Bee(1)
        b.give_xp(70)
        self.assertEqual(b.current_level, 1)
        b.give_xp(100)
        self.assertEqual(b.current_level, 2)
        self.test_bee_min_max(b)

    def test_bee(self):
        b = Bee(1)
        b.give_xp(150)

    def test_add_bee_to_nest(self):
        b = Bee(1)
        n = BeeNest(1)

        for i in range(n.max_size):
            if not n.add_bee(b):
                self.fail("Too many bees")

        self.test_nest_min_max(n)

    def test_nest_min_max(self, n=BeeNest()):
        self.assertGreaterEqual(n.current_xp, 1)
        self.assertGreaterEqual(n.current_level, 1)

        self.assertLessEqual(n.current_xp, n.max_xp)
        self.assertLessEqual(n.current_level, n.max_level)
        self.assertLessEqual(n.size, n.max_size)

    def test_bee_min_max(self, b=Bee()):
        self.assertGreaterEqual(b.current_xp, 1)
        self.assertGreaterEqual(b.current_level, 1)
        self.assertGreaterEqual(b.current_hp, 0)

        self.assertLessEqual(b.current_xp, b.max_xp)
        self.assertLessEqual(b.current_level, b.max_level)
        self.assertLessEqual(b.current_hp, b.max_hp)


if __name__ == '__main__':
    unittest.main()
