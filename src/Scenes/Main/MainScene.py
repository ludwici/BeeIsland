import pygame
from pygame.event import Event

from src import Constants
from src.Scenes.Main.SettingsMenu import SettingsMenu
from src.Scenes.Scene import Scene
from src.UI.Button import ButtonState, ButtonEventType
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class MainMenuScene(Scene):
    __slots__ = ("main_image", "bg_image", "bg_rect", "main_rect", "start_button", "settings_button", "exit_button")

    def __init__(self, main_window, name, player) -> None:
        Scene.__init__(self, main_window=main_window, name=name, player=player)
        self.main_image = pygame.image.load("{0}/images/main_img.jpg".format(self._res_dir))
        self.bg_image = pygame.image.load("{0}/images/main_bg.jpg".format(self._res_dir))
        self.main_rect = self.main_image.get_rect()
        self.bg_rect = self.bg_image.get_rect()
        self.main_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)

        start_label = TextLabel(parent=self, font_size=18, bold=True)
        settings_label = TextLabel(parent=self, font_size=18, bold=True)
        exit_label = TextLabel(parent=self, font_size=18, bold=True)

        self.start_button = TextButton(parent=self, text_label=start_label,
                                       normal_image_path="start_quest_btn_normal.png")
        self.start_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.settings_button = TextButton(parent=self, text_label=settings_label,
                                          normal_image_path="start_quest_btn_normal.png")
        self.settings_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.exit_button = TextButton(parent=self, text_label=exit_label,
                                      normal_image_path="start_quest_btn_normal.png")
        self.exit_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.start_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.change_scene("Farm")})
        self.settings_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show_settings()})
        self.exit_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.exit_game()})

    def exit_game(self):
        self.main_window.stop()

    def on_scene_started(self) -> None:
        super().on_scene_started()
        self.main_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)

        self.start_button.set_position((self.main_rect.centerx - self.start_button.size[0] / 2, 240))
        self.settings_button.set_position((self.start_button.position[0],
                                           self.start_button.get_rect().bottom + 20))
        self.exit_button.set_position((self.settings_button.position[0],
                                       self.settings_button.get_rect().bottom + 20))

        self.start_button.set_text(text=self._localization.get_string("start"))
        self.start_button.set_padding(padding=(self._localization.get_params_by_string("start")["padding"], 3))

        self.settings_button.set_text(text=self._localization.get_string("settings"))
        self.settings_button.set_padding(padding=(self._localization.get_params_by_string("settings")["padding"], 3))

        self.exit_button.set_text(text=self._localization.get_string("exit"))
        self.exit_button.set_padding(padding=(self._localization.get_params_by_string("exit")["padding"], 3))

        s = self.find_render_by_type(SettingsMenu)
        if s:
            s.destroy()
            self.show_settings()

    def stop_handle(self):
        self.start_button.stop_handle()
        self.settings_button.unselect()
        self.settings_button.stop_handle()
        self.exit_button.stop_handle()

    def start_handle(self):
        self.start_button.start_handle()
        self.settings_button.start_handle()
        self.exit_button.start_handle()

    def show_settings(self):
        SettingsMenu(parent=self)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((38, 34, 35))
        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.main_image, self.main_rect)
        self.start_button.draw(surface)
        self.settings_button.draw(surface)
        self.exit_button.draw(surface)
        super().draw(surface)

    def handle_events(self, event: Event) -> None:
        [r.handle_event(event) for r in self._render_list]
        self.start_button.handle_event(event)
        self.settings_button.handle_event(event)
        self.exit_button.handle_event(event)
