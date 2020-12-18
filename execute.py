#! /usr/bin/python
import os
import sys
import subprocess
from py import delta
import csv

gaus_values = ['0.0005','0.001','0.0015','0.002','0.0025','0.003'] #0.002
realistic_values = ['0.005','0.01','0.015','0.02','0.025','0.03'] #0.02
campoints = {'small' : '-0.06 -0.8 -0.038',
                 'medium' :'-0.1 -0.6 -0.95',
                 'big' : '-0.1 -0.6 -0.95'}
down_values = ['1']     #2
normal_radius = '0.05'
mls_radius = ['0.005','0.01','0.015','0.02','0.025','0.03','0.035']   #0.025
ear_radius = ['0.005','0.01','0.015','0.02','0.025','0.03']   #0.02
wlop_radius = ['0.05','0.1','0.15','0.2','0.25']   #0.16
blf_neighbors = ['5','8','10','12','15','20','30']  #10 bei down 2

evaluation_list =  []

def save_evaluation():
    with open('evaluation.csv', 'w', newline='') as csvfile:
        evaluation_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        evaluation_writer.writerow(
            ["Src", "File", "Noise", "Noise value", "Downsample", "Downsample Value", "Filer", "Filter radius",
             "Avg delta", "Median delta", "Hausdorff distance"])
        for ele in evaluation_list:
            evaluation_writer.writerow(ele)

def cloud_size(input):
    file1 = open(input, 'r')
    Lines = file1.readlines()
    cloud = []
    for line in Lines:
        if (line[0].isnumeric()) or (line[0] == "-"):
            point = (line[0:-1]).split(" ", 2)
            cloud.append([float(point[0]), float(point[1]), float(point[2])])
    return len(cloud)

def execute():
    data = os.listdir('data')
    for src_file in data:
        if src_file[-4:] == ".pcd":
            src = src_file[:-4]
            create_directory('data/' + src)
            create_directory('data/' + src + '/gaus_noise')

            for gaus_val in gaus_values:
                gaus_dir = 'data/' + src + '/gaus_noise/' + gaus_val
                create_directory(gaus_dir)
                gaus_file = src + '-gaus'
                gaus_command = 'pcl/pcl_add_gaussian_noise.exe ' + 'data/' + src_file + ' ' + gaus_dir + '/' + gaus_file + '.pcd -sd ' + gaus_val
                proc = subprocess.Popen(gaus_command, stdout=subprocess.PIPE, creationflags=0x08000000)
                proc.wait()
                downsample(src_file, gaus_dir, gaus_file)
            for realistic_val in realistic_values:
                realistic_dir = 'data/' + src + '/realistic_noise/' + realistic_val
                create_directory(realistic_dir)
                realistic_file = src + '-realistic'
                realistic_command = 'python py/realistic_noise.py ' + 'data/' + src_file + ' ' + realistic_dir + '/' + realistic_file + '.pcd ' + campoints[src] + ' ' + realistic_val
                proc = subprocess.Popen(realistic_command, stdout=subprocess.PIPE, creationflags=0x08000000)
                proc.wait()
                downsample(src_file, realistic_dir, realistic_file)

def downsample(src_file, dir, file):
    for down_val in down_values:
        down_dir = dir + '/downsample/' + down_val
        create_directory(down_dir)
        down_file = file + "-down"
        down_command = 'python py/downsample.py ' + dir + '/' + file + '.pcd ' + down_dir + '/' + down_file + '.pcd ' + down_val
        process = subprocess.Popen(down_command, stdout=subprocess.PIPE, creationflags=0x08000000)
        process.wait()
        normal_file = down_file + '-normal'
        normal_command = 'pcl/pcl_normal_estimation.exe ' + down_dir + '/' + down_file + '.pcd ' + down_dir + '/' + normal_file + '.pcd ' + '-radius ' + normal_radius
        process = subprocess.Popen(normal_command, stdout=subprocess.PIPE, creationflags=0x08000000)
        process.wait()
        ascii_file = normal_file + '-ascii'
        ascii_command = 'pcl/pcl_convert_pcd_ascii_binary.exe ' + down_dir + '/' + normal_file + '.pcd ' + down_dir + '/' + ascii_file + '.pcd 0'
        process = subprocess.Popen(ascii_command, stdout=subprocess.PIPE, creationflags=0x08000000)
        process.wait()
        convert_command = 'python py/pcd2xyz.py ' + down_dir + '/' + ascii_file + '.pcd'
        process = subprocess.Popen(convert_command, stdout=subprocess.PIPE, creationflags=0x08000000)
        process.wait()

        for mls_rad in mls_radius:
            mls_dir = down_dir + '/mls/' + mls_rad
            create_directory(mls_dir)
            mls_file = ascii_file + '-mls'
            mls_command = 'pcl_mls_smoothing.exe ' + down_dir + '/' + ascii_file + '.pcd ' + mls_dir + '/' + mls_file + '.pcd -radius ' + mls_rad + ' -sqr_gauss_param 0.01 -polynomial_order 3'
            process = subprocess.Popen(mls_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            mls_ascii_file = mls_file + '-ascii'
            mls_ascii_command = 'pcl/pcl_convert_pcd_ascii_binary.exe ' + mls_dir + '/' + mls_file + '.pcd ' + mls_dir + '/' + mls_ascii_file + '.pcd 0'
            process = subprocess.Popen(mls_ascii_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            evaluation = mls_dir + delta.calculate_delta('data/' + src_file, mls_dir + '/' + mls_ascii_file + '.pcd')
            evaluation_list.append(evaluation.replace(".", ",").split("/"))
            save_evaluation()
        
        for blf_near in blf_neighbors:
            blf_dir = down_dir + '/blf/' + blf_near
            create_directory(blf_dir)
            blf_file = ascii_file + '-blf'
            blf_command = 'cgal/bilateral_smooth_point_set_example.exe ' + down_dir + '/' + ascii_file + '.xyz ' + blf_dir + '/' + blf_file + '.xyz '+ blf_near
            process = subprocess.Popen(blf_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            convert_command = 'python py/xyz2pcd_blf.py ' + blf_dir + '/' + blf_file + '.xyz'
            process = subprocess.Popen(convert_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            evaluation =  blf_dir + delta.calculate_delta('data/' + src_file, blf_dir + '/' + blf_file + '.pcd')
            evaluation_list.append(evaluation.replace(".", ",").split("/"))
            save_evaluation()

        for ear_rad in ear_radius:
            ear_dir = down_dir + '/ear/' + ear_rad
            create_directory(ear_dir)
            ear_file = ascii_file + '-ear'
            ear_command = 'cgal/edge_aware_upsample_point_set_example.exe ' + down_dir + '/' + ascii_file + '.xyz ' + ear_dir + '/' + ear_file + '.xyz '+ ear_rad
            process = subprocess.Popen(ear_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            convert_command = 'python py/xyz2pcd_ear.py ' + ear_dir + '/' + ear_file + '.xyz'
            process = subprocess.Popen(convert_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            evaluation =  ear_dir + delta.calculate_delta('data/' + src_file, ear_dir + '/' + ear_file + '.pcd')
            evaluation_list.append(evaluation.replace(".", ",").split("/"))
            save_evaluation()

        for wlop_rad in wlop_radius:
            wlop_dir = down_dir + '/wlop/' + wlop_rad
            create_directory(wlop_dir)
            wlop_file = ascii_file + '-wlop'
            wlop_command = 'cgal/wlop_simplify_and_regularize_point_set_example.exe ' + down_dir + '/' + ascii_file + '.xyz ' + wlop_dir + '/' + wlop_file + '.xyz ' + wlop_rad + ' 100'
            process = subprocess.Popen(wlop_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            convert_command = 'python py/xyz2pcd_wlop.py ' + wlop_dir + '/' + wlop_file + '.xyz'
            process = subprocess.Popen(convert_command, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            evaluation = wlop_dir + delta.calculate_delta('data/' + src_file, wlop_dir + '/' + wlop_file + '.pcd')
            evaluation_list.append(evaluation.replace(".", ",").split("/"))
            save_evaluation()




def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    execute()