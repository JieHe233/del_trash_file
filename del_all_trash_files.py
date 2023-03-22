import os, time, math
import multiprocessing as mp
from concurrent import futures
import argparse
from datetime import datetime


def get_change_time(dir_or_file):
    t1 = os.path.getmtime(dir_or_file)
    # file_change_date = time.strftime('%Y-%m-%d', time.localtime(t1))
    return t1


def check_item(item, input_file_path):
    if item in input_file_path:
        return True
    return False

def check_all_files(scan_dir):
    for curDir, dirs, files in os.walk(scan_dir):
        for file in files:
            file_path = os.path.join(curDir, file)
            if os.path.exists(file_path) and check_item(input_mode, file_path):                
                if (datetime.now() - datetime.fromtimestamp(get_change_time(file_path))).days > keep_day:
                    f = open('temp_files_to_del.txt', 'a')
                    f.write(file_path + '\t' + get_change_time(file_path) + '\n')
                    f.close()

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--target_dir', help='The target dir to clean')
parser.add_argument('-p', '--processes', help='The number of processes used to scan all the files and clean the temp trash files')
parser.add_argument('-o', '--outfile', help='The file used for saving the path for all the trash files scaned')
parser.add_argument('-k', '--keep_day', help='Set the limit for the date, if the file was changed before the date, \
                                                then the file was assumed as trashfile, else not')
parser.add_argument('-i', '--file_mode', help='The file mode for the trash file, \
                                                if file mode exists in any file, the file is assumed as trash file')


args = parser.parse_args()
target_dir = args.target_dir
process_num = args.processes
outfile = args.outfile
keep_day = args.keep_day
input_mode = args.file_mode

# all_dirs = os.listdir(target_dir)

# 对所有父目录进行拆分处理，每次处理1000个样本，防止进程卡死
for i in range(0, math.ceil(len(all_dirs)/1000)):
   end = len(all_dirs) if (i+1)*100 > len(all_dirs) else (i+1)*100
   pool = mp.Pool(processes = process_num)
   pool.map(check_all_files, all_dirs[i*100: end])
   pool.close()
   pool.join()
