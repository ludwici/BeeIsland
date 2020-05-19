class QuestTemplate:
    def __init__(self, title: str, desc: str, icon_pos: (int, int)) -> None:
        self.title = title
        self.desc = desc
        self.icon_pos = icon_pos
        self.resources_bag = None
