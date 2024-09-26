import pandas as pd
import numpy as np
import os

# 加載 Excel 文件
file_path = os.path.join('日總收入.xlsx')  # 修改成你的檔案路徑
data = pd.read_excel(file_path, header=None)

# 提取 B2:M32 的數據，對應於 pandas 的 [1:32, 1:13]
extracted_data = data.iloc[1:32, 1:13]  # B2:M32 對應於 [1:32, 1:13]

# 準備日期和天數對應
start_year = 112 + 1911  # 112年 (2023)
start_month = 10  # 開始月份為 10 月
start_day = 1

# 定義每個月份的天數（考慮閏年 113年2月有29天）
days_in_month = {
    10: 31, 11: 30, 12: 31, 1: 31, 2: 29, 3: 31, 4: 30,
    5: 31, 6: 30, 7: 31, 8: 31, 9: 30
}

# 準備一個空列表存儲重新格式化的數據
output_list = []
current_year = start_year
current_month = start_month
day_counter = start_day

# 遍歷每一列和每一行
for col_idx in range(extracted_data.shape[1]):  # 每列對應一個月份
    month = (start_month + col_idx - 1) % 12 + 1
    for row_idx in range(extracted_data.shape[0]):  # 每行對應一個日期
        # 生成對應的日期
        date_str = f"{current_year}-{month:02d}-{day_counter:02d}"
        
        # 提取當前的收入數值
        value = extracted_data.iloc[row_idx, col_idx]
        
        # 如果單元格沒有數據，標記為 "Nah"
        if pd.isna(value):
            value = "Nah"
        
        # 將日期和收入對應加入列表
        output_list.append({
            "日期": date_str,
            "收入": value
        })
        
        # 更新天數
        day_counter += 1
        
        # 如果超過該月的天數，重置天數並進入下一個月
        if day_counter > days_in_month[month]:
            day_counter = 1
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

# 將列表轉換為 DataFrame
output_data = pd.DataFrame(output_list)

# 將結果存儲為 UTF-8 編碼的 CSV 文件
csv_output_path = '整理後_日總收入_UTF8_修正.csv'
output_data.to_csv(csv_output_path, index=False, encoding='utf-8')

print(f"CSV 文件已保存到: {csv_output_path}")
