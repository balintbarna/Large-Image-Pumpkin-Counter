#!/usr/bin/python3
"""
    Program for dividing an image into tiles. Exposes a class
    that handles the division.

    Author:     frnyb
    Date:       20200306
"""

###############################################################
# Imports

import cv2
import numpy as np

inf = float('inf')

###############################################################
# Classes

class ImageDivisor:
    def __init__(
        self,
        img,
        x_desired=2000,
        y_desired=2000
    ):
        self.img = img

        self.x, self.y = self.find_division(
            img,
            x_desired,
            y_desired
        )

    def find_division(
        self,
        img,
        x_desired=2000,
        y_desired=2000
    ):
        img_shape = self.img.shape

        best_x = x_desired
        lowest_remainder_x = inf

        for x in range(int(x_desired * 0.5), int(x_desired * 2)):
            if img_shape[0] / x < 1:
                break
            remainder = (img_shape[0] / x) - int(img_shape[0] / x)
            if remainder < lowest_remainder_x:
                lowest_remainder_x = remainder
                best_x = x

        best_y = y_desired
        lowest_remainder_y = inf

        for y in range(int(y_desired * 0.5), int(y_desired * 2)):
            if img_shape[1] / y < 1:
                break
            remainder = (img_shape[1] / y) - int(img_shape[1] / y)
            if remainder < lowest_remainder_y:
                lowest_remainder_y = remainder
                best_y = y

        return x, y

    def n_tiles(self):
        img_shape = self.img.shape
        n_tiles_x = img_shape[0] / self.x

        if (n_tiles_x - int(n_tiles_x) < 0.5):
            n_tiles_x = int(n_tiles_x)
        else:
            n_tiles_x = int(n_tiles_x) + 1

        n_tiles_y = img_shape[1] / self.y

        if (n_tiles_y - int(n_tiles_y) < 0.5):
            n_tiles_y = int(n_tiles_y)
        else:
            n_tiles_y = int(n_tiles_y) + 1

        return n_tiles_x, n_tiles_y

    def index_to_slice(
        self,
        index
    ):
        img_shape = self.img.shape
        n_tiles_x, n_tiles_y = self.n_tiles()

        if (n_tiles_x * n_tiles_y <= index):
            raise IndexError("tile index out of range")

        x_start = (index % n_tiles_x) * self.x
        x_end = x_start + self.x
        if (index % n_tiles_x) == n_tiles_x - 1:
            x_end = img_shape[0]

        y_start = int(index / n_tiles_y) * self.y
        y_end = y_start + self.y
        if int(index / n_tiles_y) == n_tiles_y - 1:
            y_end = img_shape[1]

        return x_start, x_end, y_start, y_end

    def length(self):
        n_tiles_x, n_tiles_y = self.n_tiles()
        return n_tiles_x * n_tiles_y

    def __getitem__(
        self,
        index
    ):
        x_start, x_end, y_start, y_end = self.index_to_slice(index)

        if len(self.img.shape) == 2:
            return self.img[x_start:x_end, y_start:y_end]
        else:
            return self.img[x_start:x_end, y_start:y_end, :]

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if (self.iter_index < self.length()):
            tile = self[self.iter_index]
            self.iter_index += 1
            return tile
        else:
            raise StopIteration
        

if __name__ == '__main__':
    img = cv2.imread("DJI_0283.JPG")

    div = ImageDivisor(img, 500, 500)

    for tile in div:
        cv2.imshow("img", tile)
        cv2.waitKey()
