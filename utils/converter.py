import os
import argparse
import h5py
import numpy as np
import sys


def convert_ht2(directory, file_base_name):
    """convert the ht2 file to csv using picoquant. Picoquant has to be installed first"""

    os.system('picoquant -vi {in_file} -o {out_file}'.format(
        in_file=os.path.join(directory, file_base_name+'.ht2'),
        out_file=os.path.join(directory, file_base_name+'.csv')))


def convert_mat(directory, file_base_name):
    """convert the matlab mat file to csv"""

    with h5py.File(os.path.join(directory, file_base_name+'.mat'), 'r') as file:

        sync = np.array(file['Sync'][:, 0], dtype=np.uint8)
        time = np.array(file['Time'][:, 0], dtype=np.uint64)

    sync = np.trim_zeros(sync)
    time = np.trim_zeros(time)

    np.savetxt(os.path.join(directory, file_base_name+'.csv'),
               np.transpose([sync, time]), fmt=['%d', '%d'], delimiter=',')

    print('saved {}'.format(os.path.join(directory, file_base_name+'.csv')))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert all ht2 in the specified folder recursively')

    parser.add_argument('path', metavar='path', type=str,
                        help='base path for conversion',
                        default='.')

    parser.add_argument('--format', metavar='-f', type=str, default='ht2',
                        help='specify the input format. possible: ht2, mat')

    args = parser.parse_args()

    # Specify the base directory where the script looks for ht2 files recursively
    BASE_DIR = args.path

    for (directory, dirnames, filenames) in os.walk(BASE_DIR):

        for file_name in filenames:

            # check if the file has the ht2 extension
            base_name, ext = os.path.splitext(file_name)

            if ext == '.ht2' and args.format == 'ht2':
                convert_ht2(directory, base_name)

            if ext == '.mat' and args.format == 'mat':
                convert_mat(directory, base_name)
