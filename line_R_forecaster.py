import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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

# 訓練線性回歸模型
X = np.arange(len(csv_data)).reshape(-1, 1)  # 用索引值作為自變數
y = csv_data['淨利'].values  # 目標變數

model = LinearRegression()
model.fit(X, y)

# 預測未來一年（2024年9月到2025年9月，假設12個月的預測）
future_months = pd.date_range(start='2024-09-01', periods=12, freq='MS')
future_X = np.arange(len(csv_data), len(csv_data) + 12).reshape(-1, 1)
future_predictions = model.predict(future_X)

# 將日期和預測值合併到 DataFrame 中
future_data = pd.DataFrame({'Unnamed: 0': future_months, '淨利': future_predictions})

# 繪製實際數據
plt.figure(figsize=(10, 6))
plt.plot(csv_data['Unnamed: 0'], csv_data['淨利'], label='實際數據', color='b')

# 繪製預測數據
plt.plot(future_data['Unnamed: 0'], future_data['淨利'], label='預測數據', linestyle='--', color='r')

# 設置圖表標題和標籤，並應用字型
plt.title('淨利隨時間變化的折線圖（含未來一年預測）', fontproperties=font_properties)
plt.xlabel('時間', fontproperties=font_properties)
plt.ylabel('淨利', fontproperties=font_properties)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', prop=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)
plt.tight_layout()

# 顯示圖表
plt.show()
