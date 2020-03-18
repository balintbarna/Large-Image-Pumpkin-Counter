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

import rasterio

###############################################################
# Classes

class ImageDivisor:
    def __init__(
        self,
        img_filename,
        x_desired=2000,
        y_desired=2000
    ):
        self.set_image(img_filename)

        self.x, self.y = self.find_division(
            x_desired,
            y_desired
        )

    def find_division(
        self,
        x_desired=2000,
        y_desired=2000
    ):
        best_x = x_desired
        lowest_remainder_x = inf

        for x in range(int(x_desired * 0.5), int(x_desired * 2)):
            if self.img_shape[0] / x < 1:
                break
            remainder = (self.img_shape[0] / x) - int(self.img_shape[0] / x)
            if remainder < lowest_remainder_x:
                lowest_remainder_x = remainder
                best_x = x

        best_y = y_desired
        lowest_remainder_y = inf

        for y in range(int(y_desired * 0.5), int(y_desired * 2)):
            if self.img_shape[1] / y < 1:
                break
            remainder = (self.img_shape[1] / y) - int(self.img_shape[1] / y)
            if remainder < lowest_remainder_y:
                lowest_remainder_y = remainder
                best_y = y

        return best_x, best_y

    def n_tiles(self):
        n_tiles_x = self.img_shape[0] / self.x

        if (n_tiles_x - int(n_tiles_x) < 0.5):
            n_tiles_x = int(n_tiles_x)
        else:
            n_tiles_x = int(n_tiles_x) + 1

        n_tiles_y = self.img_shape[1] / self.y

        if (n_tiles_y - int(n_tiles_y) < 0.5):
            n_tiles_y = int(n_tiles_y)
        else:
            n_tiles_y = int(n_tiles_y) + 1

        return n_tiles_x, n_tiles_y

    def index_to_slice(
        self,
        index
    ):
        n_tiles_x, n_tiles_y = self.n_tiles()

        if (n_tiles_x * n_tiles_y <= index):
            raise IndexError("Tile index out of range")

        x_start = (index % n_tiles_x) * self.x
        x_end = x_start + self.x
        if (index % n_tiles_x) == n_tiles_x - 1:
            x_end = self.img_shape[0]

        y_start = int(index / n_tiles_x) * self.y
        y_end = y_start + self.y
        if int(index / n_tiles_y) == n_tiles_y - 1:
            y_end = self.img_shape[1]

        return x_start, x_end, y_start, y_end

    def length(self):
        n_tiles_x, n_tiles_y = self.n_tiles()
        return n_tiles_x * n_tiles_y

    def free_image(self):
        self.img = None

    def set_image(
            self,
            img_filename
    ):
        #self.img = rasterio.open(img_filename)
        self.img = cv2.imread(img_filename)
        #self.img_shape = (self.img.height, self.img.width, 3)
        self.img_shape = self.img.shape

    def __getitem__(
        self,
        index
    ):
        x_start, x_end, y_start, y_end = self.index_to_slice(index)
        #print(x_start, x_end, y_start, y_end)
        #input()

        #return np.transpose(self.img.read(window=((x_start, x_end), (y_start, y_end))))
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
