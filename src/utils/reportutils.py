import os
import pandas as pd
import numpy as np

def get_positives_subsets(data: list):
    """
    Get subsets of positive numbers from the input list.
    
    Parameters:
        data (list): List of numbers.
    
    Returns:
        list: List of subsets containing only positive numbers.
    """
    subsets = []
    current_subset = []
    starIndex = endIndex = 0

    for i, num in enumerate(data):
        if num > 0.2:
            if current_subset == []:
                starIndex = i
            current_subset.append(num)
        else:
            if current_subset:
                endIndex = i - 1
                subsets.append( (current_subset, starIndex, endIndex) )
                current_subset = []
    
    if current_subset:
        subsets.append( (current_subset, starIndex, endIndex) )
    
    return subsets

def generateAnnotationDataFrame(data):
    subset_list = get_positives_subsets(data)

    df = pd.DataFrame(columns=['Selection', 'Begin Time (s)', 'End Time (s)', 'Low Freq (Hz)', 'High Freq (Hz)', 'Call Type', 'Score', 'Rating'])
    df_list = []
    for i, subset in enumerate(subset_list):
        avg_score = np.mean(subset[0])
        rating = 'A' if avg_score > 0.8 else ('B' if avg_score > 0.7 else ('C' if avg_score > 0.6 else ('D' if avg_score > 0.4 else 'E')))

        mid = (subset[1] + subset[2]) / 2

        begin_t = mid * 0.05
        duration = max( min((subset[2] - subset[1]) * 0.05, 0.45), 0.3)
        end_t = begin_t + duration

        begin_t = float(int(begin_t * 100) / 100)
        end_t = float(int(end_t * 100) / 100)
        avg_score = float(int(avg_score * 100) / 100)

        annotation = {
            'Selection': int(i+1),
            'Begin Time (s)': begin_t,
            'End Time (s)': end_t,
            'Low Freq (Hz)': 6500.00,
            'High Freq (Hz)': 12500.00,
            'Call Type': str('CS'),
            'Score': avg_score,
            'Rating': str(rating)
        }
        df_list.append(pd.DataFrame(annotation, index=[0]))
    
    if len(df_list) == 0:
        return df
    
    print('Annotation Data:')
    df = pd.concat(df_list, ignore_index=True)
    print(df)
    return df

def readReportData(filename: str):
    """
    Read the report data from the given file.
    
    Parameters:
        filename (str): Name of the file to read the report data from.
    
    Returns:
        pd.DataFrame: The report data.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    
    df = pd.read_csv(filename, sep='\t')
    return df