#! /usr/bin/python
import sys
import numpy as np
import os

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

def load_xyz(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 2)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    return cloud

def convert_xyz_to_pcd(input):
    output = input[0:-4] + ".pcd"
    if not os.path.exists(input):
        print("input file not found")
    else:
        cloud = load_xyz(input)
        save_pcd(output, cloud)

if __name__ == "__main__":
    convert_xyz_to_pcd(sys.argv[1])