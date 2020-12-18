#! /usr/bin/python
import sys
import numpy as np
import os
import math as m
import random

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

def vector(one, two):
    return two - one

def distance(one, two):
    return m.sqrt(m.pow(one[0]-two[0],2) + m.pow(one[1]-two[1],2) + m.pow(one[2]-two[2],2))

def add_real_noise(input, output, campoint, thickness):
    if not os.path.exists(input):
        print("input file not found")
    else:
        cloud = load_pcd(input)
        for i in range(0, len(cloud)):
            vector = cloud[i] - campoint
            scale_factor = 1 / m.sqrt(m.pow(vector[0],2) + m.pow(vector[1],2) + m.pow(vector[2],2))
            vector = vector * scale_factor * random.uniform(-1*thickness/2, thickness/2)
            cloud[i] = (cloud[i] + vector).round(5)
        save_pcd(output, cloud)

if __name__ == "__main__":
    add_real_noise(sys.argv[1], sys.argv[2], np.array([float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]), float(sys.argv[6]))