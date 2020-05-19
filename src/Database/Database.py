import sqlite3

from Database.Localization import Localization
from InGameResources.Resource import Resource
from InGameResources.ResourceBag import ResourceBag
from Quests.QuestTemplate import QuestTemplate


class Database:
    __instance = None

    @staticmethod
    def get_instance() -> "Database":
        if not Database.__instance:
            Database()
        return Database.__instance

    def __init__(self) -> None:
        if Database.__instance is not None:
            raise Exception("This class is singleton")
        else:
            Database.__instance = self
        self._db_location_dir = "../res/db"
        self.__localization = None
        self.conn = sqlite3.connect("{0}/main.db".format(self._db_location_dir))

    def __del__(self):
        self.conn.close()

    @property
    def localization(self) -> Localization:
        return self.__localization

    @localization.setter
    def localization(self, value):
        self.__localization = value

    def get_all_quests(self) -> list:
        query = open("{0}/scripts/get_all_quests.sql".format(self._db_location_dir), 'r').read()
        cursor = self.conn.execute(query, (self.localization.current_locale, self.localization.current_locale))
        all_quests = cursor.fetchall()
        template_list = []
        for i in all_quests:
            q = QuestTemplate(title=i[1], desc=i[2], icon_pos=(i[3], i[4]))
            rb = ResourceBag()
            for j in self.get_rewards_by_quest_id(i[0]):
                r = self.get_resource_by_id(j[0])
                r.base_value = j[2]
                rb.append(r)
            q.resources_bag = rb
            template_list.append(q)
        return template_list

    def get_rewards_by_quest_id(self, quest_id: int):
        query = open("{0}/scripts/get_rewards_by_quest_id.sql".format(self._db_location_dir), 'r').read()
        cursor = self.conn.execute(query, (self.localization.current_locale, quest_id))
        rewards = cursor.fetchall()
        return rewards

    def get_resource_by_id(self, res_id: int) -> Resource:
        query = open("{0}/scripts/get_resource_by_id.sql".format(self._db_location_dir), 'r').read()
        cursor = self.conn.execute(query, (self.localization.current_locale, res_id))
        template = cursor.fetchone()
        r = Resource(locale_name=template[1], max_value=template[2])
        return r
