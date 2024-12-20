import pandas as pd
import datetime
import logging

class make_great_dataset:
    def __init__(self, col_to_drop, key):
        """
        Initializes the make_great_dataset class with columns to drop and key columns.

        Args:
            col_to_drop (list): Columns to drop from the dataset.
            key (list): Key columns to identify unique rows.
        """
        self.col_to_drop = col_to_drop
        self.key = key

    def __call__(self, file_path, col_sum_1, col_sum_2, col_make_sum, col_make_delta=None, col_make_date=None):
        """
        Processes the dataset by dropping specified columns, creating new columns, and removing duplicates.

        Args:
            file_path (str): Path to the CSV file.
            col_sum_1 (str): Column name for the first summand.
            col_sum_2 (str): Column name for the second summand.
            col_make_sum (str): Column name for the sum of col_sum_1 and col_sum_2.
            col_make_delta (str, optional): Column name for calculating delta. Defaults to None.
            col_make_date (str, optional): Column name for creating date. Defaults to None.

        Returns:
            pd.DataFrame: Processed and cleaned dataset.
        """
        data = pd.read_csv(file_path)
        if col_make_sum is not None:
            data[col_make_sum] = data[col_sum_1] + data[col_sum_2]
        data_clean = data.drop(self.col_to_drop, axis=1)
        if col_make_date is not None:
            data_clean[col_make_date] = [datetime.datetime.fromtimestamp(i).strftime('%Y%m%d') for i in data[col_make_date]]
        data_clean_unique = data_clean.drop_duplicates(self.key)
        data_featured = data_clean_unique.reset_index(drop=True)
        logging.debug(f'Data without NA {data_featured.dropna(inplace=True)}')
        return data_featured

    def delta(self, data, col):
        """
        Calculates the delta between consecutive rows for a specified column.

        Args:
            data (pd.DataFrame): DataFrame containing the data.
            col (str): Column name to calculate delta.

        Returns:
            pd.DataFrame : Dataframe containing the data and the calculated col.
        """
        data_n = list(data[col][1:])
        data_n_1 = (data[col][:-1])
        data_delta = []
        data=data.reset_index(drop=True)[1:]
        for i in range(len(data_n)):
            data_delta.append(data_n[i] - data_n_1[i])
        data[f'{col}_delta'] = data_delta
        return data


    def from_data_to_delta_data(data):
        """
        Resets the index of the DataFrame and removes the first row.

        Args:
            data (pd.DataFrame): DataFrame containing the data.

        Returns:
            pd.DataFrame: DataFrame with reset index and first row removed.
        """
        return 

def make_future(df, col_to_increment, to_fit):
    """
    Creates a future DataFrame by incrementing a specified column.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        col_to_increment (str): Column name to increment.
        to_fit (list): List of columns to include in the future DataFrame.

    Returns:
        pd.DataFrame: Future DataFrame with incremented column.
    """
    df_to_pred = pd.DataFrame(df.iloc[-1].copy()).T[to_fit]
    logging.debug(f'DATAFRAME TO PREDICT : {df_to_pred.T}')
    df_to_pred[col_to_increment] += 1
    return df_to_pred