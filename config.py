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
        data = None

        rotation = str(self.config["VIDEO"]["rotation"])
        resize = str(self.config["VIDEO"]["resize"])

        line_down_color = eval(self.config["LINES"]["line_down_color"])
        line_down_bcolor = eval(self.config["LINES"]["line_down_bcolor"])
        line_up_color = eval(self.config["LINES"]["line_up_color"])
        line_up_bcolor = eval(self.config["LINES"]["line_up_bcolor"])
        lines_pos = eval(self.config["LINES"]["lines_pos"])

        rectangle_color = eval(self.config["OBJECT"]["rectangle_color"])
        rectangle_thickness = int(self.config["OBJECT"]["rectangle_thickness"])
        obj_number_font_size = float(self.config["OBJECT"]["obj_number_font_size"])

        if args == "rotation":  # in python 3.10 will be updated to switch case
            data = int(rotation)
        elif args == "resize":
            data = float(resize)
        elif args == "line_down_color":
            # tuple BGR
            data = line_down_color
        elif args == "line_down_bcolor":
            # tuple BGR
            data = line_down_bcolor
        elif args == "line_up_color":
            # tuple BGR
            data = line_up_color
        elif args == "line_up_bcolor":
            # tuple BGR
            data = line_up_bcolor
        elif args == "lines_pos":
            # tuple h, w
            data = lines_pos
        elif args == "rectangle_color":
            # tuple BGR
            data = rectangle_color
        elif args == "rectangle_thickness":
            data = rectangle_thickness
        elif args == "obj_number_font_size":
            data = obj_number_font_size
        else:
            data = None

        return data

    def _tmp_set(self, arg1: str, arg2: str, arg3):
        self.config.read(self.conf)
        self.config.set(arg1, arg2, str(arg3))
        with open(self.conf, "r") as conf_file:
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
