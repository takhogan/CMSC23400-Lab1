import pandas as pd
import glob
import ast
import os


def parse_data_file(filename):
    filename = os.path.splitext(os.path.basename(filename))[0]
    filename = filename.split('-')
    team_name = filename[1]
    activity_name = filename[2]
    file_index = filename[3]
    with open(file, 'r') as f:
        file_data_dict = ast.literal_eval(f.read())['seq']
        file_timestamps = [{'time': data_point['time']} for data_point in file_data_dict]
        file_data = [{key: value for key, value in data_point['data'].items()} for data_point in file_data_dict]
        for (timestamp, data_point) in zip(file_timestamps, file_data):
            timestamp.update(data_point)
        file_data_flat = file_timestamps
        file_df = pd.DataFrame.from_dict(file_data_flat)
        file_df['time'] -= file_df.loc[file_df.index[0], 'time']
        file_df['team'] = team_name
        file_df['activity'] = activity_name
        file_df['file index'] = file_index
    return file_df


def load_df(reload=True):
    if not reload:
        return pd.read_csv('combined_lab1_df.csv', index_col=0)

    driving_files = glob.glob('traindata_lab1/*-Driving-[0-9]*.txt')

    jumping_files = glob.glob('traindata_lab1/*-Jumping-[0-9]*.txt')

    standing_files = glob.glob('traindata_lab1/*-Standing-[0-9]*.txt')

    walking_files = glob.glob('traindata_lab1/*-Walking-[0-9]*.txt')

    combined_lab1_df = pd.DataFrame()
    for file in driving_files + jumping_files + standing_files + walking_files:
        print(file)
        combined_lab1_df = combined_lab1_df.append(parse_data_file(file), ignore_index=True)

    combined_lab1_df.to_csv('combined_lab1_df.csv')

    return combined_lab1_df


if __name__=='__main__':
    combined_lab1_df = load_df(reload=False)
    print(combined_lab1_df)