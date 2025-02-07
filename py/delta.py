#! /usr/bin/python
import sys
import math as m
import numpy as np
import os

def load_pcd(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 6)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    return cloud

def distance(one, two):
    return m.sqrt(m.pow(one[0]-two[0],2) + m.pow(one[1]-two[1],2) + m.pow(one[2]-two[2],2))

def calculate_delta(input_1, input_2):
    if not (os.path.exists(input_1) and os.path.exists(input_2)):
        print("file not found")
    else:
        cloud_arr_1 = load_pcd(input_1)
        cloud_arr_2 = load_pcd(input_2)
        delta_arr = np.empty(shape=len(cloud_arr_2), dtype=float, order='C')
        for i in range(0, len(cloud_arr_2)):
            min_dist = distance(cloud_arr_2[i], cloud_arr_1[0])
            for j in range(0, len(cloud_arr_1)):
                dist = distance(cloud_arr_2[i], cloud_arr_1[j])
                if (dist < min_dist):
                    min_dist = dist
            delta_arr[i] = min_dist
        delta = np.sum(delta_arr) / len(delta_arr)
        median = np.median(delta_arr)
        haus = np.max(delta_arr)
        res =   '/' + str(round(delta, 6)) + '/' + str(round(median, 6)) + '/' + str(round(haus,6))
        return res


if __name__ == "__main__":
    calculate_delta(sys.argv[1], sys.argv[2])