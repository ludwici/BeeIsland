import sys
import unittest

sys.path.append('../')
from src.BeeNest import BeeNest
from src.BeeFamily.Bee import Bee


class TestEntities(unittest.TestCase):
    def setUp(self) -> None:
        self.bee = Bee(parent=None, bonus=None)
        self.nest = BeeNest()

    def test_bee_xp_1(self):
        xp = 282
        self.bee.give_xp(xp)
        self.assertEqual(self.bee.current_xp, 11)
        self.check_bee_min_max()

    def test_bee_xp_2(self):
        self.bee.change_level_to(1)
        self.bee.give_xp(80)
        self.assertEqual(self.bee.current_level, 1)
        self.bee.give_xp(200)
        self.assertEqual(self.bee.current_level, 2)
        self.check_bee_min_max()

    def test_add_bee_to_nest(self):
        b = Bee(parent=None, bonus=None)

        for i in range(self.nest.max_size):
            if not self.nest.add_bee(b):
                self.fail("Too many bees")

    def check_bee_min_max(self):
        self.assertGreaterEqual(self.bee.current_xp, 1)
        self.assertGreaterEqual(self.bee.current_level, 1)
        self.assertGreaterEqual(self.bee.current_hp, 0)

        self.assertLessEqual(self.bee.current_xp, self.bee.max_xp)
        self.assertLessEqual(self.bee.current_level, self.bee.max_level)
        self.assertLessEqual(self.bee.current_hp, self.bee.max_hp)


if __name__ == '__main__':
    unittest.main()
