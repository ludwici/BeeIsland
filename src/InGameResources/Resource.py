from copy import copy


class Resource:
    __slots__ = ("locale_name", "value", "_base_value", "max_value")

    def __init__(self, locale_name, amount=0, max_value=0) -> None:
        self.locale_name = locale_name
        self.value = amount
        self._base_value = amount
        self.max_value = max_value

    def increaseByPercent(self, percent) -> None:
        self.value = self.base_value
        self.value += self.base_value * percent / 100

    @property
    def base_value(self) -> int:
        return copy(self._base_value)

    @base_value.setter
    def base_value(self, value) -> None:
        self._base_value = value

    def __add__(self, other) -> "Resource":
        if self.locale_name == other.locale_name:
            self.value += other.value
        return self

    def __bool__(self) -> bool:
        return self.value > 0

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        r = "<Resource(name={0}, value={1}, base={2}, max_count={3})>".format(self.locale_name, self.value,
                                                                              self.base_value, self.max_value)
        return r
