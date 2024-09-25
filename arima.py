import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from matplotlib.font_manager import FontProperties
import os

# Load the CSV file
file_path = os.path.join('PET2_utf8.csv')
csv_data = pd.read_csv(file_path)

# Load the custom font (ChocolateClassicalSans or any other font supporting Chinese characters)
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 定義日期轉換函數 (民國年轉西曆年)
def convert_roc_to_ad(date_str):
    try:
        year, month = date_str.split('年')
        year = int(year) + 1911  # 將民國年轉換為西曆年
        month = month.replace('月', '')  # 去掉 '月'
        return f"{year}-{month}-01"
    except ValueError:
        return None

# 將日期進行轉換
csv_data['Unnamed: 0'] = csv_data['Unnamed: 0'].apply(convert_roc_to_ad)

# 移除無法解析的日期
csv_data = csv_data.dropna(subset=['Unnamed: 0'])

# 將轉換後的日期列轉換為 datetime 格式
csv_data['Unnamed: 0'] = pd.to_datetime(csv_data['Unnamed: 0'], format='%Y-%m-%d')

# 設置日期為索引
csv_data.set_index('Unnamed: 0', inplace=True)

# 準備要使用的淨利數據
profit_data = csv_data['淨利']

# 構建 ARIMA 模型，這裡使用 (p, d, q) = (1, 1, 1) 進行初步建模
model = ARIMA(profit_data, order=(1, 1, 1))
model_fit = model.fit()

# 預測未來一年（12 個月）的數據
forecast_steps = 12
forecast = model_fit.forecast(steps=forecast_steps)

# 生成 2024年9月 到 2025年9月 的日期
future_dates = pd.date_range(start='2024-09-01', periods=forecast_steps, freq='MS')

# 將預測值與日期進行合併
forecast_data = pd.DataFrame({'日期': future_dates, '預測淨利': forecast})

# 繪製實際數據和預測數據
plt.figure(figsize=(10, 6))

# 繪製實際淨利數據
plt.plot(profit_data.index, profit_data, label='實際淨利', color='b')

# 繪製預測淨利數據
plt.plot(future_dates, forecast, label='預測淨利', linestyle='--', color='r')

# 設置圖表標題和標籤，並應用字型
plt.title('淨利隨時間變化的折線圖（含未來一年預測）', fontproperties=font_properties)
plt.xlabel('時間', fontproperties=font_properties)
plt.ylabel('淨利', fontproperties=font_properties)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', prop=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)
plt.tight_layout()

output_path = 'arima.png'
plt.savefig(output_path, format='png', bbox_inches='tight')

# 顯示圖表
plt.show()
