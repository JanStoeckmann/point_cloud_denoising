#! /usr/bin/python
import sys
import numpy as np
import os

def load_pcd(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 2)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    return cloud

def cloud_size(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 2)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    cloud = load_pcd(input)
    return len(cloud)