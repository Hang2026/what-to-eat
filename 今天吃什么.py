import streamlit as st
import random
import pandas as pd
import os
from datetime import datetime
# 设置页面配置
st.set_page_config(page_title="今天吃什么", page_icon="🍜", layout="centered")
# 标题
st.title("🍜 今天吃什么")
st.markdown("---")
# 多选框
default_options = ["三文鱼", "沙拉", "牛肉饭", "麦当劳"]
options = st.multiselect(
    "请选择想吃的选项：",
    options=default_options,
    default=default_options
)

# 大按钮
if st.button("🎲 帮我决定", use_container_width=True, type="primary"):
    if options:
        # 随机选择一个
        choice = random.choice(options)
        
        # 显示结果（大字体）
        st.success(f"### 今天就吃：**{choice}** 🎉")
        
        # 保存到 CSV
        csv_file = "history.csv"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 创建新记录
        new_record = pd.DataFrame({
            "决定时间": [current_time],
            "决定的结果": [choice]
        })
        
        # 如果文件存在，追加；否则创建新文件
        if os.path.exists(csv_file):
            new_record.to_csv(csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            new_record.to_csv(csv_file, mode='w', header=True, index=False, encoding='utf-8-sig')
    else:
        st.warning("请至少选择一个选项哦！")
# 显示历史记录
st.markdown("---")
st.subheader("📜 最近的吃货记录")
csv_file = "history.csv"
if os.path.exists(csv_file):
    # 读取 CSV 文件
    history_df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    # 显示最近 5 条记录
    if len(history_df) > 0:
        recent_records = history_df.tail(5).iloc[::-1]  # 倒序显示最新的在前
        st.dataframe(recent_records, use_container_width=True, hide_index=True)

        # 统计并展示柱状图
        st.markdown("---")
        st.subheader("📊 吃货统计")
        # 统计每种食物出现的次数
        food_counts = history_df["决定的结果"].value_counts()
        st.bar_chart(food_counts)
    else:
        st.info("还没有记录，快来做第一次决定吧！")
else:
    st.info("还没有记录，快来做第一次决定吧！")
