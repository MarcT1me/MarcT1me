from random import randrange
from abc import ABCMeta, abstractmethod

from pyglm import glm

import EngineLite


class Scene(EngineLite.Object):
    collide_rect_sizes = 100

    goal_event_type: int = EngineLite.event.custom_type()

    def __init__(self, app: EngineLite.App):
        super().__init__(app)

        self.upper_border = EngineLite.Rect(
            0, -Scene.collide_rect_sizes,
            self.app.config.width, Scene.collide_rect_sizes
        )
        self.lower_border = EngineLite.Rect(
            0, self.app.config.height,
            self.app.config.width, Scene.collide_rect_sizes
        )
        self.ball = Ball(app, self)
        self.left_player = Player.type_from_side("left")(app, self)
        self.right_player = Player.type_from_side("right")(app, self)

    def events(self, event_list: list[EngineLite.event.Event]):
        self.ball.events(event_list)
        self.left_player.events(event_list)
        self.right_player.events(event_list)

    def update(self):
        self.ball.update()
        self.left_player.update()
        self.right_player.update()

    def render(self):
        self.ball.render()
        self.left_player.render()
        self.right_player.render()

        EngineLite.draw.rect(
            self.app.screen,
            "red",
            self.upper_border
        )
        EngineLite.draw.rect(
            self.app.screen,
            "blue",
            self.lower_border
        )


class SceneObject(EngineLite.Object, metaclass=ABCMeta):
    size_x: int = 20
    size_y: int = 20
    speed_factor = 1

    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app)
        self.scene = scene

        self.is_moving = False
        self.velocity: glm.vec2 = glm.vec2(0, 0)
        self.position: glm.vec2 = self.init_pos

        self.rect: EngineLite.Rect = EngineLite.Rect(0, 0, self.size_x, self.size_y)
        self.rect.center = self.position

    @property
    @abstractmethod
    def init_pos(self) -> tuple[float, float]:
        pass

    def reset_position(self):
        self.position = self.init_pos
        self.rect.center = self.position

    def render(self):
        EngineLite.draw.rect(
            self.app.screen,
            (33, 158, 28, 255),
            self.rect,
        )


class Ball(SceneObject):
    size_x: int = 14

    size_y: int = 14
    speed_factor = 400

    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app, scene)

    @property
    def init_pos(self) -> tuple[float, float]:
        return self.app.config.width / 2, self.app.config.height / 2

    def events(self, event_list: list[EngineLite.event.Event]):
        for event in event_list:
            if event.type == EngineLite.KEYDOWN:
                if event.key == EngineLite.K_RETURN:
                    self.is_moving = True
                    self.set_random_velocity()
                    self.reset_position()
            elif event.type == Scene.goal_event_type:
                self.is_moving = False
                self.set_random_velocity()
                self.reset_position()
                event.player.opponent.counter += 1

    def set_random_velocity(self):
        self.velocity = glm.normalize(
            glm.vec2(
                randrange(-1000, 1000),
                randrange(-1000, 1000)
            )
        )

    def update(self):
        if not self.is_moving:
            return

        dxy = self.velocity * self.app.delta_time
        self.position += dxy * self.speed_factor
        self.rect.center = self.position

        for player in [self.scene.left_player, self.scene.right_player]:
            if self.rect.colliderect(player.goal_rect):
                EngineLite.event.post(
                    EngineLite.event.Event(
                        Scene.goal_event_type,
                        player=player,
                    )
                )
                return

        for player in [self.scene.left_player, self.scene.right_player]:
            if self.rect.colliderect(player.rect):
                self.player_rebound(player)

        if self.rect.collidelist([self.scene.upper_border, self.scene.lower_border]) != -1:
            self.velocity.y *= -1

            if self.rect.top < self.scene.upper_border.bottom:
                self.rect.top = self.scene.upper_border.bottom + 1
            elif self.rect.bottom > self.scene.lower_border.top:
                self.rect.bottom = self.scene.lower_border.top - 1

            self.position = glm.vec2(self.rect.center)

    def player_rebound(self, player: 'Player'):
        hit_y = (self.rect.centery - player.rect.centery) / (player.rect.height / 2)
        hit_y = max(-1.0, min(1.0, hit_y))

        max_angle = glm.radians(45)
        angle = hit_y * max_angle

        angle += glm.radians(randrange(-10, 10))

        if player == self.scene.left_player:
            new_velocity = glm.vec2(glm.cos(angle), glm.sin(angle))
        else:
            new_velocity = glm.vec2(-glm.cos(angle), glm.sin(angle))

        self.velocity = new_velocity

        if player == self.scene.left_player:
            self.rect.left = player.rect.right + 1
        else:
            self.rect.right = player.rect.left - 1

        self.position = glm.vec2(self.rect.center)


class Player(SceneObject):
    size_x: int = 14
    size_y = 200
    speed_factor = 200
    controls: tuple[int, int] = (0, 0)

    goal_rect: EngineLite.Rect

    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app, scene)

        self.counter = 0

    def events(self, event_list: list[EngineLite.event.Event]):
        for event in event_list:
            if event.type == EngineLite.KEYDOWN:
                if event.key == EngineLite.K_RETURN:
                    self.is_moving = True
                    self.reset_position()
            elif event.type == Scene.goal_event_type:
                self.is_moving = False

    def update(self):
        self.velocity.y = 0

        if self.app.key_list[self.controls[0]]:
            self.velocity.y -= 1
        if self.app.key_list[self.controls[1]]:
            self.velocity.y += 1

        if not self.is_moving:
            return

        dxy = self.velocity * self.app.delta_time
        self.position += dxy * self.speed_factor
        self.rect.center = self.position

        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.centery
        elif self.rect.bottom > self.app.config.height:
            self.rect.bottom = self.app.config.height
            self.position.y = self.rect.centery

    @property
    @abstractmethod
    def opponent(self) -> 'Player':
        pass

    @staticmethod
    def type_from_side(side: str):
        match side:
            case "left":
                return LeftPlayer
            case "right":
                return RightPlayer
        return None


class LeftPlayer(Player):
    controls = (EngineLite.K_w, EngineLite.K_s)

    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app, scene)

        self.goal_rect = EngineLite.Rect(
            -Scene.collide_rect_sizes, - Scene.collide_rect_sizes,
            Scene.collide_rect_sizes, EngineLite.App.config.height + Scene.collide_rect_sizes * 2
        )

    @property
    def init_pos(self) -> tuple[float, float]:
        return self.app.config.width / 10 * 1, self.app.config.height / 2

    @property
    def opponent(self) -> Player:
        return self.scene.right_player


class RightPlayer(Player):
    controls = (EngineLite.K_UP, EngineLite.K_DOWN)

    def __init__(self, app: EngineLite.App, scene: Scene):
        super().__init__(app, scene)

        self.goal_rect = EngineLite.Rect(
            EngineLite.App.config.width, - Scene.collide_rect_sizes,
            Scene.collide_rect_sizes, EngineLite.App.config.height + Scene.collide_rect_sizes * 2
        )

    @property
    def init_pos(self) -> tuple[float, float]:
        return self.app.config.width / 10 * 9, self.app.config.height / 2

    @property
    def opponent(self) -> Player:
        return self.scene.left_player
