# -*- coding: utf-8 -*-
# @Time    : 2019-11-20 10:42
# @Author  : RichardoMu
# @File    : Create_datas_auto.py
# @Software: PyCharm


import numpy as np
import os
import random
path = os.getcwd()
score1 = os.path.join(path,  '308_score.txt')
np.random.seed(1234)
random.seed(1234)
fr = open(score1, 'r')
score1_list = fr.readlines()
fr.close()

for x in range(len(score1_list)):
    score1_list[x] = float(score1_list[x].strip())
# score1_list
score1_arr = np.array(score1_list)


lin1 = np.linspace(0, 0.49, 50)
lin1_2 = np.linspace(-0.49, 0, 50)
lin2 = np.linspace(2, 4.5, 150)
lin2_2 = np.linspace(-4.5, -2, 150)
lin1 = np.append(lin1, lin1_2)
lin2 = np.append(lin2, lin2_2)
lin1 = lin1[np.random.permutation(len(lin1))]
lin2 = lin2[np.random.permutation(len(lin2))]


def get_same_length_data(p):
    score1_data = []
    for i in range(len(score1_arr)):
        x1 = np.random.randint(len(lin1))
        x2 = np.random.randint(len(lin2))
        distr = np.array([lin1[x1],lin2[x2]])
        # 以p概率从distr中选1个
        t = np.random.choice(distr, 1, p=p)
        score1_data.append(t[0])

    score1_data = np.array(score1_data)
    score1_data = score1_data + score1_arr
    return score1_data


def random_lack(data,p=0.05):
    length = data.shape[0]
    lack_num = int(round(length * p))
    lack_loc = np.random.randint(0,length-1,lack_num)
    lack_loc = np.unique(np.sort(lack_loc))
    temp = data
    temp = np.delete(temp, lack_loc)

    return temp, lack_loc


def file_path(p_,p):
    folder_name = "lack-" + str(p_) + "_deviate-" + str(p[1])
    folder_path = path + "\\data\\" + folder_name
    if not os.path.exists(path+"\\data\\"+folder_name):
        os.mkdir(folder_path)
    save_file = folder_path + "\\data"
    label_file = folder_path + "\\label"
    if not os.path.exists(save_file):
        os.mkdir(save_file)
    if not os.path.exists(label_file):
        os.mkdir(label_file)
    return folder_path, folder_name,save_file, label_file


def deviation(number):
    """
    :param number: how many do u want to deiation total 32
    :return:
    """
    # score_note = score1_arr
    score_data = np.zeros_like(score1_arr)
    music_info = {0:[0],1:[1,2,3],2:[4],3:[5,6,7],4:[8,9,10],5:[11,12,13],6:[14],
                  7:[15],8:[16],9:[17,18,19],10:[20],11:[21,22,23],12:[24,25,26],
                  13:[27,28,29],14:[30,31,32],15:[33,34,35],16:[36],17:[37,38],
                  18:[39],19:[40,41],20:[42,43,44],21:[45,46],22:[47],23:[48,49,50],
                  24:[51],25:[52,53,54],26:[55],27:[56,57,58],28:[59,60,61],
                  29:[62,63,64],30:[65,66,67],31:[68,69,70]}

    # len_music_info = len(music_info)
    # length : 32
    data = random.sample(range(0,32),number)
    deviation_index = sorted(data)
    # 保存跑调的段落
    deviation_dict = {deviation_index[i]:music_info[deviation_index[i]] for i in range(len(deviation_index))}
    # print(deviation_dict)
    # 上面被选中的deviation_index 是要加上2-4 的跑调，除此之外的内容
    # 只需要加上0-0.5的deviation就可以了
    # delete deviation index
    for i in range(len(deviation_index)):
        music_info.pop(deviation_index[i])
    # 给score1_arr跑调段落加上2-4
    for i in deviation_dict.keys():
        # delta include 1 and -1
        delta = np.random.choice([-1,1],1)
        dev_arr = np.random.uniform(2.0,4.5,len(deviation_dict[i]))
        score_data[deviation_dict[i]] = dev_arr*delta + score1_arr[deviation_dict[i]]
    for i in music_info.keys():
        delta = np.random.choice([-1,1],1)
        dev_arr = np.random.uniform(0,1.0,len(music_info[i]))
        score_data[music_info[i]] = dev_arr*delta + score1_arr[music_info[i]]
    return score_data


def create_data(delta,mul):
    # delta dtype int  lack   mul dtype int  deviation
    # prob of lack score
    p_ = 0.02*delta
    mul *= 0.01
    p = np.array([1-mul, mul])
    Folder_path,Folder_name, save_file, label_file = file_path(p_,p)
    # number = 2
    for i in range(100):
        data = get_same_length_data(p)
        # data = deviation(number)
        # data = off_key_paragraph(off_key_pro=mul)
        data2, lack_loc = random_lack(data, p=p_)
        # print(data2.shape)
        with open(os.path.join(save_file, str(i + 1) + '.txt'), 'w+') as f:
            for x in data2:
                f.write(str(x) + '\n')

        with open(os.path.join(label_file, str(i + 1) + '_label.txt'), 'w+') as f2:
            for i in range(len(score1_list)):
                if (i in lack_loc):
                    f2.write(str(score1_arr[i]) + '\t' + '-' + '\n')
                else:
                    f2.write(str(score1_arr[i]) + '\t' + str(data[i]) + '\n')
    # print(Folder_name,"\n",Folder_path)
    print("lack:%f,deviate rate:%f   "%(p_,mul),end='')
    return Folder_path,Folder_name


if __name__ == '__main__':
    create_data(delta=1,mul=20)
    # deviation(number=2)