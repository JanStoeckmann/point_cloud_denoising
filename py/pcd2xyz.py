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
            point = (line[0:-1]).split(" ", 6)
            cloud.append([float(point[4]), float(point[5]), float(point[6]), float(point[0]), float(point[1]), float(point[2])])
    return cloud

def convert_pcd_to_xyz(input):
    output = input[0:-4] + ".xyz"
    if not os.path.exists(input):
        print("input file not found")
    else:
        cloud = load_pcd(input)
        f = open(output, "w")
        f.write("# " + output + "\n")
        f.write("# " + str(len(cloud)) + " points\n")
        for i in range(0, len(cloud)):
            line = ""
            for j in range(0, 6):
                line += str(cloud[i][j]) + " "
            line += "\n"
            f.write(line)
        f.close()
        print(output + " created")

if __name__ == "__main__":
    convert_pcd_to_xyz(sys.argv[1])