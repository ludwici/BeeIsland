from src.BeeFamily.Bee import Bee


class BeeNest:
    __slots__ = ("__current_level", "__max_level", "xp_enabled", "__current_xp", "max_xp", "__bee_list", "__have_queen",
                 "__max_size")

    def __init__(self) -> None:
        self.__bee_list = []
        self.__max_size = 0
        self.__have_queen = False

    def add_queen(self) -> None:
        self.__have_queen = True

    def remove_queen(self) -> None:
        self.__have_queen = False

    @property
    def max_size(self) -> int:
        if self.__have_queen:
            return self.__max_size
        else:
            return 0

    @property
    def size(self) -> int:
        return len(self.__bee_list)

    @property
    def bee_list(self) -> list:
        return self.__bee_list

    def remove_bee(self, bee: Bee) -> None:
        self.__bee_list.remove(bee)

    def add_bee(self, bee: Bee) -> bool:
        if self.size > self.__max_size:
            return False

        self.__bee_list.append(bee)
        return True
