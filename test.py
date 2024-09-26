import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from datetime import datetime
from matplotlib.font_manager import FontProperties
import os

# 讀取 CSV 文件
file_path = os.path.join('整理後_日總收入_UTF8_修正.csv')
data = pd.read_csv(file_path)

# 加載中文字體
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 將 "日期" 列轉換為 datetime 格式
data['日期'] = pd.to_datetime(data['日期'])

# 移除收入為 "Nah" 的數據
data = data[data['收入'] != "Nah"]

# 將 "收入" 列轉換為數值格式
data['收入'] = pd.to_numeric(data['收入'])

# 準備自變數 (X) 和目標變數 (y)
# 這裡將日期轉換為從最早日期的天數來做為 X
data['天數'] = (data['日期'] - data['日期'].min()).dt.days
X = data[['天數']]
y = data['收入']

# 拆分訓練和測試數據集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 構建支持向量回歸 (SVR) 模型
model = SVR(kernel='rbf')  # 使用徑向基核 (RBF kernel)
model.fit(X_train, y_train)

# 訓練集內的預測
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# 計算 R² 和 MSE
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)

print(f"訓練集 R²: {r2_train}")
print(f"測試集 R²: {r2_test}")
print(f"訓練集 MSE: {mse_train}")
print(f"測試集 MSE: {mse_test}")

# 預測未來一年的數據（從 2024-10-01 到 2025-10-31）
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 10, 31)
future_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# 計算未來日期相對於最早日期的天數
future_days = (future_dates - data['日期'].min()).days.values.reshape(-1, 1)

# 使用支持向量回歸模型進行未來的預測
future_forecast = model.predict(future_days)

# 將未來預測結果與日期合併
future_data = pd.DataFrame({'日期': future_dates, '預測收入': future_forecast})

# 繪製圖表
plt.figure(figsize=(10, 6))

# 繪製訓練集的實際收入
plt.plot(data['日期'], data['收入'], label='實際收入', color='blue')

# 繪製訓練集的預測收入
plt.plot(data['日期'].iloc[:len(y_pred_train)], y_pred_train, label='訓練集預測收入', linestyle='--', color='green')

# 繪製測試集的預測收入
plt.plot(data['日期'].iloc[len(y_pred_train):], y_pred_test, label='測試集預測收入', linestyle='--', color='orange')

# 繪製未來預測收入
plt.plot(future_dates, future_forecast, label='未來預測收入', linestyle='--', color='red')

# 圖表標題和標籤，並使用中文字體
plt.title('實際收入與未來預測收入 (SVR)', fontproperties=font_properties, fontsize=16)
plt.xlabel('日期', fontproperties=font_properties, fontsize=12)
plt.ylabel('收入', fontproperties=font_properties, fontsize=12)
plt.legend(prop=font_properties)

# 儲存圖表為 PNG 文件，並應用中文字體
plt.savefig('收入預測_SVR_圖表.png', bbox_inches='tight', dpi=300)

# 顯示圖表
plt.show()

print("圖表已保存為 '收入預測_SVR_圖表.png'")