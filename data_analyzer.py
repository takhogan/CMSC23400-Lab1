import pandas as pd
import glob
import ast

driving_files = glob.glob('traindata_lab1/*-Driving-[0-9]*.txt')

jumping_files = glob.glob('traindata_lab1/*-Jumping-[0-9]*.txt')

standing_files = glob.glob('traindata_lab1/*-Standing-[0-9]*.txt')

walking_files = glob.glob('traindata_lab1/*-Walking-[0-9]*.txt')

# print(list(set(glob.glob('traindata_lab1/*.txt')) - set(driving_files + jumping_files + standing_files + walking_files)))

for file in driving_files:
    with open(file, 'r') as f:
        print(ast.literal_eval(f.read())['seq'])
        # for line in f:
        #     print(line)
    exit(0)
