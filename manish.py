import os
import glob
import pandas as pd

def load_data(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    df_list = []
    for file in files:
        city_name = os.path.splitext(os.path.basename(file))[0] 
        temp = pd.read_csv(file)
        temp["location"] = city_name.capitalize()   
        if "Unnamed: 0" in temp.columns:
            temp = temp.drop(columns=["Unnamed: 0"])
        df_list.append(temp)
    return pd.concat(df_list, ignore_index=True)
