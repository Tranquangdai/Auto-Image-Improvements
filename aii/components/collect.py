import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from aii.utils import array_to_PIL, crop_by_bbox, grab_contours, list_images


class PatchCollect():

    def __init__(self, patch_dir):
        self.patches = list(list_images(patch_dir))

    @staticmethod
    def resize_large_patch(patch, ratio=None):
        if ratio is None:
            ratio = max(patch.size) / 1e3 * np.random.uniform(1.2, 1.5)
        patch = patch.resize(
            (int(patch.size[0] / ratio), int(patch.size[1] / ratio)))
        return patch

    def sample_collect(self, k=15):
        return self.collect(random.choices(self.patches, k=k))

    def collect(self, path):
        result = []
        for p in path:
            patch = Image.open(p)
            result.append(self.resize(patch))
        return result

    def resize(self, patch):
        ptype = self.check_type(patch)

        max_size = max(patch.size)
        if max_size > 1e3:
            patch = self.resize_large_patch(patch)
        elif 2e2 < max_size < 2e3 and ptype == 'icon':
            patch = self.resize_large_patch(patch, np.random.uniform(1.2, 1.7))
        if ptype == 'banner':
            return (patch, 'banner')
        elif ptype == 'icon':
            return (patch, 'icon')

    @staticmethod
    def check_type(patch):
        w, h = patch.size
        if w > 3 * h:
            return 'banner'
        else:
            return 'icon'


class SignCollect():

    def __init__(self, sign_dir):
        self.signs = list(list_images(sign_dir))

    def sample_collect(self, k=3):
        return self.collect(random.choices(self.signs, k=k))

    def collect(self, path):
        result = []
        for p in path:
            patch = Image.open(p)
            w, h = patch.size
            ratio = np.random.uniform(0.4, 0.6)
            patch = patch.resize((int(w * ratio), int(h * ratio)))
            result.append(patch)
        return result


class ProductCollect:

    def __init__(self, product_dir):
        self.products = list(list_images(product_dir))

    def sample_collect(self):
        return self.collect(random.choices(self.products, k=1)[0])

    def collect(self, path):
        rect = self.extract_box_from_product_in_white_bg(path)
        arr = crop_by_bbox(plt.imread(path), rect)
        result = array_to_PIL(arr)
        max_size = max(result.size)
        if max_size > 5e2:
            ratio = np.random.uniform(1.5, 2.1)
            result = result.resize(
                (int(result.size[0] / ratio), int(result.size[1] / ratio)))
        return result

    def extract_box_from_product_in_white_bg(self, path):
        image = plt.imread(path)  # path = path to your file
        bin = cv2.inRange(image, (255, 255, 255), (255, 255, 255))
        cv2.bitwise_not(bin, bin)
        cnts = cv2.findContours(
            bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        rect = cv2.boundingRect(cnts[0])
        return rect
