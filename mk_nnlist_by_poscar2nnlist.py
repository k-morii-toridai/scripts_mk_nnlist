import os
import sys
import time
import subprocess
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import numpy as np

# nnlistを作成したいPOSCARファイルの親フォルダリスト（.npy）のパスをコマンドライン引数として受け取る
args = sys.argv

print("Now loading poscar_folder_abs_path_list from .npy file...Please wait a half minite.")
poscar_folder_abs_path_list = np.load(args[1], allow_pickle=True)
print("poscar_folder_abs_path_list was loaded from .npy file!!!")
print(f"len(poscar_folder_abs_path_list): {len(poscar_folder_abs_path_list)}")


inputted_distance = input("Input a number which is poscar2nnlist's second arg. :nearest neighbors distance(Å) you want to catch: ")

# poscar2nnlist = input()
def cd_dir_and_pos2nnlist(poscar_folder_path):
    # 1. Change current dir to dir that exists a POSCAR file
    os.chdir(poscar_folder_path)

    # 2. Run poscar2nnlist
    try:
        subprocess.run(['/mnt/ssd_elecom_black_c2c/ssd_elecom_black_c2c-script/neib_code/poscar2nnlist', 'POSCAR', inputted_distance], stdout=subprocess.DEVNULL)
    except Exception as e:
        pass


before = time.time()
try:
    p = Pool(cpu_count() - 1)
    print("Now poscar2nnlist in making POSCAR.nnlist from POSCAR!!!")
    list(tqdm(p.imap(cd_dir_and_pos2nnlist, poscar_folder_abs_path_list), total=len(poscar_folder_abs_path_list)))
finally:
    p.close()
    p.join()
after = time.time()
print(f"it took {after - before}sec.")
