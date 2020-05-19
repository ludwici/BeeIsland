from InGameResources.Resource import Resource


class ResourceBag:
    def __init__(self) -> None:
        self.__bag = []

    def get_bag_copy(self) -> list:
        return self.__bag

    def append(self, new_res: Resource) -> None:
        for r in self.__bag:
            if new_res.locale_name == r.locale_name:
                r.value += new_res.value
                return

        self.__bag.append(new_res)

    def __add__(self, other: "ResourceBag") -> "ResourceBag":
        for o in other.get_bag_copy():
            self.append(o)
        return self
