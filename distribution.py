import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.font_manager import FontProperties

# 讀取 CSV 文件
file_path = os.path.join('整理後_日總收入_UTF8_修正.csv')  # 請替換成您的實際文件路徑
data = pd.read_csv(file_path)

# 加載中文字體
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 將 '日期' 列轉換為 datetime 格式
data['日期'] = pd.to_datetime(data['日期'])

# 移除收入為 "Nah" 的數據，並將 '收入' 列轉換為數值格式
data = data[data['收入'] != 'Nah']
data['收入'] = pd.to_numeric(data['收入'])

# 繪製常態分佈圖
plt.figure(figsize=(10, 6))
sns.histplot(data['收入'], kde=True, bins=30, color='blue')  # kde=True 表示繪製核密度估計曲線

# 添加標題和標籤
plt.title('收入數據的常態分佈圖', fontsize=16, fontproperties=font_properties)
plt.xlabel('收入', fontsize=12, fontproperties=font_properties)
plt.ylabel('頻率', fontsize=12, fontproperties=font_properties)

# 儲存圖表為 PNG 文件
plt.savefig('收入常態分佈圖.png', bbox_inches='tight', dpi=300)

# 顯示圖表
plt.show()

print("圖表已保存為 '收入常態分佈圖.png'")
