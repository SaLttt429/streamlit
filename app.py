import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 設置 UI 和 Slider
st.title("微積分專題：智慧亮度控制")
mode = st.radio("選擇模式", ("放電模式", "充電模式"))
x_val = st.slider("螢幕亮度 (x)", 0.0, 100.0, 50.0) # 此 Slider 會即時更新 x_val

# 2. 定義數學模型 (例如：二次函數 P = 0.005*x^2 + 0.1*x + 1)
def power_func(x):
    return 0.005 * x**2 + 0.1 * x + 1
def derivative_func(x): # 微分 P' = 0.01*x + 0.1
    return 0.01 * x + 0.1

# 3. 計算即時數據
current_p = power_func(x_val)
current_slope = derivative_func(x_val)

# 4. 繪製圖形
x_range = np.linspace(0, 100, 200)
fig = go.Figure()
# 繪製耗電曲線
fig.add_trace(go.Scatter(x=x_range, y=power_func(x_range), name="耗電曲線"))
# 繪製切線
tangent_line = current_slope * (x_range - x_val) + current_p
fig.add_trace(go.Scatter(x=x_range, y=tangent_line, name="切線 (導數)", line=dict(dash='dash')))

st.plotly_chart(fig)
st.write(f"當前亮度: {x_val}%，邊際耗電率 P'(x): {current_slope:.2f}")
