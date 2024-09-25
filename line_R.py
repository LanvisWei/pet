import pandas as pd
import os
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import seaborn as sns

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

# 定義 X 和 Y
X = csv_data['淨利']  # 目標變數
Y = csv_data[['寵物美容收入', 'Unnamed: 0', '總收入']]  # 自變數 (時間 'Unnamed: 0'、寵物美容收入、總收入)

# 繪製每個自變數與淨利之間的關係圖

# 1. 寵物美容收入 vs 淨利
plt.figure(figsize=(10, 6))
plt.scatter(Y['寵物美容收入'], X, label='寵物美容收入', color='b')
plt.title('寵物美容收入與淨利的關係', fontproperties=font_properties)
plt.xlabel('寵物美容收入', fontproperties=font_properties)
plt.ylabel('淨利', fontproperties=font_properties)
plt.tight_layout()
plt.show()

# 2. 時間 vs 淨利
plt.figure(figsize=(10, 6))
plt.scatter(Y['Unnamed: 0'], X, label='時間', color='g')
plt.title('時間與淨利的關係', fontproperties=font_properties)
plt.xlabel('時間', fontproperties=font_properties)
plt.ylabel('淨利', fontproperties=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.tight_layout()
plt.show()

# 3. 總收入 vs 淨利
plt.figure(figsize=(10, 6))
plt.scatter(Y['總收入'], X, label='總收入', color='r')
plt.title('總收入與淨利的關係', fontproperties=font_properties)
plt.xlabel('總收入', fontproperties=font_properties)
plt.ylabel('淨利', fontproperties=font_properties)
plt.tight_layout()
plt.show()