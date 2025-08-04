import EngineLite


class Background(EngineLite.Object):
    line_width = 4

    def __init__(self, app: EngineLite.App):
        super().__init__(app)

    def events(self, event_list: list[EngineLite.event.Event]):
        pass

    def update(self):
        pass

    def render(self):
        line_center = ((self.app.config.width//2) - self.line_width//2, 0, self.line_width, self.app.config.height)
        line_box = (0, 0, self.app.config.width, self.app.config.height)

        EngineLite.App.screen.fill((10, 34, 10))
        EngineLite.draw.rect(
            EngineLite.App.screen,
            (33, 158, 28),
            line_center,
        )
        EngineLite.draw.rect(
            EngineLite.App.screen,
            (33, 158, 28),
            line_box,
            width=self.line_width,
        )


