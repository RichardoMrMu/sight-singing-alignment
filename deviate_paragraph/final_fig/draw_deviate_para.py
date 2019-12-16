# -*- coding:utf-8 -*-
# @Time     : 2019-12-09 15:53
# @Author   : Richardo Mu
# @FILE     : draw_deviate_random.PY
# @Software : PyCharm
from matplotlib import pyplot as plt
import mpl_toolkits.axisartist as axisartist
import csv
import os
import numpy as np
root = os.getcwd()
print(root)
csv_file = "E:\\debug\\pyCharmdeBug\\alignment_new_2\\deviate_paragraph\\csv_folder\\paralack-0.0_deviate-1.0.csv"

accuracy_sw_array = np.array([])
accuracy_sw_ab_array = np.array([])
with open(csv_file,'r',newline='') as f:
    reader = csv.reader(f)
    # for i in range(len())
    for line in reader:
        accuracy_sw_array = np.append(accuracy_sw_array,round(float(line[0])*100,2))
        accuracy_sw_ab_array = np.append(accuracy_sw_ab_array,round(float(line[1])*100,2))
    x = np.arange(101) * 0.01
    # 创建画布
    fig = plt.figure()
    # 使用axisartist.subplot方法创建一个绘图区对象ax
    ax = axisartist.Subplot(fig,111)
    fig.add_axes(ax)
    ax.axis["bottom"].set_axisline_style("-|>",size=2)
    ax.axis["left"].set_axisline_style("-|>", size=2)
    ax.axis['top'].set_visible(False)
    ax.axis['right'].set_visible(False)
    # sw 相对音高正确率曲线
    plt.plot(x, accuracy_sw_array, c='r', linestyle="-.", label='RP-NW')
    # sw 绝对音高正确率曲线
    plt.plot(x, accuracy_sw_ab_array, c="b", linestyle="-", label='AP-NW')
    plt.xlim(0,1.05)
    plt.ylim((0,105))
    # 画垂直参考线
    plt.vlines(0.74, 0, 100,colors='k',linestyles='--')

    # 设置表的字体
    plt.xlabel('The Rate of Error Note ',fontdict={'family':'Times New Roman','size':16})
    plt.ylabel('Accuracy(%)',fontdict={'family':'Times New Roman','size':16})
    # 横纵坐标的字体
    plt.xticks(fontproperties='Times New Roman',size=14)
    plt.yticks(fontproperties='Times New Roman', size=14)
    # label
    plt.legend(prop={'family':'Times New Roman','size':14})
    # 标出点
    plt.annotate('(0.74,'+str(accuracy_sw_ab_array[74])+")", xy=(0.74, accuracy_sw_ab_array[74]), xytext=(0.5, accuracy_sw_ab_array[74]-15), arrowprops=dict(facecolor='black', shrink=0.1))
    plt.annotate('(0.74,'+str(accuracy_sw_array[74])+")", xy=(0.74, accuracy_sw_array[74]), xytext=(0.53, accuracy_sw_array[74]-13),
                 arrowprops=dict(facecolor='black', shrink=0.01))
    name = os.path.basename(csv_file)
    name = "".join(name).split(".csv")
    # path = root + "\\"+"实验一成段同趋势跑调" + ".tiff"
    path = root + "\\" + "实验一成段同趋势跑调" + ".eps"
    # plt.savefig(path, dpi=200,format='tiff')
    plt.savefig(path, dpi=200, format='eps')
    plt.close()