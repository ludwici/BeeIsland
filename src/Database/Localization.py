import json
from enum import Enum

from src.Utils import resource_path


class LocalList(Enum):
    RU = "ru",
    EN = "en",
    UA = "ua"

    def next(self):
        if self == LocalList.RU:
            return LocalList.EN
        if self == LocalList.EN:
            return LocalList.UA
        if self == LocalList.UA:
            return LocalList.RU

    def prev(self):
        if self == LocalList.RU:
            return LocalList.UA
        if self == LocalList.EN:
            return LocalList.RU
        if self == LocalList.UA:
            return LocalList.EN


class Localization:
    __current_locale = LocalList.RU

    def __init__(self, path: str) -> None:
        self.__path = path
        self.__data = self.__read_locale()

    def __read_locale(self):
        locale_path = resource_path("res/locales/{0}.json".format(self.__path))
        with open(locale_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    def get_string(self, str_id: str) -> str:
        return self.get_params_by_string(str_id)["text"]

    def get_params_by_string(self, str_id: str):
        return self.__data[Localization.get_current_locale()][str_id]

    @staticmethod
    def set_locale(locale: LocalList):
        Localization.__current_locale = locale

    @staticmethod
    def get_full_locale():
        return Localization.__current_locale

    @staticmethod
    def get_current_locale():
        return Localization.__current_locale.value[0]
