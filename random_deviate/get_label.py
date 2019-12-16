# -*- coding: utf-8 -*-
# @Time    : 2019-11-15 19:19
# @Author  : RichardoMu
# @File    : get_label.py
# @Software: PyCharm
import os


def readFile(folder_name,file_name):
    # print(folder_name)
    filePath = folder_name + '\\label\\' + file_name + '_label.txt'
    # print(filePath)
    match_loc_info = {}
    # include  '-'
    score_note_str = []
    det_note_str = []
    # not include '-'
    score_note = []
    det_note = []
    # padding zero and delete score location
    padding_zero_loc = []
    delte_loc = []
    i = 0
    # get score_note det_note
    with open(filePath,'r') as f:
        for line in f.readlines():
            data = ''.join(line).strip('\n').split('\t')

            if data[0] != '-':
                score_note_str.append(round(float(data[0])))
                score_note.append(round(float(data[0])))
            else:
                score_note_str.append(data[0])
            if data[1] != '-':
                det_note_str.append(round(float(data[1])))
                det_note.append(round(float(data[1])))
            else:
                det_note_str.append(data[1])
    # print(det_note_str[3]=='-')

    for i in range(len(score_note_str)):
        if score_note_str[i] != '-' and det_note_str[i] != '-':
            loc_det = det_note.index(det_note_str[i])
            loc_score = score_note.index(score_note_str[i])
            det_note[loc_det] = -1
            score_note[loc_score] = -1
            match_loc_info[loc_det] = loc_score
        elif score_note_str[i] != '-' and det_note_str[i] == '-':
            loc_score = score_note.index(score_note_str[i])
            score_note[loc_score] = -1
            padding_zero_loc.append(loc_score)
        elif score_note_str[i] == '-' and det_note_str[i] != '-':
            loc_det = det_note.index(det_note_str[i])
            det_note[loc_det] = -1
            delte_loc.append(loc_det)
    values = match_loc_info.values()
    for i in range(len(score_note)):
        if (i not in values) and (i not in padding_zero_loc):
            padding_zero_loc.append(i)
    for zero_loc in padding_zero_loc:
        match_loc_info[10000-zero_loc] = zero_loc
    match_loc_info = sorted(match_loc_info.items(),key = lambda x:x[1])
    # print(match_loc_info)
    # data like this
    # [(0, 0), (1, 1), (2, 2), (9997, 3), (3, 4), (4, 5), (5, 6), (9993, 7), (9992, 8), (6, 9),
    # (7, 10), (8, 11), (9, 12), (10, 13), (11, 14), (12, 15), (13, 16), (14, 17), (9982, 18),
    # (15, 19), (16, 20), (17, 21), (9978, 22), (18, 23), (19, 24), (20, 25), (21, 26), (22, 27),
    # (23, 28), (24, 29), (25, 30), (26, 31), (27, 32), (28, 33), (29, 34), (30, 35), (31, 36),
    # (32, 37), (33, 38), (34, 39), (35, 40), (9959, 41), (36, 42), (37, 43), (38, 44), (39, 45),
    # (9954, 46), (9953, 47), (9952, 48), (40, 49), (9950, 50), (41, 51), (42, 52), (43, 53), (44, 54),
    # (45, 55), (46, 56), (47, 57), (48, 58), (49, 59), (50, 60), (51, 61), (52, 62), (53, 63), (54, 64),
    # (55, 65), (56, 66), (57, 67), (58, 68), (59, 69), (60, 70)]
    return match_loc_info


def get_label(folder_name,file_name):
    match_loc_info_label = readFile(folder_name,file_name)
    # print(match_loc_info_label)
    return match_loc_info_label


def main():
    get_label("1")


if __name__ == '__main__':
    main()