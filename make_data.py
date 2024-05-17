from pathlib import Path
import tqdm

import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pandas as pd
import numpy as np
import math

# カテゴリ変数と量的変数に分ける
def separate_categorical_and_numerical_columns(df):
    numerical_cols = []
    categorical_cols = []

    threshold = len(df) * 0.02
    print(f'今回のしきい値は{str(threshold)}です。')

    for col in df.columns:
        df_ex = df[col].drop_duplicates()
        if len(df_ex) > threshold:
            numerical_cols.append(col)
        elif len(df_ex) <= threshold:
            categorical_cols.append(col)

    return categorical_cols, numerical_cols

# 表データの各値のレア度を計算する(量的変数：偏差値、質的変数：出現確率)
def calc_rarelity_of_values(df, categorical_cols, numerical_cols):
    df_rare = pd.DataFrame(index=df.index)

    total_count = len(df)
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        probability_dict = (value_counts / total_count * 100).to_dict() # カテゴリ変数：出現確率の辞書を作成
        df_rare[col] = df[col].map(probability_dict)

    for col in numerical_cols:
        mean_val = df[col].mean()
        std_val = df[col].std()
        df_rare[col] = df[col].apply(lambda x:((x - mean_val)/std_val) * 10 + 50)

    return df_rare

# 列ごとに表記ゆれと欠損率を把握する
def check_notation_distortion_and_missing_rate(df):
    df_check = pd.DataFrame()

    # 名列の種と出現回数·出現手を取得して新しいデータフレームに追加する
    total_count = len(df)

    for col in tqdm.tqdm(df.columns):
        # 列ごとの値の出現回数を算出、データフレームで吐き出す
        value_counts = df[col].value_counts()

        value_list = ['(欠損)']
        value_list.extend(value_counts.index.tolist())

        count_list =[total_count - sum(value_counts.values.tolist())]
        count_list.extend(value_counts.values.tolist())

        _df = pd.DataFrame({
            f'{col}_値': value_list,
            f'{col}_出現回数': count_list,
            f'{col}_出現率(%)': [(count / total_count * 100) for count in count_list],
            })
        
        df_check = pd.concat([df_check, _df], axis=1)

    return df_check

if __name__ == '__main__':
    # データの読み込み
    file = Path('data/train.csv')

    df = pd.read_csv(file,encoding='utf-8')
    df['SalePrice_log'] = np.log(df['SalePrice'])

    categorical_cols, numerical_cols = separate_categorical_and_numerical_columns(df)
    print('質的変数：',categorical_cols)
    print('量的変数：',numerical_cols)

    df_rare = calc_rarelity_of_values(df, categorical_cols, numerical_cols)
    # df_check = check_notation_distortion_and_missing_rate(df)

    df_rare.to_excel(f'値ごとの出現頻度(質的変数)と偏差値(量的変数)_{file.stem}.xlsx', index=False)
    # df_check.to_excel(f'表記ゆれと欠損率_{file.stem}.xlsx', index=False)

    categorical_cols.extend(numerical_cols)
    print(categorical_cols)
    df = df[categorical_cols]
    df.to_excel(f'質的変数→量的変数_{file.stem}.xlsx', index=False)