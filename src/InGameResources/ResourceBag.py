from src.InGameResources.Resource import Resource


class ResourceBag:
    __slots__ = "__bag"

    def __init__(self) -> None:
        self.__bag = []

    @property
    def bag(self) -> list:
        return self.__bag

    def append(self, new_res: Resource) -> None:
        for r in self.__bag:
            if new_res.locale_name == r.locale_name:
                r.value += new_res.value
                return

        self.__bag.append(new_res)

    def remove(self, old_res: Resource) -> None:
        for r in self.__bag:
            if old_res.locale_name == r.locale_name:
                r.value -= old_res.value
                if r.base_value == 0:
                    self.__bag.remove(r)

    def __repr__(self) -> str:
        r = ""
        for i in self.__bag:
            r += repr(i) + " | "
        return r

    def __add__(self, other: "ResourceBag") -> "ResourceBag":
        for o in other.bag:
            self.append(o)
        return self

    def __sub__(self, other: "ResourceBag") -> "ResourceBag":
        for o in other.bag:
            self.remove(o)
        return self
