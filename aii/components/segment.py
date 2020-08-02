import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
from imantics import Mask
from PIL import Image

from ..utils import grab_contours, list_images, move_polygons


class Segment:

    def __init__(self, product_dir):
        self.products = list(list_images(product_dir))

    def get_mask(self, image):
        '''
        See: https://www.pyimagesearch.com/2020/07/27/opencv-grabcut-foreground-segmentation-and-extraction/
        '''
        rect = self.extract_box_from_product_in_white_bg(image)

        mask = np.zeros(image.shape[:2], dtype="uint8")

        fgModel = np.zeros((1, 65), dtype="float")
        bgModel = np.zeros((1, 65), dtype="float")

        (mask, bgModel, fgModel) = cv2.grabCut(image, mask,
                                               rect, bgModel,
                                               fgModel,
                                               7,
                                               mode=cv2.GC_INIT_WITH_RECT)

        outputMask = np.where((mask == cv2.GC_BGD) |
                              (mask == cv2.GC_PR_BGD), 0, 1)
        outputMask = (outputMask * 255).astype("uint8")
        output = cv2.bitwise_and(image, image, mask=outputMask)
        return output, outputMask

    @staticmethod
    def extract_box_from_product_in_white_bg(image):
        '''
        See: https://stackoverflow.com/questions/57346239/finding-the-bounding-box-around-white-background-with-white-colour-product-in-py
        '''
        bin = cv2.inRange(image, (255, 255, 255), (255, 255, 255))
        cv2.bitwise_not(bin, bin)
        cnts = cv2.findContours(
            bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        rect = cv2.boundingRect(cnts[0])
        return rect

    @staticmethod
    def overlay_product_upon_bg(img1, img2, mask, step_x, step_y):
        '''
        See: https://docs.opencv.org/master/d0/d86/tutorial_py_image_arithmetics.html
        '''
        rows, cols, channels = img2.shape
        roi = img1[0:rows, 0:cols]

        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

        dst = cv2.add(img1_bg, img2_fg)
        img1[step_y:rows + step_y, step_x:cols + step_x] = dst

        polygons = Mask(mask).polygons()
        polygons = move_polygons(polygons, step_x, step_y)
        return img1, polygons

    def sample_collect(self, bg):
        img = polygons = None
        try:
            path = random.choices(self.products, k=1)[0]
            size = np.random.randint(600, 800)
            image = cv2.resize(plt.imread(path), (size, size))
            output, mask = self.get_mask(image)
            img, polygons = self.overlay_product_upon_bg(
                bg,
                output,
                mask,
                step_x=np.random.randint(0, 200),
                step_y=np.random.randint(0, 250))
        except Exception as e:
            print(e)
            pass
        return img, polygons
