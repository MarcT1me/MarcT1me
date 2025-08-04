import time

import EngineLite
from background import Background as Bg
from scene import Scene as Scene


class Interface(EngineLite.Object):
    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app)

        self.fps_display = FpsDisplay(app)
        self.counter_display = CounterDisplay(app, scene)

    def events(self, event_list: list[EngineLite.event.Event]):
        self.fps_display.events(event_list)
        self.counter_display.events(event_list)

    def update(self):
        self.fps_display.update()
        self.counter_display.update()

    def render(self):
        self.fps_display.render()
        self.counter_display.render()


class FpsDisplay(EngineLite.Object):
    cooldown: int = 1 / 5

    def __init__(self, app: EngineLite.App):
        super().__init__(app)

        self.font = EngineLite.font.SysFont("Arial", 18)
        self.content_fps = 0
        self.last_update_time = 0

    def events(self, event_list: list[EngineLite.event.Event]):
        pass

    def update(self):
        current_time = time.time()

        if self.last_update_time + self.cooldown <= current_time:
            self.content_fps = int(self.app.clock.get_fps())
            self.last_update_time = current_time

    def render(self):
        EngineLite.App.screen.blit(
            self.font.render(
                f"FPS: {self.content_fps}",
                True,
                (255, 255, 255)
            ),
            [Bg.line_width] * 2
        )


class CounterDisplay(EngineLite.Object):
    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app)
        self.scene = scene

        self.font = EngineLite.font.SysFont("Arial", 80)
        self.content_counter_left_player = 5
        self.content_counter_right_player = 2

    def events(self, event_list: list[EngineLite.event.Event]):
        pass

    def update(self):
        self.content_counter_left_player = self.scene.left_player.counter
        self.content_counter_right_player = self.scene.right_player.counter

    def render(self):
        rnd_font = self.font.render(
            f"{self.content_counter_left_player}",
            True,
            (33, 158, 28, 255)
        )
        rnd_pos = (self.app.config.width // 3 * 1 - rnd_font.get_width() // 2, Bg.line_width * 2)
        self.blit(rnd_font, rnd_pos)

        rnd_font = self.font.render(
            f"{self.content_counter_right_player}",
            True,
            (33, 158, 28, 255)
        )
        rnd_pos = [self.app.config.width / 3 * 2 - rnd_font.get_width() / 2, Bg.line_width * 2]
        self.blit(rnd_font, rnd_pos)
