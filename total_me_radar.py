# convert _me and _radar scv file to total csv file
import os
import pandas as pd
import xml.etree.ElementTree as ET
from collections import Counter
import csv
import natsort

# FIND = '_me'
FIND = '_radar'

total_file_li = []
to_len = 0
root_li = []
count = 0

# #  folder dir list
# root_dir = '/Users/jowanseo/Desktop/Recoder_test1'
# for (root, dirs, files) in os.walk(root_dir):
#     print("# root : " + root)
#     root_li.append(root)

# ====== 나중에 폴더 전체 파일 가지고 올때 열고 일단 하나의 폴더에 대해서만 진행  ====
# for path in root_li:
#     path_dir = path

path_dir = '/Users/jowanseo/Desktop/Recoder_test1'
file_list = os.listdir(path_dir)
#  여기 위에 두줄 지우고 두줄 위의 내용 풀기

for j in file_list :
    if j.find(FIND) != -1 :
        total_file_li.append(j)

total_file_li = natsort.natsorted(total_file_li,reverse=False)
base_file = total_file_li[-1]
del total_file_li[-1]

#  file number error check
if FIND == '_me':
    if len(total_file_li) != 10 :
        print("total num of _me file error at this path : {}".format(path_dir))
        with open("{}/error_log.txt".format(path_dir), "w") as file:
            file.write("total num of _me file error at this path : {}".format(path_dir))
            file.close()

elif FIND == '_rader' :
    if len(total_file_li) != 18 :
        print("total num of _radar file error at this path : {}".format(path_dir))
        with open("{}/error_log.txt".format(path_dir), "w") as file:
            file.write("total num of _radar file error at this path : {}".format(path_dir))
            file.close()


# base file 에 대해서 진행
pd_list = []
f = open("{}/{}".format(path_dir,base_file), 'r', encoding='utf-8')
rdr = csv.reader(f)
count = 0

for line in rdr:
    if count == 0:
        header = line[:2]
    count+=1
    if count > 1 :
        if count == 2 :
            col_li = line
            num_col = len(col_li)
        else : pd_list.append(line[:num_col])

data_ = pd.DataFrame(pd_list,columns=col_li)
total_df = data_
#  base 의 time stamp 얻어놓기
base_time_stamp = total_df.iloc[:,0]


for i in range(len(total_file_li)):
# for i in range(1):
    num_col = 0
    pd_list_ = []
    f = open("{}/{}".format(path_dir,total_file_li[i]), 'r', encoding='utf-8')
    rdr = csv.reader(f)
    count = 0
    for line in rdr:
        count+=1
        if count > 1 :
            if count == 2 :
                col_li = line
                num_col = len(col_li)
            else :
                for index, item in enumerate(line[:num_col]):
                    if  item == '':
                        line[:num_col][index] = 'Nan'
                pd_list_.append(line[:num_col])

    data = pd.DataFrame(pd_list_, columns=col_li)
    print(data.iloc[:, ])

# get time stamp
    new_data_time_stamp = data.iloc[:,0]
    new_t_li  = list(new_data_time_stamp)
    b_t_li = list(base_time_stamp)

# time stamp error check
    if new_t_li != b_t_li :
        print("time stamp error at this path : {} file : {}".format(path_dir,total_file_li[i]))
        print("give up making total file of this dir")
        with open("{}/error_log.txt".format(path_dir), "w") as file:
            file.write("time stamp error at this path : {} file : {}".format(path_dir,total_file_li[i]))
            file.close()
        break

    new_file_df = data.iloc[:,21:]
    a = len(new_file_df.iloc[0,:])
    b = len(total_df.columns)
    total_df = pd.concat([total_df,new_file_df],axis=1)
    c = len(total_df.columns)
    if c == a+b : print("true")


#  header 포함 trun out to csv file
f = open("{}/{}.csv".format(path_dir,'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'w', newline='')
wr = csv.writer(f)
wr.writerow([header[0],header[1]])
f.close()

with open("{}/{}.csv".format(path_dir,'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'a') as f:
    total_df.to_csv(f, header=True, index=False)


# 폴더마다, row 확인하는 코드 추가하기







