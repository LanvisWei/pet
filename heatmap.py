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

# 特徵欄位
columns_to_convert = ['寵物美容收入', '寵物美容支出', '寵物用品銷售收入', '寵物用品銷售支出', '寵物安親住宿收入', 
                      '寵物安親住宿支出', '企業合作寵物用品銷售收入', '企業合作寵物用品銷售支出', '交通費支出', 
                      '課程收入', '課程支出', '課程營所稅支出', '營所稅支出', '寄賣收入', '寄賣支出', '開辦支出', 
                      '總收入', '總支出', '淨利']

# 將特徵欄位轉換為數值型，無法轉換的則變為 NaN
for col in columns_to_convert:
    csv_data[col] = pd.to_numeric(csv_data[col], errors='coerce')

# 選擇數值型欄位，忽略字串型欄位
numeric_data = csv_data[columns_to_convert]

# Calculate the correlation matrix for numeric data
correlation_matrix = numeric_data.corr()

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Draw the heatmap
ax = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

# 設置 x 軸和 y 軸標籤字型
ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_properties, rotation=45, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_properties, rotation=0)

# Add a title with the custom font
plt.title('數值項目的相關性熱力圖', fontproperties=font_properties)

output_path = 'heatmp.png'
plt.savefig(output_path, format='png', bbox_inches='tight')

# Show the plot
plt.tight_layout()
plt.show()
