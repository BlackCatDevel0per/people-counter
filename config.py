import configparser
import os


class Config:
    def __init__(self):
        self.app_path = os.getcwd()
        self.app_name = "People Counter"
        self.app_version = "Alpha 1.0"
        self.config = configparser.ConfigParser()  # создаём объекта парсера
        self.settings = os.path.join(self.app_path, 'src', 'data', 'settings.ini')
        self.PostgreSQL_File = os.path.join(self.app_path, 'src', 'data', 'PostgreSQL.ini')

    def get(self, args: str):
        #############
        self.config.read(self.settings)  # читаем конфиг
        data = None

        rotation = int(self.config["VIDEO"]["rotation"])
        resize = float(self.config["VIDEO"]["resize"])

        line_down_color = eval(self.config["LINES"]["line_down_color"])
        line_down_bcolor = eval(self.config["LINES"]["line_down_bcolor"])
        line_up_color = eval(self.config["LINES"]["line_up_color"])
        line_up_bcolor = eval(self.config["LINES"]["line_up_bcolor"])
        lines_pos = eval(self.config["LINES"]["lines_pos"])

        rectangle_color = eval(self.config["OBJECT"]["rectangle_color"])
        rectangle_thickness = int(self.config["OBJECT"]["rectangle_thickness"])
        obj_number_font_size = float(self.config["OBJECT"]["obj_number_font_size"])

        data = eval(args) # Return result like a dictonary

        return data

    def _tmp_set(self, arg1: str, arg2: str, arg3):
        self.config.read(self.settings)
        self.config.set(arg1, arg2, str(arg3))
        with open(self.settings, "r") as conf_file:
            self.config.write(open(self.settings, "w"))

    def set_VideoRotation(self, degree: int):
        self._tmp_set("VIDEO", "rotation", str(degree))


    def set_VideoResize(self, resize: float):
        self._tmp_set("VIDEO", "resize", str(resize))

    def set_LineDownColor(self, color_bgr: tuple):
        self._tmp_set("LINES", "line_down_color", str(color_bgr))

    def set_LineUpColor(self, color_bgr: tuple):
        self._tmp_set("LINES", "line_up_color", str(color_bgr))

    def set_LineUpColor(self, thickness: int):
        self._tmp_set("LINES", "rectangle_thickness", str(thickness))

    def PostgreSQL(self, type: str):
        self.self.config.read(self.PostgreSQL_File)
        data = None

        host = str(self.PostgreSQL_File["PSQL"]["host"])
        port = str(self.PostgreSQL_File["PSQL"]["port"])

        login = str(self.PostgreSQL_File["PSQL"]["login"])
        password = str(self.PostgreSQL_File["PSQL"]["password"])