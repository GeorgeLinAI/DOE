# -*- coding: utf-8 -*-

"""
林大神的實驗設計, DOE 的基本物件
Version 0.1 2026/05/09 我一定是瘋了…哈哈哈…
"""

import streamlit as st
import pandas as pd
import numpy as np
import DOE

# 設定網頁標題與佈局
st.set_page_config(page_title="DoE 實驗設計產生器", layout="wide")

# st.title("🧪 實驗設計 (DoE) 互動產生器",)
st.markdown("<h2 style='text-align: center; color: red;'>🧪 實驗設計 (DoE) 互動產生器</h2>", unsafe_allow_html=True)
st.markdown("根據輸入因子自動產生 **Resolution IV (或以上)** 的二水準正交實驗表。")

# --- 初始化 Session State ---
if 'factor_data' not in st.session_state:
    st.session_state.factor_data = []

# --- 佈局設定：左、中、右 ---
left_col, mid_col= st.columns([1, 2], gap="large")

# 設定 error message
error_messages = ''

def build_sheet(n_factors, n_responses, factor_configs):
    factor_df = DOE.build_factorial(n_factors)
    error_messages, f_names, f_mins, f_maxs = DOE.check_factor(n_factors, factor_configs)
    factor_df = DOE.assign_values(factor_df, f_names, f_mins, f_maxs)
    df = DOE.build_final_sheet(factor_df, n_factors, n_responses)
    return error_messages, df
    

# ==========================================
# 左邊部分：設定
# ==========================================
with left_col:
    st.header("⚙️ 參數設定")
    n_responses = st.number_input("1. 目標值數量", min_value=1, max_value=5, value=1)
    n_factors = st.number_input("2. 因子數量", min_value=2, max_value=15, value=5)
    
    st.write("3. 定義因子名稱與範圍")
    factor_configs = []
    # 先產生一個 default 的因子表
    for i in range(n_factors):
        with st.expander(f"因子 {i+1} 設定", expanded=(i < 3)):
            col_name, col_min, col_max = st.columns([2, 1, 1])
            name = col_name.text_input(f"名稱", value=f"因子_{i+1}", key=f"n_{i}")
            min_val = col_min.number_input(f"小值", value=-1.0, key=f"min_{i}")
            max_val = col_max.number_input(f"大值", value=1.0, key=f"max_{i}")
            factor_configs.append({"Name": name, "Min": min_val, "Max": max_val})

    # print(factor_configs)

# ==========================================
# 中間部分：結果產出 (邏輯計算)
# ==========================================
with mid_col:

    error_messages, df = build_sheet(n_factors, n_responses, factor_configs)
        
    if error_messages !='':
        st.markdown(error_messages)

    edited_df = st.data_editor(df, disabled=["std_order","run_order",], hide_index=True)




