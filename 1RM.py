import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="1RM 運動科學預測系統", layout="wide")

# 設定標題與說明
st.title("🏋️ 1RM 多元迴歸預測與訓練區間報告")
st.markdown("本系統基於 **IMTP (N)** 與 **SMI (kg/m²)** 之多元線性迴歸模型")
st.warning("⚠️ **預測適用限制**：本模型建模時，臥推與深蹲皆限制於**肘關節與膝關節 90 度**即向上推起。若低於或超過此角度，預測準確度將受影響。")
st.markdown("---")

# --- 側邊欄：研究背景與設定 ---
with st.sidebar:
    st.header("⚙️ 系統設定")
    low_val = st.number_input("中等強度起始值 (N)", value=2300)
    high_val = st.number_input("優秀強度起始值 (N)", value=2800)
    
    st.divider()
    st.header("🎓 學術資訊")
    st.markdown("**開發者：** 張文彥 & 王重凱")
    st.markdown("**指導教授：** 何承訓 博士")
    st.markdown("**研究機構：**")
    st.info("國立中正大學\n運動生化實驗室")
    
    st.divider()
    st.caption("© 2026 National Chung Cheng University. All rights reserved.")

# 2. 主要版面配置
col_input, col_result = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("📝 數據輸入")
    name = st.text_input("受試者姓名", value="受試者 A")
    test_date = st.date_input("測試日期", value=datetime.now())
    
    st.divider()
    
    # 數據輸入欄位
    imtp_value = st.number_input("IMTP 峰值發力 (N)", min_value=0.0, value=3000.0, step=100.0)
    
    c1, c2 = st.columns(2)
    with c1:
        height_cm = st.number_input("身高 (cm)", min_value=100.0, max_value=250.0, value=170.0)
    with c2:
        smm_kg = st.number_input("骨骼肌肉量 (kg)", min_value=0.0, value=30.0, help="請輸入骨骼肌重量 (Skeletal Muscle Mass)")
    
    # 自動計算 SMI
    height_m = height_cm / 100
    smi_calc = smm_kg / (height_m ** 2)
    st.success(f"系統換算 SMI：**{smi_calc:.2f}** kg/m²")
        
    predict_btn = st.button("🚀 生成三項綜合預測報告", use_container_width=True)

with col_result:
    if predict_btn:
        # 迴歸公式計算
        pred_sq = max(0.0, -16.379 + (0.038 * imtp_value) + (8.524 * smi_calc))
        pred_bp = max(0.0, -59.761 + (0.014 * imtp_value) + (9.358 * smi_calc))
        pred_dl = max(0.0, -62.803 + (0.024 * imtp_value) + (14.047 * smi_calc))

        # --- 顯示報告抬頭 ---
        st.subheader(f"📊 綜合預測報告：{name}")
        st.write(f"**檢測日期：** {test_date}")
        
        # --- 一次輸出三種預測 ---
        m1, m2, m3 = st.columns(3)
        m1.metric(label="深蹲 (SQ) 預估 1RM", value=f"{round(pred_sq, 1)} kg")
        m2.metric(label="臥推 (BP) 預估 1RM", value=f"{round(pred_bp, 1)} kg")
        m3.metric(label="硬舉 (DL) 預估 1RM", value=f"{round(pred_dl, 1)} kg")
        
        st.divider()

        # --- 綜合訓練強度區間表 (更新肌肥大區間為 6-12RM) ---
        st.write("### 📋 建議訓練重量參考 (RM)")
        
        intensity_data = {
            "訓練目標 (RM)": ["最大肌力 (1RM)", "爆發/力量 (3-5RM)", "肌肥大區間 (6-12RM)", "肌耐力 (15RM+)"],
            "強度百分比": ["100%", "85-90%", "70-85%", "< 65%"],
            "深蹲 SQ (kg)": [
                f"{round(pred_sq, 1)}", 
                f"{round(pred_sq*0.85, 1)} - {round(pred_sq*0.9, 1)}", 
                f"{round(pred_sq*0.7, 1)} - {round(pred_sq*0.85, 1)}", 
                f"<{round(pred_sq*0.65, 1)}"
            ],
            "臥推 BP (kg)": [
                f"{round(pred_bp, 1)}", 
                f"{round(pred_bp*0.85, 1)} - {round(pred_bp*0.9, 1)}", 
                f"{round(pred_bp*0.7, 1)} - {round(pred_bp*0.85, 1)}", 
                f"<{round(pred_bp*0.65, 1)}"
            ],
            "硬舉 DL (kg)": [
                f"{round(pred_dl, 1)}", 
                f"{round(pred_dl*0.85, 1)} - {round(pred_dl*0.9, 1)}", 
                f"{round(pred_dl*0.7, 1)} - {round(pred_dl*0.85, 1)}", 
                f"<{round(pred_dl*0.65, 1)}"
            ]
        }
        
        st.table(pd.DataFrame(intensity_data))

        # --- IMTP 發力評級 ---
        st.write(f"**IMTP 數據分析 (發力值: {imtp_value} N)**")
        if imtp_value < low_val:
            st.error("Level : Below Average")
        elif imtp_value < high_val:
            st.warning("Level：Average")
        else:
            st.success("Level：Elite")
            
        st.progress(min(1.0, imtp_value / 6000.0))
        st.caption("註：肌肥大區間 (6-12RM) 是依據運動科學建議之強度範圍。預測值僅限於關節角度 90 度之規範動作。")
    else:
        st.info("請在左側輸入 IMTP、身高與骨骼肌肉量，系統將即時生成三項 1RM 預測報告。")
