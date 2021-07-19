# Title: Convert CAN_data(_me,_radar) to total .csv file, Date: 2021.7.18, Writer: Wan seo Jo
import os
import pandas as pd
import csv
import natsort
# ====== INIT ======
# FIND = '_me'
FIND = '_radar'
THRESHOLD = 0.0000001
root_dir = '/Users/jowanseo/Desktop/Recoder_test1'
# ===================
root_li = []
for (root, dirs, files) in os.walk(root_dir):
    root_li.append(root)
err_path = root_li[0]

for path_dir in root_li:
    total_file_li = []
    file_list = os.listdir(path_dir)
    for j in file_list :
        if j.find(FIND) != -1 :
            total_file_li.append(j)
    total_file_li = natsort.natsorted(total_file_li,reverse=False)

    if len(total_file_li) == 0 :
        print("No file at {} dir..".format(path_dir))
        with open("{}/error_log{}.txt".format(err_path,FIND), "a") as file:
            file.write("No file at {} dir..\n".format(path_dir))
            file.close()
        continue
    else:
        base_file = total_file_li[-1]
        del total_file_li[-1]
#  file number error check
    if FIND == '_me':
        if len(total_file_li) != 10 :
            print("*** error ***\ntotal num of _me file error at this path : {}".format(path_dir))
            with open("{}/error_log{}.txt".format(err_path,FIND), "a") as file:
                file.write("*** error ***\ntotal num of _me file error at this path : {}\n\n".format(path_dir))
                file.close()
                continue
    elif FIND == '_radar':
        if len(total_file_li) != 18 :
            print("*** error ***\ntotal num of _radar file error at this path : {}".format(path_dir))
            with open("{}/error_log{}.txt".format(err_path,FIND), "a") as file:
                file.write("*** error ***\ntotal num of _radar file error at this path : {}\n\n".format(path_dir))
                file.close()
                continue
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
    base_time_stamp = total_df.iloc[:,0]

    for i in range(len(total_file_li)):
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
# row Nan check
        ro_err = 0
        test_d = data
        df_1 = test_d['CAM_1'] == ''
        test_d = test_d.loc[df_1,:]
        df_2 = test_d['CAM_2'] == ''
        test_d = test_d.loc[df_2, :]
        df_3 = test_d['CAM_3'] == ''
        test_d = test_d.loc[df_3, :]
        test_d  = test_d.iloc[:,21:]
        test_d_co = test_d.columns

        for test_dco in test_d_co :
            row_check = [str(x) for x in pd.DataFrame(test_d[test_dco]).values.squeeze(axis=1)]
            if '' in row_check:
                print("*** error ***\nrow value Nan error path: {}, file_name : {}, error column : {}".format(path_dir,total_file_li[i],test_dco))
                with open("{}/error_log{}.txt".format(err_path,FIND), "a") as file:
                    file.write("*** error ***\nrow value Nan error path: {}, file_name : {}, error column : {}\n\n".format(path_dir,total_file_li[i],test_dco))
                    file.close()
                    # ro_err+=1
                    # break
        # if ro_err == 1 : break
        new_data_time_stamp = data.iloc[:, 0]
        new_t_li = list(new_data_time_stamp)
        b_t_li = list(base_time_stamp)
# time stamp error check
        for nu in range(len(b_t_li)):
            if abs(float(new_t_li[nu]) - float(b_t_li[nu])) > THRESHOLD :
                print("*** error ***\ntime stamp error at this path : {} file : {}".format(path_dir,total_file_li[i]))
                with open("{}/error_log{}.txt".format(err_path,FIND), "a") as file:
                    file.write("*** error ***\n")
                    file.write("time stamp error at this path : {} file : {}\n\n".format(path_dir,total_file_li[i]))
                    file.close()
        new_file_df = data.iloc[:,21:]
        total_df = pd.concat([total_df,new_file_df],axis=1)
        print("..processing..")

    f = open("{}/{}.csv".format(path_dir,'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'w', newline='')
    wr = csv.writer(f)
    wr.writerow([header[0],header[1]])
    f.close()
    with open("{}/{}.csv".format(path_dir,'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'a') as f:
        total_df.to_csv(f, header=True, index=False)