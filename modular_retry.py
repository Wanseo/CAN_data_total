# Title: Convert CAN_data(_me,_radar) to total .csv file, last commit 2021.7.20, Writer: Wan seo Jo
import os
import pandas as pd
import csv
import natsort
# ===== INIT =====
ORIGIN_PATH  = '/Users/jowanseo/Desktop/Recoder_test1'
err_path = ORIGIN_PATH
THRESHOLD = 0.0000001
# ===== FILE =====
# FIND = '_me'
FIND = '_radar'
# ================

def find_Dir(root_dir): # finding dirs
    dir_li = []
    for (root, dirs, files) in os.walk(root_dir):
        dir_li.append(root)
    return dir_li

def find_Files(path_dir): # finding files
    file_li = []
    file_list = os.listdir(path_dir)
    for j in file_list:
        if j.find(FIND) != -1:
            file_li.append(j)
    total_file_li = natsort.natsorted(file_li, reverse=False)
    return total_file_li

def load_data(path_dir, base_file, cnt): # load data
    num_col = 0
    pd_list = []
    f = open("{}/{}".format(path_dir, base_file), 'r', encoding='utf-8')
    rdr = csv.reader(f)
    count = 0
    for line in rdr:
        if count == 0:
           header = line[:2]
        count += 1
        if count == 2:
            col_li = line
            num_col = len(col_li)
        if count > 2 :
            if cnt == 0:
                pd_list.append(line[:num_col])
            else:
                for index, item in enumerate(line[:num_col]):
                    if item == '':
                        line[:num_col][index] = 'Nan'
                pd_list.append(line[:num_col])
    data_ = pd.DataFrame(pd_list, columns=col_li)
    return data_, header

def fileNum_Error(total_file_li, path_dir, FIND): # check num of files error
    go = 0
    if FIND == '_me' :
        if len(total_file_li) == 11 : go+=1
    if FIND == '_radar' :
        if len(total_file_li) == 19 : go+=1
    if go == 1 : return 0
    elif go == 0:
        print("*** error ***\ntotal num of {} file error at this path : {}".format(FIND,path_dir))
        with open("{}/error_log{}.txt".format(err_path, FIND), "a") as file:
            file.write("*** error ***\ntotal num of _me file error at this path : {}\n\n".format(path_dir))
            file.close()
        return 2

def rowNan_Error(data, path_dir, total_file_li): # check row Nan value error
    test_d = data
    df_1 = test_d['CAM_1'] == ''
    test_d = test_d.loc[df_1, :]
    df_2 = test_d['CAM_2'] == ''
    test_d = test_d.loc[df_2, :]
    df_3 = test_d['CAM_3'] == ''
    test_d = test_d.loc[df_3, :]
    test_d = test_d.iloc[:, 21:]
    test_d_co = test_d.columns
    for test_dco in test_d_co:
        row_check = [str(x) for x in pd.DataFrame(test_d[test_dco]).values.squeeze(axis=1)]
        if '' in row_check:
            print("*** error ***\nrow value Nan error path: {}, file_name : {}, error column : {}".format(
                path_dir, total_file_li, test_dco))
            with open("{}/error_log{}.txt".format(err_path, FIND), "a") as file:
                file.write(
                    "*** error ***\nrow value Nan error path: {}, file_name : {}, error column : {}\n\n".format(
                        path_dir, total_file_li, test_dco))
                file.close()

def timeStamp_Error(b_t_li,new_t_li,path_dir,total_file_li): #check time stamp error
    for nu in range(len(b_t_li)):
        if abs(float(new_t_li[nu]) - float(b_t_li[nu])) > THRESHOLD:
            print("*** error ***\ntime stamp error at this path : {} file : {}".format(path_dir,
                                                                                       total_file_li))
            with open("{}/error_log{}.txt".format(err_path, FIND), "a") as file:
                file.write("*** error ***\n")
                file.write(
                    "time stamp error at this path : {} file : {}\n\n".format(path_dir, total_file_li))
                file.close()

def toCSV(path_dir,total_df,header): # turn to CSV file
        f = open("{}/{}.csv".format(path_dir, 'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'w', newline='')
        wr = csv.writer(f)
        wr.writerow([header[0], header[1]])
        f.close()
        with open("{}/{}.csv".format(path_dir, 'Recorder_2020-11-03_17-04-22_total{}'.format(FIND)), 'a') as f:
            total_df.to_csv(f, header=True, index=False)
        
def concatData(data,total_df): # concat data
        new_file_df = data.iloc[:, 21:]
        total_df = pd.concat([total_df, new_file_df], axis=1)
        print("..processing..")
        return total_df

def totalCSV(root_dir): # total csv file
    for path_dir in find_Dir(root_dir):
        total_file_li = find_Files(path_dir)
        err_val = fileNum_Error(total_file_li, path_dir, FIND)
        if err_val == 2 :
            continue
        else :
            base_file = total_file_li[-1]
            del total_file_li[-1]
        cnt = 0
        total_df, header = load_data(path_dir, base_file, cnt) # base file
        for i in range(len(total_file_li)): # rest files
            data, header = load_data(path_dir,total_file_li[i],cnt)
            cnt +=1
            rowNan_Error(data, path_dir, total_file_li[i]) # row Nan check
            timeStamp_Error(list(total_df.iloc[:, 0]), list(data.iloc[:, 0]), path_dir, total_file_li[i]) # time stamp error check
            total_df = concatData(data, total_df) # data concat
        toCSV(path_dir,total_df,header) # turn to csv file

if __name__ == '__main__':
    totalCSV(ORIGIN_PATH)

