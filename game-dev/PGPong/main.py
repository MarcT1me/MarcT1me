import EngineLite

from background import Background as Bg
from interface import Interface as Inf
from scene import Scene as Sc


class PinPong(EngineLite.App):
    bg: Bg
    inf: Inf
    sc: Sc

    def create(self):
        self.bg = Bg(self)
        self.sc = Sc(self)
        self.inf = Inf(self, self.sc)

    def events(self, event_list: list[EngineLite.event.Event]):
        for event in event_list:
            if event.type == EngineLite.QUIT:
                self.running = False

        self.sc.events(event_list)

    def update(self):
        self.sc.update()
        self.inf.update()

    def render(self):
        self.bg.render()
        self.sc.render()
        self.inf.render()


if __name__ == '__main__':
    app = PinPong()
    app.run()
