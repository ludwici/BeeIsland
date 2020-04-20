from src.UI.RadioButton import RadioButton


class BeeSocket(RadioButton):
    def __init__(self, parent, group, path_to_image: str, selected_image: str, is_selected: bool = False,
                 is_locked: bool = False, position: (int, int) = (0, 0)) -> None:
        RadioButton.__init__(self, parent=parent, group=group, path_to_image=path_to_image,
                             selected_image=selected_image, is_selected=is_selected, is_locked=is_locked,
                             position=position)
        self.bee = None
