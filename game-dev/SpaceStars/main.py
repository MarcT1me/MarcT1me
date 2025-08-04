import math
import json
import random
import time
import pygame as pg


class Config:
    @staticmethod
    def load_config(config_path):
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {config_path} не найден.")
            return {}
        except json.JSONDecodeError:
            print(f"Ошибка в формате JSON файла {config_path}.")
            return {}


class AppConfig(Config):
    width = 1600
    height = 900
    res_center = width / 2, height / 2
    fps = 0
    alpha = 33

    def __init__(self):
        settings_data = self.load_config("settings.json")

        self.width = settings_data.get("WIDTH", self.width)
        self.height = settings_data.get("HEIGHT", self.height)
        self.res_center = self.width / 2, self.height / 2
        self.fps = settings_data.get("FPS", self.fps)
        self.alpha = settings_data.get("ALPHA", self.alpha)


class StarConfig(Config):
    index_reload = 1
    vel_min = 0.001
    vel_max = 0.01
    colors = [
        {"chance": 0.9, "color": "blue"},
        {"chance": 0.4, "color": "cyan"},
        {"chance": 0.0, "color": "red"}
    ]
    # x, y - на дистанции в DISTANCE_Z буду генерироваться звезды в радиусе MAX_RANGE
    max_range = 35
    distance_z = 50
    stars_count = 1000

    params_data: dict = None

    def __init__(self):
        self.check_scene()

        params_data = StarConfig.params_data[StarConfig.index_reload]

        self.colors = params_data.get("COLORS", self.colors)
        self.vel_min = params_data.get("VEL_MIN", self.vel_min)
        self.vel_max = params_data.get("VEL_MAX", self.vel_max)
        self.max_range = params_data.get("MAX_RANGE", self.max_range)
        self.distance_z = params_data.get("DISTANCE_Z", self.distance_z)
        self.stars_count = params_data.get("STARS_COUNT", self.stars_count)

    @staticmethod
    def check_scene():
        StarConfig.params_data = Config.load_config("params.json")

        if StarConfig.index_reload > len(StarConfig.params_data) - 1:
            StarConfig.index_reload = len(StarConfig.params_data) - 1
            return False
        elif StarConfig.index_reload < 0:
            StarConfig.index_reload = 0
            return False
        else:
            return True


class Stars:
    star_config = None

    def __init__(self):
        Stars.star_config = StarConfig()
        self.star_list: list[Star] = []

        for star_index in range(Stars.star_config.stars_count):
            self.star_list.append(Star(Stars.get_random_positions()))

    @staticmethod
    def get_random_positions() -> pg.Vector3:
        # PI - 3.14
        # RADIAN - 57.29
        # 0 to 360
        angle = random.uniform(0, 2 * math.pi)  # get random float in range
        # 1080 to 37800
        radius = random.randrange(App.config.height,
                                  App.config.height * Stars.star_config.max_range)  # get random int in range
        # angle transform to coordinate
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        # return random position
        return pg.Vector3(x, y, Stars.star_config.distance_z)

    def update(self, delta_time: float):
        for star in self.star_list:
            star.update(delta_time)

    def render(self):
        self.star_list.sort(key=lambda star_key: star_key.position.z, reverse=True)
        for star in self.star_list:
            star.render()


class App:
    screen = None
    config = None
    alpha_surface = None
    stars: Stars  # C like shit

    def __init__(self):
        App.config = AppConfig()

        pg.init()
        self.running = True
        self.show_fps = False
        self.is_jumping = False
        self.show_jump_font = False
        self.delta_time = 0
        self.jump_time = 0
        self.jump_length = 3
        self.fps_time = 0

        App.screen = pg.display.set_mode([App.config.width, App.config.height])
        App.alpha_surface = pg.Surface([App.config.width, App.config.height])
        App.alpha_surface.set_alpha(App.config.alpha)
        self.clock = pg.time.Clock()

        self.font = pg.font.SysFont("Arial", 14)
        self.rnd_fps_font = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, "white")
        self.rnd_jump_font = self.font.render(f"Jumping...", True, "white")

    def create(self):
        self.stars = Stars()

    def run(self):
        self.create()

        while self.running:
            self.events()
            self.update(self.delta_time)
            self.render()

            pg.display.flip()
            self.delta_time = self.clock.tick(App.config.fps)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    StarConfig.index_reload += 1

                    if StarConfig.check_scene():
                        self.stars = Stars()
                if event.key == pg.K_DOWN:
                    StarConfig.index_reload -= 1

                    if StarConfig.check_scene():
                        self.stars = Stars()
                if event.key == pg.K_r:
                    self.stars = Stars()
                if event.key == pg.K_LEFT:
                    Star.speed_velocity /= 2
                if event.key == pg.K_RIGHT:
                    Star.speed_velocity *= 2
                if event.key == pg.K_j:
                    if 0 < time.time() - self.jump_time < self.jump_length + 2:
                        continue
                    self.show_jump_font = True
                    self.jump_time = time.time()
                if event.key == pg.K_f:
                    self.show_fps = not self.show_fps

    def update(self, delta_time: float):
        cur_jump_time = time.time() - self.jump_time

        # phase 1
        if 0 < cur_jump_time < 1:
            Star.speed_velocity = cur_jump_time * 10

        # phase 2 - jump
        if 0.95 < cur_jump_time < 1.05 and not self.is_jumping:
            StarConfig.index_reload = 0
            Star.speed_velocity = 6
            self.stars = Stars()
            self.is_jumping = True

        # phase 3 - jump is ending
        if self.jump_length + 1 < cur_jump_time < self.jump_length + 1.05 and self.is_jumping:
            StarConfig.index_reload = 1
            Star.speed_velocity = 10
            self.stars = Stars()
            self.is_jumping = False

        # phase 4
        if self.jump_length + 1.05 < cur_jump_time < self.jump_length + 1.95:
            factor = (cur_jump_time - self.jump_length) - 1
            Star.speed_velocity = 10 - factor * 10

        if self.jump_length + 1.95 < cur_jump_time < self.jump_length + 2.05:
            self.show_jump_font = False

        self.stars.update(delta_time)

    def render(self):
        self.screen.blit(App.alpha_surface, [0, 0])
        self.stars.render()

        if self.show_fps:
            if time.time() - self.fps_time > 1:
                self.rnd_fps_font = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, "white")
                self.fps_time = time.time()

            self.screen.blit(self.rnd_fps_font, [0, 0])

        if self.show_jump_font:
            self.screen.blit(self.rnd_jump_font, [0, App.config.height - self.rnd_jump_font.get_height()])


class Star:
    speed_velocity = 1

    def __init__(self, position: pg.Vector3):
        self.position: pg.Vector3 = position

        # скорость по направлению Z (в камеру)
        self.velocity_z: float = random.uniform(Stars.star_config.vel_min, Stars.star_config.vel_max)
        self.color: str = Star.get_rnd_color()

        # screen 2D, звезды 3D - позиция трехмерных звезд в 2D пространстве окна
        self.screen_position: pg.Vector2 = pg.Vector2()

        # размер звезды - меняется при ее движении относительно 2D пространства
        self.size: float = 10

    @staticmethod
    def get_rnd_color() -> str:
        rnd = random.random()
        for v in Stars.star_config.colors:
            if rnd > v["chance"]:
                return v["color"]

    def update(self, delta_time: float):
        self.position.z -= self.velocity_z * Star.speed_velocity * delta_time

        if self.position.z < 0:
            self.position = Stars.get_random_positions()

        self.screen_position = pg.Vector2(self.position.x, self.position.y) / self.position.z + pg.Vector2(
            App.config.res_center)
        self.size = ((Stars.star_config.distance_z - self.position.z) / (0.25 * self.position.z)) / 2

    def render(self):
        # pg.draw.rect(App.screen, self.color, (*self.screen_position, self.size, self.size))
        pg.draw.circle(App.screen, self.color, self.screen_position, self.size)


if __name__ == '__main__':
    app = App()
    app.run()
