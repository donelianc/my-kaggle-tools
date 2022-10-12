"""Utility functions for the competition"""

import os
import glob
import pandas as pd
import numpy as np


def reduce_mem_usage(data: pd.DataFrame, keep_float16: bool = True) -> pd.DataFrame:
    """
    Author: ArjanGroen
    Source: https://www.kaggle.com/code/arjanso/reducing-dataframe-memory-size-by-65/notebook

    Iterate through all the columns of a dataframe and modify the data type
    to reduce memory usage.

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to reduce the memory usage of.
    keep_float16 : bool
        Whether to keep the float16 data type. If False, float16 will be
        converted to float32.

    Returns
    -------
    pd.DataFrame
        The dataframe with reduced memory usage.
    """

    start_mem = data.memory_usage().sum() / 1024**2
    print(f"Memory usage of dataframe is {start_mem:.2f} MB")

    for col in data.columns:
        col_type = data[col].dtype

        if col_type != object:
            c_min = data[col].min()
            c_max = data[col].max()

            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    data[col] = data[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    data[col] = data[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    data[col] = data[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    data[col] = data[col].astype(np.int64)

            else:
                # adding condition to remove float16
                if keep_float16:
                    if (
                        c_min > np.finfo(np.float16).min
                        and c_max < np.finfo(np.float16).max
                    ):
                        data[col] = data[col].astype(np.float16)
                    elif (
                        c_min > np.finfo(np.float32).min
                        and c_max < np.finfo(np.float32).max
                    ):
                        data[col] = data[col].astype(np.float32)
                    else:
                        data[col] = data[col].astype(np.float64)

                else:
                    if (
                        c_min > np.finfo(np.float16).min
                        and c_max < np.finfo(np.float16).max
                    ):
                        data[col] = data[col].astype(np.float32)
                    elif (
                        c_min > np.finfo(np.float32).min
                        and c_max < np.finfo(np.float32).max
                    ):
                        data[col] = data[col].astype(np.float32)
                    else:
                        data[col] = data[col].astype(np.float64)

        else:
            data[col] = data[col].astype("category")

    end_mem = data.memory_usage().sum() / 1024**2

    print(f"Memory usage after optimization is: {end_mem:.2f} MB")
    print(f"Decreased by {100 * (start_mem - end_mem) / start_mem:.1f}%")

    return data


def import_data(file: str, keep_float16: bool = True) -> pd.DataFrame:
    """
    Author: Ayush Bihani
    Source: https://www.kaggle.com/code/hsuyab/fast-loading-high-compression-with-feather/notebook

    Create a dataframe and optimize its memory usage

    Parameters
    ----------
    file : str
        The path to the file to import.
    keep_float16 : bool
        Whether to keep the float16 data type. If False, float16 will be
        converted to float32.

    Returns
    -------
    pd.DataFrame
        The dataframe with reduced memory usage.
    """

    data = pd.read_csv(file, parse_dates=True, keep_date_col=True)
    data = reduce_mem_usage(data, keep_float16)

    return data


def makedir_check(path: str) -> bool:
    """
    Author: Ayush Bihani
    Source: https://www.kaggle.com/code/hsuyab/fast-loading-high-compression-with-feather/notebook

    Takes path as input and creates a directory if it doesn't exist

    Parameters
    ----------
    path : str
        The path to the directory to create.

    Returns
    -------
    bool
        Whether the directory was created or not.
    """

    exist_dir = os.path.exists(path)

    if exist_dir:
        print("The directory already exists!")
    else:
        os.makedirs(path)
        print(f"The directory, {path}, has been created!")

    return exist_dir


def delete_files(path: str, removal: str = "file") -> None:
    """
    Author: Ayush Bihani
    Source: https://www.kaggle.com/code/hsuyab/fast-loading-high-compression-with-feather/notebook

    Takes path as input and deletes that file

    Parameters
    ----------
    path : str
        The path to the file to delete.
    removal : str
        Whether to delete a file or a directory.

    Returns
    -------
    None
    """

    if removal == "file":
        files = glob.glob(path)

        for file in files:
            os.remove(file)

        print("Files deleted successfully.")

    if removal == "directory":
        os.removedirs(path)

        print("Directory deleted successfully.")
