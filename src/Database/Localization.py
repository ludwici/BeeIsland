import json
from enum import Enum


class LocalList(Enum):
    RU = "ru",
    EN = "en",
    UA = "ua"


class Localization:
    __current_locale = LocalList.RU

    def __init__(self, scene_name: str) -> None:
        self.__scene_name = scene_name
        self.__data = self.__read_locale()

    def __read_locale(self):
        locale_path = "../res/locales/scenes/{0}.json".format(self.__scene_name,
                                                              Localization.get_current_locale())
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
    def get_current_locale():
        return Localization.__current_locale.value[0]
