from abc import ABC, abstractmethod
from src.UI.PopupNotify import PopupNotify


class Scene(ABC):
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.drawable_list = []
        self.timer_list = []

    @abstractmethod
    def update(self, dt) -> None:
        pass

    @abstractmethod
    def handle_events(self, event) -> None:
        pass

    @abstractmethod
    def draw(self, surface) -> None:
        pass

    def check_timers(self) -> None:
        for t in self.timer_list:
            if t.done:
                self.timer_list.remove(t)

    def create_popup(self, position, text) -> None:
        popup = PopupNotify(parent=self, position=position)
        if text:
            popup.set_text(text)
        popup.show()
