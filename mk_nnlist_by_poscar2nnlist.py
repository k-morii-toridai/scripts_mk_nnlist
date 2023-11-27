import os
import sys
import time
import shutil
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import numpy as np


# nnlistを作成したいPOSCARファイルの親フォルダリスト（.npy）のパスをコマンドライン引数として受け取る
args = sys.argv
# load poscar existed folder list
print("Now loading poscar_folder_path_list from .npy file...Please wait a half minite.")
poscar_folder_path_list = np.load(args[1], allow_pickle=True)
print("poscar_folder_path_list was loaded from .npy file!!!")
print(f"len(poscar_folder_path_list): {len(poscar_folder_path_list)}")
# casting PosixPath to str
poscar_folder_path_list = [str(p) for p in poscar_folder_path_list]
# get poscar2nnlist abs path
cwd = os.getcwd()
poscar2nnlist_abs_path = cwd + '/neib_code/poscar2nnlist'
# get poscar2nnlist 2nd arg
inputted_distance = input("Input a number which is poscar2nnlist's second arg. :nearest neighbors distance(Å) you want to catch: ")


# poscar2nnlist = input()
def cd_dir_and_pos2nnlist(poscar_folder_path):
    # 1. Change current dir to dir that exists a POSCAR file
    os.chdir(poscar_folder_path)
    # 2. make folder for POSCAR.nnlist
    poscar_nnlist_folder_p = poscar_folder_path + '/nnlist_' + inputted_distance
    os.makedirs(poscar_nnlist_folder_p)
    # 3. Run poscar2nnlist
    with open(poscar_nnlist_folder_p + '/poscar2nnlist_log.txt', mode='w') as f:
        cp = subprocess.run([poscar2nnlist_abs_path, 'POSCAR', inputted_distance],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,)
        print(cp.stdout, file=f)
    # 4. move POSCAR.nnlist from cwd to sub-cwd(: current working directory)
    poscar_nnlist_p = poscar_folder_path + '/POSCAR.nnlist'
    shutil.move(poscar_nnlist_p, poscar_nnlist_folder_p)


before = time.time()
try:
    p = Pool(cpu_count() - 1)
    print("Now poscar2nnlist is making POSCAR.nnlist from POSCAR!!!")
    list(tqdm(p.imap(cd_dir_and_pos2nnlist, poscar_folder_path_list[0:3]), total=len(poscar_folder_path_list)))
finally:
    p.close()
    p.join()
after = time.time()
print(f"it took {after - before}sec.")
