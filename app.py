import streamlit as st
from streamlit_plotly_events import plotly_events

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px

# グローバル変数の定義
PRIMARY_KEY = 'Id'
TARGET_VARIABLE = ['SalePrice', 'SalePrice_log']

# タイトル
st.title('深掘り分析アプリ')
st.write("1．目的変数との関係性を確認する")

# データの読み込み
df = pd.read_excel('質的変数→量的変数_train.xlsx')
df_rare = pd.read_excel('値ごとの出現頻度(質的変数)と偏差値(量的変数)_train.xlsx')

# 可視化するカラムの選択
df_cols = [None]
df_cols.extend(list(df.columns))

col1, col2, col3, col4 = st.columns(4)
with col1:
    y_col = st.selectbox("目的変数を選択してください", TARGET_VARIABLE)
with col2:
    x_col = st.selectbox("説明変数を選択してください", df.columns)
with col3:
    hue_column = st.selectbox("色分けしたい列を選択してください", df_cols)
with col4:
    is_scatter = st.radio("散布図を表示させますか？",['Yes','No(箱ひげ図が表示)'])

# 目的変数との関係性を表示
if x_col and y_col:
    if is_scatter == 'Yes':
        fig = px.scatter(df, x=x_col, y=y_col, color=hue_column, color_continuous_scale='jet', hover_name=PRIMARY_KEY)
    elif is_scatter == 'No(箱ひげ図が表示)':
        fig = px.box(df, x=x_col, y=y_col, points="all", hover_name=PRIMARY_KEY)
else:
    st.info("目的変数と説明変数を選択してください")

# 散布図をクリックして選択した場合の処理
selected_points = plotly_events(fig)

# クリックされたポイントの情報を表示
if selected_points:
    selected_point = selected_points[0]
    x_val = selected_point['x']
    y_val = selected_point['y']
    id = df[(df[x_col] == x_val) & (df[y_col] == y_val)][PRIMARY_KEY].values[0]

    selected_df = df[df[PRIMARY_KEY]==id]
    selected_df_rare = df_rare[df[PRIMARY_KEY]==id]
    df_c = pd.concat([selected_df, selected_df_rare])

    st.write(f"選択されたポイントの詳細情報: Id={str(int(id))}")
    st.write("質的変数の出現頻度(%)：")
    st.write(df_c.loc[:,:PRIMARY_KEY])
    st.write("量的変数の偏差値：")
    st.write(df_c.loc[:,PRIMARY_KEY:])

else:
    st.info("散布図内の気になるプロットをクリックしてください")

# 1変数の可視化
st.write("2．1変数の分布を確認する")
col5, col6 = st.columns(2)
with col5:
    column = st.selectbox("列を選択してください", df.columns)
with col6:
    chart_type = st.radio("表示するグラフの種類を選択してください", ['histogram','bar'])

if column and chart_type:
        if chart_type == 'histogram':
            fig = px.histogram(df, x=column)
            st.plotly_chart(fig)
        elif chart_type == 'bar':
            fig = px.bar(df, x=column)
            st.plotly_chart(fig)
else:
    st.info("列名とグラフの種類を入力してください")
