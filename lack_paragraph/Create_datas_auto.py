# -*- coding: utf-8 -*-
# @Time    : 2019-11-20 10:42
# @Author  : RichardoMu
# @File    : Create_datas_auto.py
# @Software: PyCharm


import numpy as np
import os
import random
from add_utils import add_diff2score,find_and_append
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


lin1 = np.linspace(0, 0.5, 50)
lin1_2 = np.linspace(-0.5, 0, 50)
lin2 = np.linspace(2, 4, 150)
lin2_2 = np.linspace(-4, -2, 150)
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


def paragraph_lack(data,lack_pro):
    """
    :param data:
    :param lack_pro: 跑调的概率
    lack_pro * length =1
        lack
    lack_pro * length >=2
        保证
    :return:
    """
    #  成段漏音
    length = data.shape[0]
    # 缺音数
    lack_number = round(length*lack_pro)
    data_dict = {i: 1 for i in range(length)}
    loc = np.ones(length).astype(int)
    if lack_number == 0:
        lack_loc = np.array([])
        return data,lack_loc
    elif lack_number == 1:
        lack_loc = np.array(random.sample(range(0,length),1))
        data = np.delete(data,lack_loc)
        return data,lack_loc
    elif lack_number == 2:
        lack_loc = random.sample(range(0,length-1),1)
        lack_loc.append(lack_loc[0]+1)
        data = np.delete(data,lack_loc)
        return data,np.array(lack_loc)
    else:
        # 每选择一个lack位置，将之置为-1
        lack_loc = np.array([])
        while lack_number != 0:
            lack_loc_temp = np.array([])
            if lack_number == 1:
                lack_loc_temp1 = random.sample(range(0,length),1)
                if (loc[lack_loc_temp1]==1).all():
                    lack_loc = np.append(lack_loc,lack_loc_temp1).astype(int)
                    loc[lack_loc_temp1] = -1
                    lack_number -= 1
                    break
                else:
                    continue
            if lack_number == 2:
                lack_loc_temp1 = random.sample(range(0,length-1),1)
                lack_loc_temp1 = np.append(lack_loc_temp1,lack_loc_temp1[0]+1).astype(int)
                if (loc[lack_loc_temp1]==1).all():
                    lack_loc = np.append(lack_loc,lack_loc_temp1)
                    loc[lack_loc_temp1] = -1
                    lack_number -= 2
                    break
                else:
                    continue
            lack_length = random.sample(range(2,lack_number),1)
            lack_loc_temp1 = random.sample(range(0,length-lack_length[0]),1)
            # print(lack_loc_temp1)
            lack_loc_temp = np.append(lack_loc_temp,np.array([lack_loc_temp1[0]+i for i in range(lack_length[0])])).astype(int)
            # print(loc[lack_loc_temp]==1)
            if (loc[lack_loc_temp1]==1).all():
                lack_loc = np.append(lack_loc,lack_loc_temp).astype(int)
                loc[lack_loc_temp] = -1
                lack_number -= lack_length[0]
            else:
                continue
        data = np.delete(data,lack_loc)
        # print("done!")
        return data,np.sort(lack_loc)



def file_path(p_,number):
    folder_name = "lack-" + str(p_) + "_deviate_number-" + str(number)
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

def off_key_paragraph3(off_key_pro):
    """
    :param off_key_pro: 跑调的概率
    :return:
    """
    # 成段跑调
    # score_data : 函数中的模板序列 长度71
    score_data = score1_arr + 0.
    # 模板序列的长度
    score_length = score_data.shape[0]
    # off_key_length : 跑调的长度 四舍五入
    off_key_length = round(score_length*off_key_pro)
    # print(off_key_length)
    # score_queue : 队列数据结构 保存没有处理过的list
    # 初始为全部 [[0,1,2,3...,70]]
    score_queue = [[i for i in range(score_length)]]
    # loc_array :设置标志序列 为1的为未处理过的  为-1 的为被处理过的
    # 长度71 ， 形式和乐谱序列相同
    loc_array = np.ones_like(score_data).astype(int)

    # 跑调处理

    # 情况1 跑调off_key_length = 0 没有跑调情况
    # 直接返回score_data
    if off_key_length == 0:
        pass
    # 情况2 跑调off_key_length = 1 有一个跑调，随机找一个位置跑调即可
    elif off_key_length == 1:
        score_data_temp = np.array(score_queue[0])
        score_data,_,_ = add_diff2score(off_key_length,score_data,score_data_temp,score_length)
    # 情况3 跑调off_key_length = 2 有2个跑调，找一段跑调
    elif off_key_length == 2:
        score_data_temp = np.array(score_queue[0])
        score_data,_,_ = add_diff2score(off_key_length,score_data,score_data_temp,score_length)
    # 情况4 跑调off_key_length > 2 有3个及3个以上的跑调，则需要进行队列的进出 和 判断off_key_length and temp_score_queue的长度，谁长
    else :
        while off_key_length > 0:
            # 现将队列中的未处理过的各段shuffle
            random.shuffle(score_queue)
            # 从队列中取出来一个为处理的list 该list的内容为 某未处理段的indexs 且连续 如 [3,4,5,6,7]
            score_data_temp = np.array(score_queue[0])
            # 计算未处理段的长度 和 应该跑调的长度比较
            score_data_temp_length = len(score_data_temp)
            # 如果应该跑调的数量等于取出的段的长度，那么选取跑调的长度和位置应该基于temp_score_queue_length或off_key_length 然后从第一位开始跑调就可以 这样会出现一个问题就是当全跑调的时候，直接全加了
            if off_key_length >= score_data_temp_length:
                score_data,off_key_loc_temp,loc_array_temp  = add_diff2score(off_key_length=off_key_length,score_data=score_data,score_data_temp=score_data_temp,arr_length=score_data_temp_length,style='upper')
                off_key_length -= len(loc_array_temp)
                loc_array[loc_array_temp] = -1
                # 提取出本段除去off_key_loc的段  可能有1段或者两段
                # 排除处理的位置
                score_queue = find_and_append(score_data_temp=score_data_temp,loc_array_temp=loc_array_temp,score_queue=score_queue)
                del score_queue[0]
            # 如果off_key_length < score_data_temp_length off_key_length 来判断
            else:
                score_data,off_key_loc_temp,loc_array_temp = add_diff2score(off_key_length=off_key_length,score_data=score_data,score_data_temp=score_data_temp,arr_length=score_data_temp_length,style='down')
                off_key_length -= len(loc_array_temp)
                loc_array[loc_array_temp] = -1
                # 提取出本段除去off_key_loc的段  可能有1段或者两段
                # 排除处理的位置
                score_queue = find_and_append(score_data_temp=score_data_temp,loc_array_temp=loc_array_temp,score_queue=score_queue)
                del score_queue[0]
    for i in range(len(score_data)):
        if loc_array[i] == 1:
            delta = np.random.choice([-1,1],1)
            add_arr = np.random.uniform(0.,0.49,1)
            score_data[i] += delta * add_arr
    return score_data


def create_data(delta,mul):
    # delta dtype int  lack   mul dtype int  deviation
    # prob of lack score
    p_ = 0.01*delta
    mul = round(mul*0.05,2)
    p = np.array([1-mul, mul])
    Folder_path,Folder_name, save_file, label_file = file_path(p_,p)
    # number = 2
    for i in range(100):
        # data = get_same_length_data(mul)
        # data = deviation(mul)
        data = off_key_paragraph3(off_key_pro=mul)
        data2, lack_loc = paragraph_lack(data, p_)
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
    create_data(delta=10,mul=0)
    # deviation(number=2)