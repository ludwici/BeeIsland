class Resource:
    def __init__(self, name, locale_name, amount=0) -> None:
        self.name = name
        self.locale_name = locale_name
        self.value = amount
        self.base_value = amount
        self.max_value = 0

    def increaseByPercent(self, percent) -> None:
        self.value = self.base_value
        self.value += self.base_value * percent / 100

    def __add__(self, other) -> "Resource":
        if self.name == other.name:
            self.value += other.value
        return self

    def __bool__(self) -> bool:
        return self.value > 0

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        r = "<Resource(Name={0}, value={1}, base={2})>".format(self.name, self.value, self.base_value)
        return r


class ResourceBag:
    def __init__(self) -> None:
        self.__bag = []

    def get_bag_copy(self) -> list:
        return self.__bag

    def append(self, new_res: Resource) -> None:
        for r in self.__bag:
            if new_res.name == r.name:
                r.value += new_res.value
                return

        self.__bag.append(new_res)

    def __add__(self, other: "ResourceBag") -> "ResourceBag":
        for o in other.get_bag_copy():
            self.append(o)
        return self
