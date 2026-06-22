import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 設置網頁配置
st.set_page_config(page_title="微積分智慧電能管理系統", layout="wide")

# ==============================================================================
# 🌟 全網頁同步亮暗美化 & 區間色調連動
# ==============================================================================
# 建立側邊欄控制亮度
st.sidebar.header("🛠️ 智慧控能中心")
x_val = st.sidebar.slider("調整手機螢幕亮度 x (%)", 0.0, 100.0, 50.0)

# 選擇操作情境
mode = st.sidebar.radio("選擇操作情境", ("🔋 放電模式 (使用電池)", "🔌 充電模式 (連線快充)"))

# 動態計算背景明暗度
bg_brightness = int(15 + (x_val * 0.4))  # 隨亮度滑動在 15~55 之間微幅變動

# 根據目前所在的區間，給予網頁整體微微的色調回饋
if mode == "🔌 充電模式 (連線快充)":
    if x_val <= 30:
        base_color = f"rgba({bg_brightness}, {bg_brightness+12}, {bg_brightness}, 1)"  # 帶微綠
    elif x_val <= 70:
        base_color = f"rgba({bg_brightness+10}, {bg_brightness+8}, {bg_brightness}, 1)"  # 帶微黃
    else:
        base_color = f"rgba({bg_brightness+15}, {bg_brightness}, {bg_brightness}, 1)"  # 帶微紅
else:
    base_color = f"rgba({bg_brightness}, {bg_brightness+8}, {bg_brightness}, 1)"  # 放電模式維持微綠

# 注入 CSS 讓主畫面與左側側邊欄（Sidebar）同步變色，並優化文字與卡片視覺
st.markdown(f"""
    <style>
    /* 主畫面背景 */
    .stApp {{
        background-color: {base_color} !important;
        transition: background-color 0.4s ease;
    }}
    /* 左側邊欄背景與文字顏色全面同步 */
    [data-testid="stSidebar"] {{
        background-color: {base_color} !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        transition: background-color 0.4s ease;
    }}
    /* 強制側邊欄與主畫面所有文字維持高對比白色 */
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, h1, h2, h3, p, span {{
        color: #ffffff !important;
    }}
    /* 指示文字美化 */
    .metric-container {{
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    </style>
""", unsafe_allow_html=True)

# 標題區
st.title("📱 微積分在智慧型手機雙模式最佳化亮度控制之應用")
st.caption("逢甲大學 微積分(二)期末專題競賽數值工具演示")
st.markdown("---")

# ==============================================================================
# 🔋 模式一：放電模式
# ==============================================================================
if mode == "🔋 放電模式 (使用電池)":
    st.header("🔋 放電模式：邊際耗電率與使用效益分析")
    st.subheader("數學模型：耗電功率二次函數 $P(x) = 0.0008x^2 + 0.02x + 1.5$ (瓦特)")
    
    def P_discharge(x):
        return 0.0008 * x**2 + 0.02 * x + 1.5
    
    def dP_dx(x):
        return 0.0016 * x + 0.02

    current_p = P_discharge(x_val)
    slope = dP_dx(x_val)
    
    x_range = np.linspace(0, 100, 200)
    y_range = P_discharge(x_range)
    tangent_y = slope * (x_range - x_val) + current_p

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_range, name="耗電功率 P(x)", line=dict(color='#2ca02c', width=3)))
    fig.add_trace(go.Scatter(x=x_range, y=tangent_y, name="當前一階導數切線 (斜率)", line=dict(color='#d62728', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=[x_val], y=[current_p], mode='markers+text', name='當前工作點', 
                             marker=dict(size=14, color='#d62728', line=dict(color='white', width=2)),
                             text=[f"  ({x_val}%, {current_p:.2f}W)"], textposition="top left"))
    
    fig.update_layout(
        xaxis=dict(title="螢幕亮度 x (%)", gridcolor='rgba(255,255,255,0.1)', ticksuffix="%"),
        yaxis=dict(title="耗電功率 P (W)", gridcolor='rgba(255,255,255,0.1)', range=[1, 11]),
        paper_bgcolor='rgba(0,0,0,0.4)', plot_bgcolor='rgba(0,0,0,0.4)',
        font=dict(color='white'), legend=dict(x=0.02, y=0.98),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="當前螢幕亮度 (x)", value=f"{x_val} %")
    with col2:
        st.metric(label="當前總耗電功率 P(x)", value=f"{current_p:.3f} W")
    with col3:
        st.metric(label="邊際耗電率 dP/dx (斜率)", value=f"+{slope:.4f} W/%", delta="調亮 1% 增加的瓦數")

    st.info("💡 **微積分工程解釋**：當你滑動亮度，圖形上紅色虛線的**斜率 (一階導數)**會即時變動。斜率越陡峭，代表高亮度下的邊際耗電代價越高。利用動態求導，系統能精準計算出續航力衰減率。當前導數為：")
    st.latex(r"\frac{dP}{dx} = " + f"{slope:.4f} \\text{ W/\%}")

# ==============================================================================
# 🔌 模式二：充電模式
# ==============================================================================
else:
    st.header("🔌 充電模式：結合熱能限制的快充效能最佳化")
    st.subheader("數學模型：充電淨效能函數 $E(x) = 20 \cdot \cos(0.012x) - 0.0006x^2$ (瓦特)")
    st.write("*(此修正模型完美呼應硬體充電的三個階段：高效率區、熱平衡滑落區、過熱保護降速區)*")

    def E_charge(x):
        return 20 * np.cos(0.012 * x) - 0.0006 * x**2
    
    def dE_dx(x):
        return -0.24 * np.sin(0.012 * x) - 0.0012 * x

    current_e = E_charge(x_val)
    slope_e = dE_dx(x_val)

    x_range = np.linspace(0, 100, 200)
    y_range = E_charge(x_range)
    tangent_y = slope_e * (x_range - x_val) + current_e

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_range, name="實質充電效能 E(x)", line=dict(color='#ff7f0e', width=3)))
    fig.add_trace(go.Scatter(x=x_range, y=tangent_y, name="熱效能變化率切線", line=dict(color='#1f77b4', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=[x_val], y=[current_e], mode='markers+text', name='當前工作點', 
                             marker=dict(size=14, color='#1f77b4', line=dict(color='white', width=2)),
                             text=[f"  ({x_val}%, {current_e:.2f}W)"], textposition="bottom left"))
    
    # 🌟 劃分三大核心物理區間 (修正為接受的 'top left' 與 'top right' 參數)
    fig.add_vrect(x0=0, x1=30, fillcolor="green", opacity=0.12, line_width=0, 
                  annotation_text="🟢 1. 最佳高效區", annotation_position="top left")
    
    fig.add_vrect(x0=30, x1=70, fillcolor="yellow", opacity=0.08, line_width=0, 
                  annotation_text="🟡 2. 熱平衡滑落區", annotation_position="top left")
    
    fig.add_vrect(x0=70, x1=100, fillcolor="red", opacity=0.1, line_width=0, 
                  annotation_text="🔴 3. 過熱降速區", annotation_position="top right")

    fig.update_layout(
        xaxis=dict(title="螢幕亮度 x (%)", gridcolor='rgba(255,255,255,0.1)', ticksuffix="%"),
        yaxis=dict(title="淨充電功率 E (W)", gridcolor='rgba(255,255,255,0.1)', range=[-5, 25]),
        paper_bgcolor='rgba(0,0,0,0.4)', plot_bgcolor='rgba(0,0,0,0.4)',
        font=dict(color='white'), legend=dict(x=0.02, y=0.02),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="當前螢幕亮度 (x)", value=f"{x_val} %")
    with col2:
        st.metric(label="實質充電功率 E(x)", value=f"{current_e:.2f} W")
    with col3:
        if x_val <= 30:
            status_text = "🟢 最佳快充狀態"
            color_mode = "normal"
        elif x_val <= 70:
            status_text = "🟡 發熱輕微降速"
            color_mode = "off"
        else:
            status_text = "🔴 觸發過熱保護"
            color_mode = "inverse"
            
        st.metric(label="熱損耗變化率 dE/dx", value=f"{slope_e:.4f} W/%", delta=status_text, delta_color=color_mode)

    st.warning("⚠️ **微積分工程解釋**：在充電模式下，隨著亮度 x 提高，導數轉為**負值**且絕對值越來越大，這在物理上代表**熱能累積造成的降速懲罰**。圖表中的綠色最佳充電區間，正是透過求導找出以下最佳化條件的最高效亮度範圍：")
    st.latex(r"\frac{dE}{dx} \approx 0")
