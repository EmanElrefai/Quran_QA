import pandas as pd
from sklearn.model_selection import KFold
import numpy as np

import os

ensemble_datasets_path = "./datasets/ensemble_datasets/"
combined_data_path = './/datasets//combined_data.csv'

def read():
    Training_datadf = pd.read_csv(combined_data_path )
    return Training_datadf


def K_fold_split_data(Training_datadf):
    kf = KFold(n_splits=8)
    KFold(n_splits=8, random_state=None, shuffle=False)
    index = 0
    for train_index, test_index in kf.split(Training_datadf):
        df = Training_datadf.drop(test_index)
        file_name = 'data_part'+str(index)+'.csv'
        df.to_csv(ensemble_datasets_path+file_name, index=False, encoding='utf-8-sig')
        index = index+1


def main():
    Training_datadf = read()
    K_fold_split_data(Training_datadf)


if __name__ == "__main__":
    main()
