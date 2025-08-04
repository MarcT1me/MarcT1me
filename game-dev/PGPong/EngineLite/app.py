from abc import ABCMeta, abstractmethod

import EngineLite
from . import AppConfig, Object


class App(Object, metaclass=ABCMeta):
    screen: EngineLite.Surface = None
    config: AppConfig = None

    def __init__(self):
        super().__init__(self)
        App.config = AppConfig()

        EngineLite.init()
        self.running = True

        App.screen = EngineLite.display.set_mode([App.config.width, App.config.height])
        self.clock = EngineLite.time.Clock()
        self.delta_time = 0

        self.event_list = []
        self.key_list: EngineLite.key.ScancodeWrapper = ()

    def run(self):
        self.create()

        while self.running:
            self.event_list = EngineLite.event.get()
            self.key_list = EngineLite.key.get_pressed()
            self.events(self.event_list)
            self.update()
            self.render()

            EngineLite.display.flip()
            self.delta_time = self.clock.tick(App.config.fps) / 1000

    @abstractmethod
    def create(self):
        pass
