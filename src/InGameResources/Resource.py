class Resource:
    __slots__ = ("locale_name", "__value", "__base_value", "max_value", "locale_desc")

    def __init__(self, locale_name, locale_desc="", amount=0, max_value=0) -> None:
        self.locale_name = locale_name
        self.locale_desc = locale_desc
        self.__value = amount
        self.__base_value = amount
        self.max_value = max_value

    def increase_by_percent(self, percent) -> None:
        self.__value = self.base_value
        self.__value += self.base_value * percent / 100

    @property
    def value(self) -> int:
        return int(self.__value)

    @value.setter
    def value(self, v: int) -> None:
        self.__value = v
        self.base_value = v

    @property
    def base_value(self) -> int:
        return self.__base_value

    @base_value.setter
    def base_value(self, value) -> None:
        self.__base_value = value
        if self.__base_value < 0:
            self.__base_value = 0
        if self.__base_value > self.max_value:
            self.__base_value = self.max_value

    def __add__(self, other) -> "Resource":
        if self.locale_name == other.locale_name:
            self.base_value += other.base_value
        return self

    def __sub__(self, other) -> "Resource":
        if self.locale_name == other.locale_name:
            self.base_value -= other.base_value
        return self

    def __bool__(self) -> bool:
        return self.__value > 0

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        r = "<Resource(name={0}, value={1}, base={2}, max_count={3})>".format(self.locale_name, self.__value,
                                                                              self.base_value, self.max_value)
        return r
