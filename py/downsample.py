#! /usr/bin/python
import sys
import math as m
import numpy as np
import os
import random

cs = 0.01

def load_pcd(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 2)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    return cloud

def save_pcd(output, cloud):
    f = open(output, "w")
    f.write('# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH '+str(len(cloud))+'\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS '+str(len(cloud))+'\nDATA ascii\n')
    for i in range(0, len(cloud)):
        line = ""
        for j in range(0, 3):
            line += str(cloud[i][j]) + " "
        line += "\n"
        f.write(line)
    f.close()
    print(output + " created")

def vox(val, min):
    return int(m.ceil(abs(val - min) / cs)) - 1

def downsample(input, output, density):
    if not os.path.exists(input):
        print("input file not found")
    else:
        arr = load_pcd(input)
        x_max = arr[0][0]
        x_min = arr[0][0]
        y_max = arr[0][1]
        y_min = arr[0][1]
        z_max = arr[0][2]
        z_min = arr[0][2]
        for i in range(0, len(arr)):
            if arr[i][0] > x_max:
                x_max = arr[i][0]
            elif arr[i][0] < x_min:
                x_min = arr[i][0]
            if arr[i][1] > y_max:
                y_max = arr[i][1]
            elif arr[i][1] < y_min:
                y_min = arr[i][1]
            if arr[i][2] > z_max:
                z_max = arr[i][2]
            elif arr[i][2] < z_min:
                z_min = arr[i][2]
        output_list = []
        x_size = vox(x_max, x_min) + 1
        y_size = vox(y_max, y_min) + 1
        z_size = vox(z_max, z_min) + 1
        voxel_arr = []
        for i in range(0, x_size):
            voxel_arr.append([])
            for j in range(0, y_size):
                voxel_arr[i].append([])
                for k in range(0, z_size):
                    voxel_arr[i][j].append([])
        for i in range(0, len(arr)):
            voxel_arr[vox(arr[i][0], x_min)][vox(arr[i][1], y_min)][vox(arr[i][2], z_min)].append(arr[i])

        for i in range(0, x_size):
            for j in range(0, y_size):
                for k in range(0, z_size):
                    voxel_list = voxel_arr[i][j][k]
                    if voxel_list != 0:
                        if len(voxel_list) <= density:
                            output_list += voxel_list
                        else:
                            random.shuffle(voxel_list)
                            output_list += voxel_list[:density]
        save_pcd(output, output_list)


if __name__ == "__main__":
    downsample(sys.argv[1], sys.argv[2], int(sys.argv[3]))