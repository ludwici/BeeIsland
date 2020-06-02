class QuestTemplate:
    __slots__ = ("title", "desc", "icon_pos", "resources_bag", "q_type")

    def __init__(self, title: str, q_type: int, desc: str, icon_pos: (int, int)) -> None:
        self.title = title
        self.desc = desc
        self.icon_pos = icon_pos
        self.resources_bag = None
        self.q_type = q_type
