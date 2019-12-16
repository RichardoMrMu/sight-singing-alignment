# -*- coding: utf-8 -*-
# @Time    : 2019-11-11 14:57
# @Author  : RichardoMu
# @File    : DTW.py
# @Software: PyCharm
# https://github.com/Mr-Wang119/SequenceAlignment/blob/master/SequenceAlignment.py
import time
import numpy as np
# Algorithm based dtw  dynamic time wrapping


def relative_pitch(x,y):
    x, y = np.array(x), np.array(y)
    x_diff = x[1:] - x[0:-1]
    _lt = np.where(x_diff < 0)[0]
    _eq = np.where(x_diff == 0)[0]
    _gt = np.where(x_diff > 0)[0]
    x_diff[_lt] = 1
    x_diff[_eq] = 2
    x_diff[_gt] = 3

    y_diff = y[1:] - y[0:-1]
    _lt = np.where(y_diff < 0)[0]
    _eq = np.where(y_diff == 0)[0]
    _gt = np.where(y_diff > 0)[0]
    y_diff[_lt] = 1
    y_diff[_eq] = 2
    y_diff[_gt] = 3
    return x_diff,y_diff


def DTW(x, y, flag="relative"):
    # type of x,y : list   type of x,y element:int
    # x : score_note
    # y : det_note

    # use relative pitch
    if flag == "relative":
        x, y = relative_pitch(x, y)

    m = len(x)
    n = len(y)

    class cell:
        def __init__(self, cost, pointer, x, y):
            self.cost = cost
            self.pointer = pointer
            self.x = x
            self.y = y

    # initialization
    opt = [[cell(0, None, idx_x, idx_y) for idx_y in range(n + 1)] for idx_x in range(m + 1)]
    # A1 as score_note A2 as det_note
    A1,A2 = [],[]
    # A2 = []
    for i in range(m - 1, -1, -1):
        opt[i][n].cost = 2 * (m - i)
        opt[i][n].pointer = opt[i + 1][n]
    for j in range(n - 1, -1, -1):
        opt[m][j].cost = 2 * (n - j)
        opt[m][j].pointer = opt[m][j + 1]
    x = [str(i) for i in x]
    y = [str(i) for i in y]
    if flag == "relative":
        x.append(str(2))
        y.append(str(2))
    # fill the table opt
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            penalty = 0
            # pdb.set_trace()
            if x[i] != y[j]:
                penalty = 1
            below = opt[i + 1][j].cost + 2
            right = opt[i][j + 1].cost + 2
            diagonal = opt[i + 1][j + 1].cost + penalty
            if below <= right and below <= diagonal:
                opt[i][j].cost = below
                opt[i][j].pointer = opt[i + 1][j]
            elif right <= below and right <= diagonal:
                opt[i][j].cost = right
                opt[i][j].pointer = opt[i][j + 1]
            else:
                opt[i][j].cost = diagonal
                opt[i][j].pointer = opt[i + 1][j + 1]

    # find the way
    nextcell = opt[0][0]
    while nextcell.pointer != None:
        nextcell_next_x = nextcell.pointer.x
        nextcell_next_y = nextcell.pointer.y
        if nextcell.x == nextcell_next_x:
            # A1 = A1 + '-'
            A1.append("-")
            # A2 = A2 + y[nextcell.y]
            A2.append(y[nextcell.y])
        elif nextcell.y == nextcell_next_y:
            # A1 = A1 + x[nextcell.x]
            # A2 = A2 + '-'
            A1.append(x[nextcell.x])
            A2.append("-")
        else:
            A1.append(x[nextcell.x])
            A2.append(y[nextcell.y])
            # A1 = A1 + x[nextcell.x]
            # A2 = A2 + y[nextcell.y]
        nextcell = nextcell.pointer
    # sw_ref_str => A1  sw_query_str =>A2 ref_str => x query_str => y
    locate_info = {}
    pading_zero_loc = []
    delte_loc = []
    for i in range(len(A1)):
        if A1[i] != '-' and A2[i] != '-':
            loc_ref = x.index(A1[i])
            loc_query = y.index(A2[i])
            x[loc_ref] = -1
            y[loc_query] = -1
            locate_info[loc_query] = loc_ref
        elif A1[i] != '-' and A2[i] == '-':
            loc_ref = x.index(A1[i])
            x[loc_ref] = -1
            pading_zero_loc.append(loc_ref)
        elif A1[i] == '-' and A2[i] != '-':
            loc_query = y.index(A2[i])
            y[loc_query] = -1
            # delte_loc 之后没有用到
            delte_loc.append(loc_query)

    values = locate_info.values()
    for i in range(len(x)):
        if (i not in values) and (i not in pading_zero_loc):
            pading_zero_loc.append(i)
    for zero_loc in pading_zero_loc:
        locate_info[10000 - zero_loc] = zero_loc

    locate_info = sorted(locate_info.items(), key=lambda x: x[1])
    match_loc_info = {
        'loc_info': locate_info,
        'zero_loc': pading_zero_loc
    }

    # return opt[0][0].cost, A1, A2
    return match_loc_info,opt


def main():
    # sequence alignment using DTW
    print("请输入x: ")
    x = input()
    print("请输入y: ")
    y = input()
    m = len(x)
    n = len(y)
    start = time.time()
    cost, A1, A2 = DTW(x, y)
    end = time.time()
    print("Sequence length of X: " + str(m) + "   Sequence length of Y: " + str(n) + "   Runtime of Algorithm 2(s): " + str(
        end - start) + "   cost: " + str(cost))
    print("the optimal alignment of the two sequences is: ")
    print(A1)
    print(A2)


if __name__ == '__main__':
    main()

