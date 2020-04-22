import os
import argparse

parser = argparse.ArgumentParser(description='Convert all ht2 in the specified folder recursively')

parser.add_argument('path', metavar='path', type=str,
                    help='base path for conversion',
                    default='.')

args = parser.parse_args()

# Specify the base directory where the script looks for ht2 files recursively
BASE_DIR = args.path

for (directory, dirnames, filenames) in os.walk(BASE_DIR):

    for file_name in filenames:
        
        # check if the file has the ht2 extension
        base_name, ext = os.path.splitext(file_name)
        if ext != '.ht2':
            continue
        
        # convert the file to csv using picoquant. This needs to be installed first
        os.system('picoquant -vi {in_file} -o {out_file}'.format(
            in_file=os.path.join(directory, file_name),
            out_file=os.path.join(directory, base_name+'.csv')))
