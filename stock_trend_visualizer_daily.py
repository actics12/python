#開発環境

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import japanize_matplotlib

delta_day = st.sidebar.number_input("表示期間", value=15)

st.sidebar.caption('VDC : 生活必需品セクター\n景気が弱く金利が低い不況期に買われやすい。安定感あり。')
st.sidebar.caption('VDE : エネルギーセクター\nバリュー株多い。値動きに注意。')
st.sidebar.caption('VFH : 金融セクター\n景気が強く金利が低い回復期に買われやすい。短期投資向け。')
st.sidebar.caption('VHT : ヘルスケアセクター\n近年はVTIを上回る。期待大。')
st.sidebar.caption('VDC : 一般消費財セクター\n景気変動に敏感。グロース株多い。')
st.sidebar.caption('VCR : 生活必需品セクター\n景気が弱く金利が低い不況期に買われやすい。安定感あり。')


tickers = ['VDC', 'VDE', 'VFH', 'VHT', 'VCR', 'VTI']

fig, ax = plt.subplots(2, 3, figsize=(12, 8), sharex=True)

for i, ticker in enumerate(tickers):
    df = pd.read_excel(f"C:/Users/actic/OneDrive/10_株式投資/python_本番環境/株DF更新/{ticker}_Stock_Price_Data.xlsx")
    df = df[delta_day* -1:]


    row = i // 3
    col = i % 3

    ax[row, col].plot(df['Date'], df['Close'])
    ax[row, col].plot(df['Date'], df['SMA_short'], label='SMA_short')
    ax[row, col].plot(df['Date'], df['SMA_long'], label='SMA_long')
    ax[row, col].set_title(ticker)
    ax[row, col].legend(loc='upper left')
    ax[row, col].axes.xaxis.set_visible(False)

st.pyplot(fig)