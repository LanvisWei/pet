import pandas as pd
import os

# 讀取 CSV 文件
file_path = os.path.join('整理後_日總收入_UTF8_修正.csv')  # 請替換成您的實際文件路徑
data = pd.read_csv(file_path)

# 將 '日期' 列轉換為 datetime 格式
data['日期'] = pd.to_datetime(data['日期'])

# 移除收入為 "Nah" 的數據，並將 '收入' 列轉換為數值格式
data = data[data['收入'] != 'Nah']
data['收入'] = pd.to_numeric(data['收入'])

# 提取日期是星期幾 (0 = 星期一, 6 = 星期日)
data['星期'] = data['日期'].dt.dayofweek

# 按星期分組，並計算每個星期的平均收入
weekly_revenue = data.groupby('星期')['收入'].mean().reset_index()

# 將數字與實際的星期對應 (0 = 星期一, 6 = 星期日)
days_mapping = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
weekly_revenue['星期'] = weekly_revenue['星期'].map(days_mapping)

# 按平均收入排序，找到平均收入最高的星期
weekly_revenue = weekly_revenue.sort_values(by='收入', ascending=False)

# 輸出結果
print(weekly_revenue)

# 如果需要將結果保存為 CSV 文件，可以取消以下註釋：
# weekly_revenue.to_csv('周平均收入統計.csv', index=False, encoding='utf-8')
