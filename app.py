import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 設置網頁標題與介紹
st.set_page_config(page_title="微積分專題：智慧電能最佳化控制系統", layout="wide")
st.title("📱 微積分在智慧型手機雙模式最佳化亮度控制之應用")
st.caption("逢甲大學 電機一乙 曾宥銓 微積分(二)期末專題競賽數值工具演示")
st.markdown("---")

# 側邊欄：模式切換與環境變數設定
st.sidebar.header("🛠️ 系統參數設定")
mode = st.sidebar.radio("選擇操作模式", ("🔋 放電模式 (使用電池)", "🔌 充電模式 (連線快充)"))

# 共同的輸入：螢幕亮度 Slider
x_val = st.sidebar.slider("調整螢幕亮度 x (%)", 0.0, 100.0, 50.0)

# ==============================================================================
# 模式一：放電模式 (求耗電極小值與導數切線)
# ==============================================================================
if mode == "🔋 放電模式 (使用電池)":
    st.header("🔋 放電模式：邊際耗電率與使用效益分析")
    st.subheader("數學模型：耗電功率二次函數 $P(x) = 0.0008x^2 + 0.02x + 1.5$ (瓦特)")
    
    # 定義函數與導數
    def P_discharge(x):
        return 0.0008 * x**2 + 0.02 * x + 1.5
    
    def dP_dx(x):
        return 0.0016 * x + 0.02

    # 計算當前亮度的數值
    current_p = P_discharge(x_val)
    slope = dP_dx(x_val)
    
    # 建立數據矩陣繪圖
    x_range = np.linspace(0, 100, 200)
    y_range = P_discharge(x_range)
    
    # 計算切線方程式：y - y1 = m(x - x1) -> y = m(x - x1) + y1
    tangent_y = slope * (x_range - x_val) + current_p

    # 繪製圖表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_range, name="耗電功率 P(x)", line=dict(color='#2ca02c', width=3)))
    fig.add_trace(go.Scatter(x=x_range, y=tangent_y, name="當前一階導數切線 (斜率)", line=dict(color='#d62728', dash='dash')))
    fig.add_trace(go.Scatter(x=[x_val], y=[current_p], mode='markers+text', name='當前工作點', 
                             marker=dict(size=12, color='red'), text=[f"({x_val}%, {current_p:.2f}W)"], textposition="top left"))
    
    fig.update_layout(title="螢幕亮度與耗電功率關係圖 (含動態切線)", xaxis_title="螢幕亮度 x (%)", yaxis_title="耗電功率 P (W)",
                      yaxis=dict(range=[1, 11]))
    st.plotly_chart(fig, use_container_width=True)

    # 數據面板
    col1, col2, col3 = st.columns(3)
    col1.metric(label="當前螢幕亮度 (x)", value=f"{x_val} %")
    col2.metric(label="當前總耗電功率 P(x)", value=f"{current_p:.3f} W")
    col3.metric(label="邊際耗電率 dP/dx (斜率)", value=f"+{slope:.4f} W/%", delta="代表調亮1%增加的瓦數")

   st.warning(f"⚠️ 微積分工程解釋：在放電模式（使用電池）下，隨螢幕亮度 $x$ 提高，耗電功率 $P$ 呈二次函數非線性上升。導數 $\\frac{{dP}}{{dx}}$ 代表每增加 $1\%$ 亮度所帶來耗電功率的邊際變動率（斜率）。圖表中的動態切換線與臨界點，正是透過求導尋求找出以下最佳條件的最高效亮度範圍：\n\n $$\n\\frac{{dP}}{{dx}} \\approx 0\n$$")

# ==============================================================================
# 模式二：充電模式 (求最佳充電效能與熱限制極值)
# ==============================================================================
else:
    st.header("🔌 充電模式：結合熱能限制的快充效能最佳化")
    st.subheader("數學模型：充電淨效能函數 $E(x) = 15 \cdot \cos(0.015x) - 0.0005x^2$ (瓦特)")
    st.write("*(此模型考慮了『螢幕調太亮引發手機發熱，導致系統觸發保護機制降低充電功率』的非線性物理特性)*")

    # 定義充電效率函數與偏導函數(對亮度的影響)
    def E_charge(x):
        return 15 * np.cos(0.015 * x) - 0.0005 * x**2
    
    def dE_dx(x):
        # 導數: -15 * 0.015 * sin(0.015x) - 0.001x
        return -0.225 * np.sin(0.015 * x) - 0.001 * x

    current_e = E_charge(x_val)
    slope_e = dE_dx(x_val)

    # 尋找理論極值點 (E'(x) = 0) 的近似位置 (經計算大約在 x = 0 附近為最大值，此處模擬發熱衰減曲線)
    x_range = np.linspace(0, 100, 200)
    y_range = E_charge(x_range)
    tangent_y = slope_e * (x_range - x_val) + current_e

    # 繪製圖表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_range, name="實質充電效能 E(x)", line=dict(color='#ff7f0e', width=3)))
    fig.add_trace(go.Scatter(x=x_range, y=tangent_y, name="熱效能變化率切線", line=dict(color='#1f77b4', dash='dash')))
    fig.add_trace(go.Scatter(x=[x_val], y=[current_e], mode='markers+text', name='當前工作點', 
                             marker=dict(size=12, color='blue'), text=[f"({x_val}%, {current_e:.2f}W)"], textposition="bottom left"))
    
    # 標示出微積分算出的最佳快充綠色區間 (例如亮度在 0%~30% 之間發熱最少，充電最快)
    fig.add_vrect(x0=0, x1=30, fillcolor="green", opacity=0.1, line_width=0, annotation_text="微積分計算：低!")

    fig.update_layout(title="螢幕亮度與實質充電效能關係圖", xaxis_title="螢幕亮度 x (%)", yaxis_title="淨充電功率 E (W)")
    st.plotly_chart(fig, use_container_width=True)

    # 數據面板
    col1, col2, col3 = st.columns(3)
    col1.metric(label="當前螢幕亮度 (x)", value=f"{x_val} %")
    col2.metric(label="實質充電功率 E(x)", value=f"{current_e:.2f} W")
    col3.metric(label="熱損耗變化率 dE/dx", value=f"{slope_e:.4f} W/%", delta="負值代表發熱導致功率正在衰減", delta_color="inverse")

   st.warning(f"⚠️ 微積分工程解釋：在充電模式（插線快充）下，隨著亮度 $x$ 提高，淨充電功率 $E$ 會因為機身發熱而逐步遞減。因此導數 $\\frac{{dE}}{{dx}}$ 皆為負值且絕對值越來越大，這在物理上代表熱能累積造成的降速懲罰。圖表中的綠色最佳充電區間，正是透過求導尋求尋找出以下最佳條件的最高效亮度範圍：\n\n $$\n\\frac{{dE}}{{dx}} \\approx 0\n$$")

