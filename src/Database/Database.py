import sqlite3

from src.Database.Localization import Localization
from src.InGameResources.Resource import Resource
from src.InGameResources.ResourceBag import ResourceBag
from src.Quests.QuestTemplate import QuestTemplate


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
        self.__localization = Localization.get_current_locale()
        self.conn = sqlite3.connect("{0}/main.db".format(self._db_location_dir))

    def __del__(self):
        self.conn.close()

    def get_all_quests(self) -> list:
        query = open("{0}/scripts/get_all_quests.sql".format(self._db_location_dir), 'r').read()
        cursor = self.conn.execute(query, (self.__localization, self.__localization))
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
        cursor = self.conn.execute(query, (self.__localization, quest_id))
        rewards = cursor.fetchall()
        return rewards

    def get_resource_by_id(self, res_id: int) -> Resource:
        query = open("{0}/scripts/get_resource_by_id.sql".format(self._db_location_dir), 'r').read()
        cursor = self.conn.execute(query, (self.__localization, res_id))
        template = cursor.fetchone()
        r = Resource(locale_name=template[1], max_value=template[2])
        return r
