#!/usr/bin/python3
"""
    Program for counting pumpkins in a orthomosaic.
    Utilizes the following scripts:
        pumpkin_counter_single_img.py   For counting 
                                        pumpkins in a 
                                        single tile

        image_divisor.py                For dividing a
                                        orthomosaic into
                                        tiles

    Author:     frnyb
    Date:       20200312
"""

###############################################################
# Imports

import cv2
import numpy as np

import sys
import argparse
from tqdm import tqdm

from math import sqrt

from config_loader import load_config

from pumpkin_counter_single_img import PumpkinCounter
from image_divisor import ImageDivisor

###############################################################
# Classes

class PumpkinCounterOrthomosaic:
    def __init__(
            self,
            orthomosaic_path=None,
            silent=False
    ):
        self.silent = silent
        self.config = load_config()
        
        if (orthomosaic_path == None):
            self.orthomosaic_path = self.config['orthomosaic_filename']
        else:
            self.orthomosaic_path = orthomosaic_path

    def count_pumpkins(
            self,
            marked_images_dir=None,
            tiles_dir=None
    ):
        if not self.silent:
            print('Dividing orthomosaic into tiles.')
        div = ImageDivisor(
                self.orthomosaic_path,
                self.config['tile_height'],
                self.config['tile_width']
            )

        if not self.silent:
            print("Divided orthomosaic into %i tiles."%div.length())
        
        self.counted_pumpkins_data = [] 

        if not self.silent:
            print("Counting pumpkins in each tile.")
        for index, tile in tqdm(
                enumerate(div),
                disable=self.silent
        ):
            img_filename = None
            if marked_images_dir != None:
                img_filename = output_img_dir + "marked_pumpkins_" + str(index) + ".png"
                
            tile_filename = None
            if tiles_dir != None:
                tile_filename = tiles_dir + "tile_" + str(index) + ".png"
                cv2.imwrite(
                        tile_filename,
                        tile
                )

            self.counted_pumpkins_data.append(
                self._count_pumpkins_tile(
                    tile,
                    index,
                    img_filename
                )
            )
    
        div.free_image()

        self.counted_pumpkins_data, total_count = self._sort_counted_pumpkins_data(
                self.counted_pumpkins_data,
                div
                )

        return total_count

    def _count_pumpkins_tile(
            self,
            tile,
            index,
            marked_img_filename=None
    ):
        cnt_pmk_data = {}

        pc = PumpkinCounter(
                img=tile,
                silent=self.silent
            )

        cnt_pmk_data['count'] = pc.count_pumpkins_fast(marked_img_filename)

        cnt_pmk_data['bordering_coordinates'] = pc.get_bordering_pumpkins_coordinates()

        cnt_pmk_data['index'] = index

        return cnt_pmk_data

    def _sort_counted_pumpkins_data(
            self,
            counted_pumpkins_data,
            divisor
    ):
        for i, pmk_data_i in enumerate(counted_pumpkins_data):
            for j, pmk_data_j in enumerate(
                    counted_pumpkins_data,
                    i + 1
            ):
                is_bordering, direction = self._is_bordering(
                        pmk_data_i,
                        pmk_data_j,
                        divisor
                        )

                if is_bordering:
                    counted_pumpkins_data[i], counted_pumpkins_data[j] = self._reduce_counted_pumpkins(
                            counted_pumpkins_data[i], 
                            counted_pumpkins_data[j],
                            direction,
                            divisor
                            )

        total_count = 0

        for pmk in counted_pumpkins_data:
            total_count += pmk['count']

        return counted_pumpkins_data, total_count

    def _is_bordering(
            self,
            pmk_data_i,
            pmk_data_j,
            divisor
    ):
        x_start_i, x_end_i, y_start_i, y_end_i = divisor.index_to_slice(pmk_data_i['index'])
        x_start_j, x_end_j, y_start_j, y_end_j = divisor.index_to_slice(pmk_data_j['index'])

        if (x_start_j == (x_end_i + 1)):
            return True, '0'                # Tile i comes before tile j in the x direction
        elif (x_start_i == (x_end_j + 1)):
            return True, '-0'               # Tile j comes before tile i in the x direction
        elif (y_start_j == (y_end_i + 1)):
            return True, '1'                # Tile i comes before tile j in the y direction
        elif (y_start_i == (y_end_j + 1)):
            return True, '-1'               # Tile j comes before tile i in the y direction
        else:
            return False, None

    def _reduce_counted_pumpkins(
            self,
            cnt_pmk_data_i,
            cnt_pmk_data_j,
            direction,
            divisor
    ):
        bordering_coords_i = []
        bordering_coords_j = cnt_pmk_data_j['bordering_coordinates']

        for i, coord_i in enumerate(cnt_pmk_data_i['bordering_coordinates']):
            index_to_remove = None              # None for no duplicate, -1 for removing from list i, 
                                                # otherwise remove index from list j
            for j, coord_j in enumerate(
                    bordering_coords_j,
                    i + 1
            ):
                dist = self._cross_tile_distance(
                        cnt_pmk_data_i['index'],
                        cnt_pmk_data_j['index'],
                        coord_i,
                        coord_j,
                        direction,
                        divisor
                        )

                if dist < self.config['pumpkin_diameter']:
                    dist_to_border_i, dist_to_border_j = self._dist_to_border(
                            cnt_pmk_data_i['index'],
                            cnt_pmk_data_j['index'],
                            coord_i,
                            coord_j,
                            direction,
                            divisor
                            )

                    if dist_to_border_i > dist_to_border_j:
                        index_to_remove = j
                    else:
                        index_to_remove = -1

                    break

            if index_to_remove == -1:
                continue
            
            if index_to_remove != None:
                bordering_coords_j.pop(index_to_remove)

            bordering_coords_i.append(coord_i)

        cnt_pmk_data_i['count'] = cnt_pmk_data_i['count'] - (len(cnt_pmk_data_i['bordering_coordinates']) - len(bordering_coords_i))

        cnt_pmk_data_i['bordering_coordinates'] = bordering_coords_i;

        cnt_pmk_data_j['count'] = cnt_pmk_data_j['count'] - (len(cnt_pmk_data_j['bordering_coordinates']) - len(bordering_coords_j))

        cnt_pmk_data_j['bordering_coordinates'] = bordering_coords_j

        return cnt_pmk_data_i, cnt_pmk_data_j

    def _cross_tile_distance(
            tile_index_i,
            tile_index_j,
            coord_i,
            coord_j,
            direction,
            divisor
    ):
        x_start_i, x_end_i, y_start_i, y_end_i = divisor.index_to_slice(tile_index_i)
        x_start_j, x_end_j, y_start_j, y_end_j = divisor.index_to_slice(tile_index_j)

        size_x_i = x_end_i - x_start_i
        size_y_i = y_end_i - y_start_i
        size_x_j = x_end_j - x_start_j
        size_y_j = y_end_j - y_start_j

        if direction == '0':
            dist_x = size_x_i - coord_i[0] + coord_j[0]
            dist_y = abs(coord_i[1] - coord_j[1])
            
            return sqrt(dist_x**2 + dist_y**2)
        
        if direction == '-0':
            dist_x = size_x_j - coord_j[0] + coord_i[0]
            dist_y = abs(coord_i[1] - coord_j[1])

            return sqrt(dist_x**2 + dist_y**2)

        if direction == '1':
            dist_x = abs(coord_i[0] - coord_j[0])
            dist_y = size_y_i - coord_i[1] + coord_j[1]

            return sqrt(dist_x**2 + dist_y**2)

        if direction == '-1':
            dist_x = abs(coord_i[0] - coord_j[0])
            dist_y = size_y_j - coord_j[1] + coord_i[1]

            return sqrt(dist_x**2 + dist_y**2)

    def _dist_to_border(
            tile_index_i,
            tile_index_j,
            coord_i,
            coord_j,
            direction,
            divisor
    ):
        x_start_i, x_end_i, y_start_i, y_end_i = divisor.index_to_slice(tile_index_i)
        x_start_j, x_end_j, y_start_j, y_end_j = divisor.index_to_slice(tile_index_j)

        if direction == '0':
            return size_x_i - coord_i[0], coord_j[0]
        
        if direction == '-0':
            return coord_i[0], size_x_j - coord_j[0] 

        if direction == '1':
            return size_y_i - coord_i[1], coord_j[1]

        if direction == '-1':
            return coord_i[1], size_y_j - coord_j[1] 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Count pumpkins in an orthomosaic.")

    parser.add_argument(
        '-i',
        dest='i',
        action='store',
        help="The input orthomosaic path. If non given, a default path will be used."
    )
    parser.add_argument(
        '-o',
        dest='o',
        action='store',
        type=str,
        help="Marked images output directory. If specified, will save tiles with marked pumpkins in the specified directory."
    )
    parser.add_argument(
        '-t',
        dest='t',
        action='store',
        type=str,
        help='Tile output directory. If specified, will store ouput tiles without marked pumpkins here.'
    )
    parser.add_argument(
        '-s',
        dest='s',
        action='store_true',
        default=False,
        help="If specified, no progress bar will be shown."
    )

    args = parser.parse_args(sys.argv[1:])

    pc = PumpkinCounterOrthomosaic(
            orthomosaic_path=args.i,
            silent=args.s
    )

    n_pumpkins = pc.count_pumpkins(
            marked_images_dir=args.o,
            tiles_dir=args.t
    )
    
    if pc.silent:
        print(n_pumpkins)
    else:
        print("Counted pumpkins: %i"%n_pumpkins)
