# -*- coding: utf-8 -*-
# @Time    : 2019-11-20 10:39
# @Author  : RichardoMu
# @File    : main_auto.py
# @Software: PyCharm
from alignment import sw_alignment
import os
from get_label import get_label
from utils import readFile,load_data,evaluate,data_concat
from Create_datas_auto import create_data
import numpy as np
import csv
import random
from matplotlib import pyplot as plt
random.seed(1234)
np.random.seed(1234)

def main(delta,mul):
    # get created data folder path ensure deal with them next step
    folder_path,folder_name = create_data(delta,mul)
    root = os.getcwd()
    fileList = readFile(folder_path + '\\data')
    # 确定长度
    fileList_length = len(fileList)
    score_file_name = root + '\\308_score.txt'
    score_note = load_data(score_file_name)
    # 计算平均准确率
    accuracy_sw_sum = 0. # 相对
    accuracy_sw_absolute_sum = 0. # sw绝对
    for name in fileList:
        det_note = load_data(name)
        # use sw relative
        match_loc_info, _ = sw_alignment(score_note,det_note,flag="relative")
        # use sw absolute
        absolute_match_loc_info, _ = sw_alignment(score_note,det_note,flag="absolute")
        # save as csv
        file_name = name.replace(folder_path+"\\data\\","").replace('.txt','')
        match_loc_info_label = get_label(folder_path,file_name)
        # evaluate result of alignment about dtw and sw of absolute and relative
        # sw relative
        accuracy_sw = evaluate(match_loc_info,match_loc_info_label)
        accuracy_sw_sum += accuracy_sw
        # evalute sw absolute
        accuracy_sw_absolute = evaluate(absolute_match_loc_info,match_loc_info_label)
        accuracy_sw_absolute_sum += accuracy_sw_absolute
        data_concat(match_loc_info['loc_info'],absolute_match_loc_info['loc_info'],match_loc_info_label,root,folder_name,file_name)
    # evaluate accuracy of algorithm
    accuracy_sw_sum /= fileList_length
    accuracy_sw_absolute_sum /= fileList_length
    print("mean accuracy of relative sw :%f, absolute sw: %f"%(accuracy_sw_sum,accuracy_sw_absolute_sum))
    return accuracy_sw_sum,accuracy_sw_absolute_sum,folder_name

if __name__ == '__main__':
    #  n lack 缺音
    #  m deviate 成段跑音的段
    n = 11
    m = 101
    for i in range(n):
        accuracy_sw_array = np.array([])
        accuracy_sw_ab_array = np.array([])
        for j in range(m):
            accuracy_sw, accuracy_sw_ab, folder_name = main(delta=i, mul=j)
            accuracy_sw_array = np.append(accuracy_sw_array, accuracy_sw)
            accuracy_sw_ab_array = np.append(accuracy_sw_ab_array, accuracy_sw_ab)
        x = np.arange(m) * 0.01
        plt.figure()
        # sw 相对音高正确率曲线
        plt.plot(x, accuracy_sw_array, c='r', linestyle="--", marker='o', label='relative sw')
        # sw 绝对音高正确率曲线
        plt.plot(x, accuracy_sw_ab_array, c="b", linestyle="-", marker='>', label='absolute sw')
        plt.title(folder_name + '  accuracy')
        plt.xlabel('deviate number')
        plt.ylabel('accuracy')
        plt.legend()
        path = ".\\fig\\" + folder_name + ".tiff"
        plt.savefig(path, dpi=500)
        print("\n")
        with open(".\\csv_folder\\" + folder_name + ".csv", 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(len(accuracy_sw_array)):
                sw_array = accuracy_sw_array[i]
                sw_ab_array = accuracy_sw_ab_array[i]
                writer.writerow([float(sw_array), float(sw_ab_array)])
    # n = 0
    # m = 101
    # accuracy_sw_array = np.array([])
    # accuracy_sw_ab_array = np.array([])
    # for j in range(m):
    #     accuracy_sw , accuracy_sw_ab, folder_name = main(delta=n,mul=j)
    #     accuracy_sw_array = np.append(accuracy_sw_array,accuracy_sw)
    #     accuracy_sw_ab_array = np.append(accuracy_sw_ab_array,accuracy_sw_ab)
    # with open("deviate_random.csv",'w',newline='') as f:
    #     writer = csv.writer(f)
    #     for i in range(len(accuracy_sw_array)):
    #         sw_array = accuracy_sw_array[i]
    #         sw_ab_array = accuracy_sw_ab_array[i]
    #         writer.writerow([float(sw_array),float(sw_ab_array)])