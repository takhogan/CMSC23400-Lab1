import pandas as pd
import glob
import ast
import os
from sklearn.linear_model import LogisticRegression





def parse_training_data_file(filename):
    filename_split = os.path.splitext(os.path.basename(filename))[0]
    filename_split = filename_split.split('-')
    team_name = filename_split[1]
    activity_name = filename_split[2]
    file_index = filename_split[3]
    with open(filename, 'r') as f:
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
        file_df = file_df.drop(file_df.index[(file_df['time'] < 0.25)])
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
        combined_lab1_df = combined_lab1_df.append(parse_training_data_file(file), ignore_index=True)

    combined_lab1_df.to_csv('combined_lab1_df.csv')

    return combined_lab1_df


def predict_w_model(data, labels=None):
    training_labels = labels
    training_prediction = model.predict_proba(logistic_regression_target[regression_params])

    probability_col_names = ['Driving', 'Jumping', 'Standing', 'Walking']
    probability_predictions = pd.DataFrame(data=training_prediction, columns=probability_col_names)
    data_w_predictions = logistic_regression_target.join(probability_predictions)
    predictions = data_w_predictions.groupby(['activity', 'team', 'file index'])[probability_col_names].mean().idxmax(
        axis=1).reset_index(drop=True).values
    n_mistakes = 0
    for label_index in range(0, training_labels.shape[0]):
        if not (predictions[label_index] == training_labels[label_index]):
            n_mistakes += 1

    print('n_mistakes: ' + str(n_mistakes))
    print('training error: {:02f}'.format(n_mistakes / training_labels.shape[0]))
    print(training_labels)





if __name__=='__main__':
    combined_lab1_df = load_df(reload=False)
    # print(combined_lab1_df)
    training_labels = combined_lab1_df.groupby(['activity', 'team', 'file index']).count().reset_index()['activity']
    regression_params = ['xAccl','yAccl','zAccl','xGyro','yGyro','zGyro']
    combined_lab1_df['time'] = combined_lab1_df['time'].astype('datetime64[s]')
    group_data_by_file = combined_lab1_df.groupby(
        ['activity', 'team', 'file index']
        # pd.Grouper(key='time', freq='10S')
    )
    logistic_regression_target = group_data_by_file.var().reset_index()
    old_df_cols = logistic_regression_target.columns
    variance_col_names = ['activity', 'team', 'file index'] + ['VAR-' + col_name
                                                               for col_name in old_df_cols[3:]]
    logistic_regression_target.rename(mapper={logistic_regression_target.columns[col_index]:variance_col_names[col_index]
                                              for col_index in range(0, logistic_regression_target.shape[1])},
                                      axis=1,
                                      inplace=True)

    median_vals = group_data_by_file.median().reset_index()
    median_col_names = ['activity', 'team', 'file index'] + ['MED-' + col_name
                                                           for col_name in old_df_cols[3:]]

    print(median_col_names)
    exit(0)
    # logistic_regression_target.join()
    print(logistic_regression_target)
    print(group_data_by_file.mean().join())
    exit(0)
    # print(logistic_regression_target.groupby('activity').mean())
    clf = LogisticRegression(multi_class='multinomial')
    model = clf.fit(logistic_regression_target[regression_params], logistic_regression_target['activity'])
    print('finished training')

    predict_w_model(logistic_regression_target[regression_params], labels=training_labels)

