from abc import ABC, abstractmethod

import EngineLite


class Object(ABC):
    def __init__(self, app: 'EngineLite.App'):
        self.app = app

    @abstractmethod
    def events(self, event_list: list[EngineLite.event.Event]):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

    def blit(self, surface: EngineLite.Surface, pos: tuple[int, int]):
        self.app.screen.blit(
            surface,
            pos
        )

        if not self.app.config.IS_RELEASE:
            rect = surface.get_rect()
            rect.topleft = pos
            EngineLite.draw.rect(
                self.app.screen,
                (0, 255, 0),
                rect,
                width=2,
            )
            EngineLite.draw.circle(
                self.app.screen,
                (255, 0, 0),
                pos,
                radius=2,
            )
