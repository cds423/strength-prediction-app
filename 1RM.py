import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="1RM 運動科學預測系統", layout="wide")

# 設定標題與說明
st.title("🏋️ 1RM 多元迴歸預測與訓練區間報告")
st.markdown("本系統基於 IMTP (N) 與 SMI (kg/m²) 之多元線性迴歸模型")
st.markdown("---")

# --- 側邊欄：常模與進階設定 ---
with st.sidebar:
    st.header("⚙️ 系統設定")
    low_val = st.number_input("中等強度起始值 (N)", value=2500)
    high_val = st.number_input("優秀強度起始值 (N)", value=4500)
    st.divider()
    st.caption("開發者：張大帥")

# 2. 主要版面配置
col_input, col_result = st.columns([1, 1.5], gap="large")

with col_input:
    st.subheader("📝 基本資料與數據輸入")
    
    # 新增：受試者資訊欄位
    name = st.text_input("受試者姓名", value="受試者 A")
    test_date = st.date_input("測試日期", value=datetime.now())
    
    st.divider()
    
    # 數據輸入欄位
    c1, c2 = st.columns(2)
    with c1:
        imtp_value = st.number_input("IMTP 峰值發力 (N)", min_value=0.0, value=3000.0)
    with c2:
        smi_value = st.number_input("SMI 指數 (kg/m²)", min_value=0.0, value=8.5)
        
    exercise = st.selectbox("選擇預測動作", ["硬舉 (DL)", "臥推 (BP)", "深蹲 (SQ)"])
    predict_btn = st.button("🚀 生成預測報告", use_container_width=True)

with col_result:
    if predict_btn:
        # 迴歸公式計算
        if exercise == "硬舉 (DL)":
            prediction = -62.803 + (0.024 * imtp_value) + (14.047 * smi_value)
        elif exercise == "臥推 (BP)":
            prediction = -59.761 + (0.014 * imtp_value) + (9.358 * smi_value)
        elif exercise == "深蹲 (SQ)":
            prediction = -16.379 + (0.038 * imtp_value) + (8.524 * smi_value)

        final_result = max(0.0, prediction)

        # --- 顯示報告抬頭 ---
        st.subheader(f"📊 {exercise} 檢測報告：{name}")
        st.write(f"**檢測日期：** {test_date}")
        
        # 顯示預測數值
        st.metric(label="預估 1RM 重量", value=f"{round(final_result, 1)} kg")
        
        # --- 訓練強度區間表 (依照 NSCA 標準與您的需求) ---
        st.write("### 📋 建議訓練強度區間")
        
        intensity_data = {
            "訓練目標": [
                "Strength", 
                "Hypertrophy", 
                "The lower limit of hypertrophy", 
                "Endurance"
            ],
            "1RM 百分比": ["90%", "85%", "60%", "< 60%"],
            "建議重量 (kg)": [
                f"{round(final_result * 0.9, 1)} kg",
                f"{round(final_result * 0.85, 1)} kg",
                f"{round(final_result * 0.6, 1)} kg",
                f"低於 {round(final_result * 0.6, 1)} kg"
            ]
        }
        
        df_intensity = pd.DataFrame(intensity_data)
        st.table(df_intensity)

        # --- IMTP 發力評級 ---
        st.divider()
        st.write(f"**IMTP 數據分析 (發力值: {imtp_value} N)**")
        
        # 強度判定
        if imtp_value < low_val:
            st.error("level : Below Average")
        elif imtp_value < high_val:
            st.warning("level：Average")
        else:
            st.success("level：Elite")
            
        st.progress(min(1.0, imtp_value / 6000.0))
        st.caption("註：預測公式根據運動科學回歸模型計算，結果僅供訓練參考。")
    else:
        st.info("請在左側輸入受試者資料與數據後，點擊『生成預測報告』按鈕。")