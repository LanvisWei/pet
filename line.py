import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.font_manager import FontProperties

# Load the CSV file
file_path = os.path.join('PET2_utf8.csv')
csv_data = pd.read_csv(file_path)

# Load the custom font (ChocolateClassicalSans or any other font supporting Chinese characters)
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 定義要繪製的特徵欄位
columns_to_plot = ['寵物美容收入', '寵物美容支出', '寵物用品銷售收入', '寵物用品銷售支出', '寵物安親住宿收入', 
                   '寵物安親住宿支出', '企業合作寵物用品銷售收入', '企業合作寵物用品銷售支出', '總收入', '總支出', '淨利']

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

# 繪製每個特徵的折線圖，X軸為 'Unnamed: 0' (時間)
plt.figure(figsize=(10, 6))

for col in columns_to_plot:
    plt.plot(csv_data['Unnamed: 0'], csv_data[col], label=col)

# 設置圖表標題和標籤，並應用字型
plt.title('各特徵隨時間變化的折線圖', fontproperties=font_properties)
plt.xlabel('時間', fontproperties=font_properties)
plt.ylabel('數值', fontproperties=font_properties)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', prop=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)
plt.tight_layout()

output_path = 'line.png'
plt.savefig(output_path, format='png', bbox_inches='tight')
# 顯示圖表
plt.show()
