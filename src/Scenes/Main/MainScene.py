import pygame
from pygame.event import Event

from Scenes.Main.SettingsMenu import SettingsMenu
from Scenes.Scene import Scene
from UI.Button import ButtonState, ButtonEventType
from UI.TextButton import TextButton
from UI.TextLabel import TextLabel
from src import Constants


class MainMenuScene(Scene):

    def __init__(self, main_window, name, player) -> None:
        Scene.__init__(self, main_window=main_window, name=name, player=player)
        self.__main_image = pygame.image.load("{0}/images/main_img.jpg".format(self._res_dir))
        self.__bg_image = pygame.image.load("{0}/images/main_bg.jpg".format(self._res_dir))
        self.__main_rect = self.__main_image.get_rect()
        self.__bg_rect = self.__bg_image.get_rect()
        self.__main_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)

        start_label = TextLabel(parent=self, font_size=18, bold=True)
        settings_label = TextLabel(parent=self, font_size=18, bold=True)
        exit_label = TextLabel(parent=self, font_size=18, bold=True)

        self.__start_button = TextButton(parent=self, text_label=start_label,
                                         normal_image_path="start_quest_btn_normal.png")
        self.__start_button.set_position((self.__main_rect.centerx - self.__start_button.get_size()[0] / 2, 240))
        self.__start_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.__settings_button = TextButton(parent=self, text_label=settings_label,
                                            normal_image_path="start_quest_btn_normal.png")
        self.__settings_button.set_position((self.__start_button.position[0],
                                             self.__start_button.get_rect().bottom + 20))
        self.__settings_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.__exit_button = TextButton(parent=self, text_label=exit_label,
                                        normal_image_path="start_quest_btn_normal.png")
        self.__exit_button.set_position((self.__settings_button.position[0],
                                         self.__settings_button.get_rect().bottom + 20))
        self.__exit_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.__start_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.change_scene("Farm")})
        self.__settings_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show_settings()})
        self.__exit_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.exit_game()})

    def exit_game(self):
        self.main_window.stop()

    def on_scene_started(self) -> None:
        super().on_scene_started()
        self.__start_button.set_text(text=self._localization.get_string("start"))
        self.__start_button.set_padding(padding=(self._localization.get_params_by_string("start")["padding"], 3))

        self.__settings_button.set_text(text=self._localization.get_string("settings"))
        self.__settings_button.set_padding(padding=(self._localization.get_params_by_string("settings")["padding"], 3))

        self.__exit_button.set_text(text=self._localization.get_string("exit"))
        self.__exit_button.set_padding(padding=(self._localization.get_params_by_string("exit")["padding"], 3))

    def stop_handle(self):
        self.__start_button.stop_handle()
        self.__settings_button.unselect()
        self.__settings_button.stop_handle()
        self.__exit_button.stop_handle()

    def start_handle(self):
        self.__start_button.start_handle()
        self.__settings_button.start_handle()
        self.__exit_button.start_handle()

    def show_settings(self):
        SettingsMenu(parent=self)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((38, 34, 35))
        surface.blit(self.__bg_image, self.__bg_rect)
        surface.blit(self.__main_image, self.__main_rect)
        self.__start_button.draw(surface)
        self.__settings_button.draw(surface)
        self.__exit_button.draw(surface)
        super().draw(surface)

    def handle_events(self, event: Event) -> None:
        [d.handle_event(event) for d in self._drawable_list]
        self.__start_button.handle_event(event)
        self.__settings_button.handle_event(event)
        self.__exit_button.handle_event(event)
