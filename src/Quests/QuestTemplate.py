class QuestTemplate:
    __slots__ = ("title", "desc", "icon_pos", "resources_bag", "q_type", "zone_id", "quest_id")

    def __init__(self, title: str, q_type: int, desc: str, icon_pos: (int, int), zone_id: int, quest_id: int) -> None:
        self.title = title
        self.desc = desc
        self.icon_pos = icon_pos
        self.resources_bag = None
        self.q_type = q_type
        self.zone_id = zone_id
        self.quest_id = quest_id
