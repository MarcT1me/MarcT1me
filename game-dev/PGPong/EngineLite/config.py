import json


class Config:
    IS_RELEASE = True

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
    width = 1024
    height = 640
    res_center = width / 2, height / 2
    fps = 0

    def __init__(self):
        settings_data = self.load_config("settings.json")

        self.width = settings_data.get("WIDTH", self.width)
        self.height = settings_data.get("HEIGHT", self.height)
        self.res_center = self.width / 2, self.height / 2
        self.fps = settings_data.get("FPS", self.fps)
