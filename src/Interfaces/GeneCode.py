class GeneCode:
    def __init__(self) -> None:
        self.current_level = 1
        self.speed_mod = 0
        self._base_speed = 0
        self._min_hp = 0
        self._max_hp = 65
        self._current_hp = 65
        self.hp_mod = 0
        self.generation = 0

    @property
    def max_hp(self) -> int:
        return self._max_hp + self.hp_mod

    @max_hp.deleter
    def max_hp(self) -> None:
        del self.hp_mod
        del self._max_hp

    @property
    def speed(self) -> float:
        return round(self._base_speed + self.speed_mod, 2)

    @speed.deleter
    def speed(self) -> None:
        del self.speed_mod
        del self._base_speed

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value) -> None:
        if value < self._min_hp:
            self._current_hp = self._min_hp
        elif value >= self.max_hp:
            self._current_hp = self.max_hp
        else:
            self._current_hp = value

    @current_hp.deleter
    def current_hp(self) -> None:
        del self._current_hp
