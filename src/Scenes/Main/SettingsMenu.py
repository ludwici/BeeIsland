import pygame
from pygame.event import Event

from src import Constants
from src.Database.Localization import Localization
from src.UI.Button import ButtonEventType, ButtonState
from src.UI.Menu import Menu
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class SettingsMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent=parent, bg_name="settings_bg")
        self._title_label.set_text(text=self.parent.localization.get_string("settings"))
        self._title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self._title_label.get_size()[0] / 2 + 10,
             self.position[1] + 3)
        )

        self.__resolution_label = TextLabel(parent=self, font_size=18, bold=True,
                                            text=self.parent.localization.get_string("resolution"))

        right1 = TextLabel(parent=self, font_size=18, bold=True, text=">")
        self.__right_resolution_button = TextButton(parent=self, text_label=right1, normal_image_path="left_right.png",
                                                    text_padding=(10, -5))
        self.__right_resolution_button.set_position(
            (self._rect.right - self.__right_resolution_button.get_size()[0] - 20, self.position[1] + 75))

        self.__resolution_val_bg = pygame.image.load("{0}/settings.png".format(self._res_dir))
        self.__resolution_val_bg_rect = self.__resolution_val_bg.get_rect()
        self.__resolution_val_bg_rect.right = self.__right_resolution_button._rect.left - 6
        self.__resolution_val_bg_rect.y = self.position[1] + 75

        self.__lang_val_bg = pygame.image.load("{0}/settings.png".format(self._res_dir))
        self.__lang_bg_rect = self.__lang_val_bg.get_rect()
        self.__lang_bg_rect.right = self.__resolution_val_bg_rect.right
        self.__lang_bg_rect.y = self.__resolution_val_bg_rect.bottom + 15

        left1 = TextLabel(parent=self, font_size=18, bold=True, text="<")
        self.__left_resolution_button = TextButton(parent=self, text_label=left1, normal_image_path="left_right.png",
                                                   text_padding=(10, -5))
        self.__left_resolution_button.set_position((self.__resolution_val_bg_rect.left
                                                    - self.__left_resolution_button.get_size()[0] - 6,
                                                    self.position[1] + 75))

        self.__resolution_label.set_position((self.__left_resolution_button.get_rect().left
                                              - self.__resolution_label.get_size()[0] - 20,
                                              self.position[1] + 72))

        self.__lang_label = TextLabel(parent=self, font_size=18, bold=True,
                                      text=self.parent.localization.get_string("lang"))

        right2 = TextLabel(parent=self, font_size=18, bold=True, text=">")
        self.__right_lang_button = TextButton(parent=self, text_label=right2, normal_image_path="left_right.png",
                                              text_padding=(10, -5))
        self.__right_lang_button.set_position((self.__right_resolution_button.position[0],
                                               self.__right_resolution_button.get_rect().bottom + 15))

        left2 = TextLabel(parent=self, font_size=18, bold=True, text="<")

        self.__left_lang_button = TextButton(parent=self, text_label=left2, normal_image_path="left_right.png",
                                             text_padding=(10, -5))
        self.__left_lang_button.set_position((self.__left_resolution_button.position[0],
                                              self.__left_resolution_button.get_rect().bottom + 15))

        self.__lang_label.set_position((self.__left_lang_button.get_rect().left - self.__lang_label.get_size()[0] - 20,
                                        self.__resolution_label.get_rect().bottom + 8))

        self.__left_resolution_button.set_image_by_state(ButtonState.HOVERED, "left_right_hover.png")
        self.__right_resolution_button.set_image_by_state(ButtonState.HOVERED, "left_right_hover.png")
        self.__left_lang_button.set_image_by_state(ButtonState.HOVERED, "left_right_hover.png")
        self.__right_lang_button.set_image_by_state(ButtonState.HOVERED, "left_right_hover.png")

        self.__right_resolution_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda: self.change_resolution(right=True)})
        self.__left_resolution_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda: self.change_resolution(right=False)})

        self.__current_resolution_label = TextLabel(parent=self, font_size=18, bold=True,
                                                    text="{0}x{1}".format(Constants.WINDOW_W, Constants.WINDOW_H))
        self.__current_resolution_label.get_rect().center = self.__resolution_val_bg_rect.center

        self.__current_lang_label = TextLabel(parent=self, font_size=18, bold=True,
                                              text=Localization.get_current_locale().upper())
        self.__current_lang_label.get_rect().center = self.__lang_bg_rect.center

        self.__right_lang_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.change_lang(right=True)})
        self.__left_lang_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.change_lang(right=False)})

        self.parent.stop_handle()

    def destroy(self):
        self.parent.remove_drawable(self.parent.find_drawable_by_type(SettingsMenu))
        super().destroy()
        self.parent.start_handle()

    def change_lang(self, right: bool) -> None:
        if right:
            self.parent.main_window.change_lang(Localization.get_full_locale().get_next())
        else:
            self.parent.main_window.change_lang(Localization.get_full_locale().get_prev())

        self.__current_lang_label.set_text(Localization.get_current_locale().upper())

    def change_resolution(self, right: bool) -> None:
        index = Constants.SIZE.index((Constants.WINDOW_W, Constants.WINDOW_H))
        index = index + (1 if right else -1)
        if index == len(Constants.SIZE):
            index = 0
        print("Next", Constants.SIZE[index])
        Constants.WINDOW_W, Constants.WINDOW_H = Constants.SIZE[index]
        self.__current_resolution_label.set_text(text="{0}x{1}".format(Constants.WINDOW_W, Constants.WINDOW_H))
        self.__current_resolution_label.get_rect().center = self.__resolution_val_bg_rect.center
        self.parent.main_window.change_resolution(Constants.SIZE[index])

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)
        self.__left_resolution_button.handle_event(event)
        self.__right_resolution_button.handle_event(event)
        self.__left_lang_button.handle_event(event)
        self.__right_lang_button.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.__resolution_label.draw(screen)
        screen.blit(self.__resolution_val_bg, self.__resolution_val_bg_rect)
        screen.blit(self.__lang_val_bg, self.__lang_bg_rect)
        self.__right_resolution_button.draw(screen)
        self.__left_resolution_button.draw(screen)
        self.__lang_label.draw(screen)
        self.__right_lang_button.draw(screen)
        self.__left_lang_button.draw(screen)
        self.__current_resolution_label.draw(screen)
        self.__current_lang_label.draw(screen)
