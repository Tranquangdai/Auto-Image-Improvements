import random

import numpy as np
from PIL import Image

from ..utils import array_to_PIL, list_images


class BackGround():

    def __init__(self, bg_dir):
        self.exist_bgs = list(list_images(bg_dir))

    def _init_background(self):
        white_bg = np.zeros([1000, 1000, 3], dtype=np.uint8)
        white_bg.fill(255)
        white_bg = array_to_PIL(white_bg)
        if random.random() > 0.4:
            self.bg = Image.open(random.choice(
                self.exist_bgs)).resize((1000, 1000))
        else:
            self.bg = white_bg

    def place_product(self, result):
        w, h = result.size
        x_min = np.random.randint(0, 900 - w)
        y_min = np.random.randint(150, 900 - h)
        x_max = x_min + w
        y_max = y_min + h
        self.bg.paste(result, (x_min, y_min))
        self.bbox = [x_min, y_min, x_max, y_max]

    def place_banner(self, result):
        self._init_background()
        self.classify(result)
        self._place_banner()
        self._place_icon()

    def place_sign(self, result):
        for res in result:
            self.bg.paste(res, (np.random.randint(200, 850),
                                np.random.randint(150, 900)))

    def _place_banner(self):
        if len(self.banner):
            self.banner = self.banner[:2]
            if len(self.banner) == 1:
                self.bg.paste(self.banner[0], (np.random.randint(
                    0, 20), np.random.randint(0, 20)))
            elif len(self.banner) == 2:
                if random.random() > 0.3:
                    self.bg.paste(self.banner[0], (np.random.randint(
                        0, 20), np.random.randint(0, 20)))
                if random.random() > 0.3:
                    self.bg.paste(
                        self.banner[1], self.banner_bottom(self.banner[1]))

    def _place_icon(self):
        for res in self.icon[:np.random.randint(1, 4)]:
            self.bg.paste(res, (np.random.randint(200, 750),
                                np.random.randint(150, 600)))

    def classify(self, result):
        self.banner = [i for i, j in result if j == 'banner']
        self.icon = [i for i, j in result if j == 'icon']

    @staticmethod
    def banner_bottom(banner):
        w, h = banner.size
        return (np.random.randint(0, 50), np.random.randint(970, 1000) - h)

    @staticmethod
    def banner_top():
        return (np.random.randint(0, 50), np.random.randint(0, 100))
