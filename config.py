import configparser
import os


class Config:
    def __init__(self):
        self.app_path = os.getcwd()
        self.app_name = "People Counter"
        self.app_version = "Alpha 1.0"
        self.config = configparser.ConfigParser()  # создаём объекта парсера
        self.conf = os.path.join(self.app_path, 'src', 'data', 'config.ini')

    def get(self, args: str):
        self.config.read(self.conf)  # читаем конфиг

        rotation = str(self.config["VIDEO"]["rotation"])
        resize = str(self.config["VIDEO"]["resize"])

        line_down_color = eval(self.config["LINES"]["line_down_color"])
        line_up_color = eval(self.config["LINES"]["line_up_color"])
        lines_pos = eval(self.config["LINES"]["lines_pos"])

        rectangle_color = eval(self.config["OBJECT"]["rectangle_color"])
        rectangle_thickness = int(self.config["OBJECT"]["rectangle_thickness"])

        if args == "rotation":  # in python 3.10 will be updated to switch case
            args = int(rotation)
        elif args == "resize":
            args = float(resize)
        elif args == "line_down_color":
            # tuple BGR
            args = line_down_color
        elif args == "line_up_color":
            # tuple BGR
            args = line_up_color
        elif args == "lines_pos":
            # tuple h, w
            args = lines_pos
        elif args == "rectangle_color":
            # tuple BGR
            args = rectangle_color
        elif args == "rectangle_thickness":
            args = rectangle_thickness
        else:
            args = False

        return args

    def _tmp_set(self, arg1: str, arg2: str, arg3):
        self.config.read(self.conf)
        self.config.set(arg1, arg2, str(arg3))
        self.config.write(open(self.conf, "w"))

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
