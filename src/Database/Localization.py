from enum import Enum


class LocalList(Enum):
    RU = "ru",
    EN = "en",
    UA = "ua"


class Localization:
    def __init__(self, locale: LocalList) -> None:
        self.__current_locale = locale

    @property
    def current_locale(self):
        return self.__current_locale.value[0]
