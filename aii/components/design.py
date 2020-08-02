import json
import os
import uuid
from os.path import exists

import numpy as np
from PIL import Image
from tqdm import trange

from aii.utils import array_to_PIL

from .background import BackGround
from .collect import PatchCollect, SignCollect
from .segment import Segment


class Designer:

    def __init__(self, cfg):
        self.pac = PatchCollect(cfg['patch'])
        self.sc = SignCollect(cfg['sign'])
        self.lgc = SignCollect(cfg['logo'])
        self.pl = BackGround(cfg['background'])
        self.sg = Segment(cfg['product'])

        self._init_container()

    def _init_container(self):
        self.images = []
        self.annotations = []
        self.dataset = {
            'images': self.images,
            'categories': [
                {
                    "supercategory": "product",
                    "id": 1,
                    "name": "product"
                }
            ],
            'annotations': self.annotations,
        }

    @staticmethod
    def convert_xyxy_to_xywh(box):
        x_min, y_min, x_max, y_max = box
        return [x_min, y_min, x_max - x_min, y_max - y_min]

    def from_polygon(self, polygons):
        tmp = dict()
        tmp['segmentation'] = [(p.flatten() + 0.5).tolist()
                               for p in polygons.points]
        tmp['iscrowd'] = 0
        tmp['category_id'] = 1
        tmp['id'] = 1
        tmp['area'] = self.compute_area(polygons)
        tmp['bbox'] = self.convert_xyxy_to_xywh(
            [float(i) for i in polygons.bbox()])
        tmp['bbox_mode'] = 0
        return tmp

    def draw(self):
        try:
            self.pl.place_banner(self.pac.sample_collect())
            self.pl.place_sign(self.sc.sample_collect())
            self.pl.place_sign(self.lgc.sample_collect())

            bg = np.array(self.pl.bg)
            img, polygons = self.sg.sample_collect(bg)
            return img, polygons
        except:
            return None, None

    def generate(self, dirname, steps=10):
        if not exists(dirname):
            os.makedirs(dirname)
        counter = 0
        for _ in trange(steps):
            img, polygon = self.draw()
            if img is not None:
                polygon_info = self.from_polygon(polygon)
                image_info = self.gen_image_info(dirname)
                polygon_info['image_id'] = image_info['id']
                polygon_info['id'] = counter
                counter += 1
                array_to_PIL(img).convert('RGB').save(
                    '{}/{}'.format(dirname, image_info['file_name']))
                self.images.append(image_info)
                self.annotations.append(polygon_info)

    @staticmethod
    def gen_image_info(dirname):
        id_ = str(uuid.uuid4().int)[:20]
        path = '{}.jpg'.format(id_)
        return {
            'height': 1000,
            'width': 1000,
            'id': id_,
            'file_name': path,
        }

    def save(self, dirname):
        if not exists(dirname):
            os.makedirs(dirname)
        rand_id = str(uuid.uuid4().int)[:20]
        path = '{}/{}.jpg'.format(dirname, rand_id)
        self.pl.bg.convert('RGB').save(path)
        self.annot.append((path, [self.pl.bbox]))

    @staticmethod
    def compute_area(polygons):
        contour = np.array(polygons.points[0])
        x = contour[:, 0]
        y = contour[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) -
                            np.dot(y, np.roll(x, 1)))
        return area

    def dump_annotations(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f)
