import sys
import unittest
sys.path.append('../')

from src.BeeFamily.BeeQueen import BeeQueen
from src.BeeFamily.BeeWarrior import BeeWarrior
from src.BeeFamily.BeeWorker import BeeWorker

from src.BeeNest import BeeNest
from src.BeeFamily.Bee import Bee


class TestEntities(unittest.TestCase):
    def setUp(self) -> None:
        self.bee = Bee(parent=None, bonus=None, code="A")
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
        b = Bee(parent=None, bonus=None, code="A")

        for i in range(self.nest.max_size):
            if not self.nest.add_bee(b):
                self.fail("Too many bees")

    def test_modify1(self):
        b1 = self.modify("A", "A")
        if not isinstance(b1, BeeWorker) and not isinstance(b1, BeeWarrior):
            self.fail("Unresolved type")
        b2 = self.modify("B", "B")
        if not isinstance(b2, BeeWorker) and not isinstance(b2, BeeWarrior):
            self.fail("Unresolved type")
        b3 = self.modify("A", "B")
        if not isinstance(b3, BeeWorker) and not isinstance(b3, BeeWarrior):
            self.fail("Unresolved type")
        b4 = self.modify("1", "1")
        if not isinstance(b4, BeeWorker) and not isinstance(b4, BeeWarrior):
            self.fail("Unresolved type")

        self.assertIsInstance(self.modify("A", "1"), BeeWorker)
        self.assertIsInstance(self.modify("A", "J"), Bee)

        self.assertIsInstance(self.modify("B", "2"), BeeWarrior)
        self.assertIsInstance(self.modify("B", "J"), Bee)
        self.assertIsInstance(self.modify("2", "2"), BeeWarrior)

        self.assertIsInstance(self.modify("3", "3"), BeeQueen)

        self.assertIsNone(self.modify("Q", "Q"))
        self.assertIsNone(self.modify("Q", "J"))

    def modify(self, code1, code2):
        b1 = Bee(parent=None, bonus=None, code=code1)
        b2 = Bee(parent=None, bonus=None, code=code2)
        return b1 + b2

    def check_bee_min_max(self):
        self.assertGreaterEqual(self.bee.current_xp, 1)
        self.assertGreaterEqual(self.bee.current_level, 1)
        self.assertGreaterEqual(self.bee.current_hp, 0)

        self.assertLessEqual(self.bee.current_xp, self.bee.max_xp)
        self.assertLessEqual(self.bee.current_level, self.bee.max_level)
        self.assertLessEqual(self.bee.current_hp, self.bee.max_hp)


if __name__ == '__main__':
    unittest.main()
