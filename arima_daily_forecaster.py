import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, r2_score
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

# 準備時間序列數據，使用日期作為索引
data.set_index('日期', inplace=True)

# 構建 ARIMA 模型 (p, d, q) = (5, 1, 0)
model = ARIMA(data['收入'], order=(5, 1, 0))
model_fit = model.fit()

# 計算 R² 和 MSE
y_train = data['收入']
y_pred = model_fit.predict(start=0, end=len(y_train)-1, typ='levels')
r2 = r2_score(y_train, y_pred)
mse = mean_squared_error(y_train, y_pred)

print(f"R² (決定係數): {r2}")
print(f"MSE (均方誤差): {mse}")

# 預測未來一年的數據（從 2024-10-01 到 2025-10-31）
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 10, 31)
future_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# 預測未來數據
future_forecast = model_fit.forecast(steps=len(future_dates))

# 將預測結果與未來日期合併
future_data = pd.DataFrame({'日期': future_dates, '預測收入': future_forecast})

# 繪製圖表
plt.figure(figsize=(10, 6))

# 繪製實際數據
plt.plot(data.index, data['收入'], label='實際收入', color='blue')

# 繪製預測數據（訓練集內的預測）
plt.plot(data.index, y_pred, label='訓練集預測收入', linestyle='--', color='green')

# 繪製未來預測數據
plt.plot(future_dates, future_forecast, label='未來預測收入', linestyle='--', color='red')

# 圖表標題和標籤，並使用中文字體
plt.title('實際收入與未來預測收入 (ARIMA)', fontproperties=font_properties, fontsize=16)
plt.xlabel('日期', fontproperties=font_properties, fontsize=12)
plt.ylabel('收入', fontproperties=font_properties, fontsize=12)
plt.legend(prop=font_properties)

# 儲存圖表為 PNG 文件，並應用中文字體
plt.savefig('收入預測_ARIMA_圖表.png', bbox_inches='tight', dpi=300)

# 顯示圖表
plt.show()

print("圖表已保存為 '收入預測_ARIMA_圖表.png'")
