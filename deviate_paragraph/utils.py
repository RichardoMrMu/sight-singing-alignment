# -*- coding: utf-8 -*-
# @Time    : 2019-11-20 10:33
# @Author  : RichardoMu
# @File    : utils.py
# @Software: PyCharm
import os
import csv
import pandas as pd
import numpy as np




def readFile(root):
    fileList = []
    for name in os.listdir(root):
        fileList.append(os.path.join(root,name))
    return fileList


def load_data(fileName):
    note = []
    with open(fileName,'r') as f:
        for line in f.readlines():
            line = line.strip()
            # round and save as integer
            note.append(round(float(line)))
    return note


def save_data(match_loc_info,folder_name,file_name,root,style='sw'):
    if not os.path.exists(root+'\\ali_data\\' + folder_name):
        os.mkdir(root+'\\ali_data\\' + folder_name)
    file_name = root+'\\ali_data\\' + folder_name +"\\" + style+'_'+file_name+'.csv'
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['score_note_index',"det_note_index"])
        for data in match_loc_info['loc_info']:
            det_note = data[0]
            score_note = data[1]
            writer.writerow([score_note,det_note])
        # print("written into csv file",file_name)


def evaluate(match_loc_info,match_loc_info_label):
    loc_info = match_loc_info['loc_info']
    zero_loc = match_loc_info['zero_loc']
    correct_num = 0
    length_loc_info = len(loc_info)
    for i in range(length_loc_info):
        if i in zero_loc:
            if match_loc_info_label[i][0] > 7000:
                correct_num += 1
        elif loc_info[i] == match_loc_info_label[i]:
            correct_num += 1
    return (correct_num*1.0)/length_loc_info


def data_concat(sw_loc_info,sw_ab_loc_info,lable_loc_info,root,folder_name,file_name):
    if not os.path.exists(root + '\\ali_data\\' + folder_name):
        os.mkdir(root + '\\ali_data\\' + folder_name)
    file_name = root + '\\ali_data\\' + folder_name + "\\" + file_name + '.csv'
    with open(file_name,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["",'sw_score_note_index',"sw_det_note_index","","real_label_score_note_index","real_lable_det_note_index","", "absolute_sw_score_note_index","absolute_sw_det_note_index"])
        for i in range(len(lable_loc_info)):
            # # if sw_loc_info shorter than lable_loc-info
            # if i >= len(sw_loc_info):
            #     sw_loc_info.append(("", ""))
            writer.writerow(["",sw_loc_info[i][1],sw_loc_info[i][0],"",lable_loc_info[i][1],lable_loc_info[i][0],"",sw_ab_loc_info[i][1],sw_ab_loc_info[i][0]])


def get_opt(opt):
    n = len(opt[00])
    m = len(opt)
    # print(m,n)
    data_opt = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            data_opt[i][j] = opt[i][j].cost
    # print(data_opt)
    return data_opt


def save_opt(opt,root,folder_name,file_name,style):
    file_name = root + "\\ali_data\\" + folder_name + "\\" + style + "_" + file_name + ".csv"
    df = pd.DataFrame(opt,columns=[str(i) for i in range(len(opt[1]))])
    print(df)
