# -*- coding: utf-8 -*-
# @Time    : 2019-12-08 15:58
# @Author  : RichardoMu
# @File    : add_utils.py
# @Software: PyCharm

import numpy as np
import random
random.seed(1)
np.random.seed(1)

def add_util(off_key_length):
    # delta 为跑调的趋势 加或者减
    delta = np.random.choice([-1, 1], off_key_length)
    # 设置跑调的偏差值序列 长度为off_key_length
    off_key_diff = np.random.uniform(2.5, 5., off_key_length)
    return delta, off_key_diff


def add_diff2score(off_key_length, score_data, score_data_temp, arr_length,style='down'):
    if style == 'upper':
        if arr_length == 1:  # 跑调的长度为1
            # off_key_length_temp 为将要跑调序列的长度
            off_key_length_temp = arr_length
            # off_key_loc_temp 确定在哪里跑调 为1 时全序列跑调
            off_key_loc_temp = np.array([0]).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]
            delta, off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
        elif arr_length == 2:
            # off_key_length_temp 为将要跑调序列的长度
            off_key_length_temp = arr_length
            # off_key_loc_temp 暂时存放随机生成跑调位置的np.array 最后一位不能被抽到，因为2位，最后一位抽到会超出范围
            off_key_loc_temp = np.array([0,1]).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]
            delta, off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
        elif arr_length > 2:
            # 生成长度
            off_key_length_temp = random.sample(range(2,arr_length+1),1)[0]
            # off_key_loc_temp 暂时存放随机生成跑调位置的np.array 最后一位不能被抽到，因为2位，最后一位抽到会超出范围
            off_key_loc_temp = np.array(random.sample(range(0, arr_length - off_key_length_temp + 1), 1)).astype(int)
            # 因为off_key_length大于 2 将off_key_loc_temp[0] 的下n-1位也加入到temp中
            off_key_loc_temp = np.append(off_key_loc_temp,
                                         np.array([off_key_loc_temp[0]+i for i in range(1,off_key_length_temp)])
                                         ).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]
            delta, off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
    else:
        # 跑调的长度为1
        if off_key_length==1:
            # 设定跑调的长度
            off_key_length_temp = off_key_length
            # 确定跑调的位置 全序列随机跑调
            off_key_loc_temp = np.array(random.sample(range(0,arr_length),1)).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]
            delta,off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
        elif off_key_length==2:
            # 设定跑调的长度
            off_key_length_temp = off_key_length
            # 确定跑调的位置 全序列随机跑调
            off_key_loc_temp = np.array(random.sample(range(0, arr_length-1), 1)).astype(int)
            # 将下一位加到off_Key_loc_temp
            off_key_loc_temp = np.append(off_key_loc_temp,off_key_loc_temp[0]+1).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]

            delta, off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
        elif off_key_length > 2:
            # 设定跑调的长度
            off_key_length_temp = random.sample(range(2,off_key_length+1),1)[0]
            # 确定跑调的位置 全序列随机跑调
            off_key_loc_temp = np.array(random.sample(range(0, arr_length - off_key_length_temp + 1), 1)).astype(int)
            # 因为off_key_length大于 2 将off_key_loc_temp[0] 的下n-1位也加入到temp中
            off_key_loc_temp = np.append(off_key_loc_temp,
                                         np.array([off_key_loc_temp[0] + i for i in range(1, off_key_length_temp)])
                                         ).astype(int)
            # score_data中的跑调位置
            loc_array_temp = score_data_temp[off_key_loc_temp]
            delta, off_key_diff = add_util(off_key_length=off_key_length_temp)
            # 将偏差加到score_data上
            score_data[loc_array_temp] = score_data[loc_array_temp] + delta * off_key_diff
    return score_data,off_key_loc_temp,loc_array_temp


def find_and_append(score_data_temp,loc_array_temp,score_queue):
    score_data_temp_not_deal = []
    for i in score_data_temp:
        if i not in loc_array_temp:
            score_data_temp_not_deal.append(i)
    if len(score_data_temp_not_deal) > 0:
        temp = -1
        for i in range(len(score_data_temp_not_deal) - 1):
            if score_data_temp_not_deal[i] + 1 != score_data_temp_not_deal[i + 1]:
                temp = i
                break
        # 说明剩下的是连续的一段
        if temp == -1:
            score_queue.append(score_data_temp_not_deal)
        # 剩下的是 1 + 一段
        else:
            score_queue.append(score_data_temp_not_deal[:temp + 1])
            score_queue.append(score_data_temp_not_deal[temp + 1:])
    return score_queue


