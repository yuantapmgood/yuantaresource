import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# 1. 頁面與視覺設定
# ==========================================
st.set_page_config(page_title="元大證券國金-資源彙整", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans TC', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* 大方塊按鈕樣式 */
    div.stButton > button {
        height: 140px;
        border-radius: 16px;
        border: 2px solid #E5E7EB;
        background-color: white;
        transition: 0.3s;
        margin-bottom: 20px; 
    }
    div.stButton > button p {
        font-size: 26px !important; 
        font-weight: 700 !important;
        color: #002D62; /* 元大藍 */
    }
    div.stButton > button:hover {
        border-color: #002D62;
        background-color: #F0F4F8;
        box-shadow: 0 8px 20px rgba(0, 45, 98, 0.15);
        transform: translateY(-2px);
    }
    
    /* 隱藏預設的側邊欄選單符號 */
    [data-testid="collapsedControl"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 狀態管理與檔案對應表
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = '總覽首頁'

FILE_MAP = {
    'IR 會議公司名單': 'IR會議公司名單.csv',
    '論壇講師': '論壇講師.csv',
    '專家領域': '專家領域.csv',
    '研究資源': '研究資源.csv'
}

DEFAULT_COLUMNS = {
    'IR 會議公司名單': ['市場', '公司', 'Ticker'],
    '論壇講師': ['專家', '曾舉辦議題'],
    '專家領域': ['專家', '內容摘要', '相關標的'],
    '研究資源': ['上手', '資源類型']
}

# ==========================================
# 3. 核心功能：讀取 CSV
# ==========================================
@st.cache_data(ttl=60)
def load_data(category_name):
    filename = FILE_MAP[category_name]
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename, encoding='utf-8-sig')
        except UnicodeDecodeError:
            return pd.read_csv(filename, encoding='cp950')
    else:
        return pd.DataFrame(columns=DEFAULT_COLUMNS[category_name])

# ==========================================
# 4. 側邊欄 (僅顯示返回首頁按鈕)
# ==========================================
with st.sidebar:
    st.title("導覽列")
    if st.session_state.current_page != '總覽首頁':
        if st.button("🏠 返回總覽首頁", use_container_width=True, type="primary"):
            st.session_state.current_page = '總覽首頁'
            st.rerun()
    st.markdown("---")

# ==========================================
# 5. 畫面邏輯 - 總覽首頁
# ==========================================
if st.session_state.current_page == '總覽首頁':
    st.title("🏦 元大證券國金 - 資源總覽")
    st.markdown("---")
    
    # 讀取所有資料庫的數量
    db_counts = {}
    total_records = 0
    for cat in FILE_MAP.keys():
        df_temp = load_data(cat)
        count = len(df_temp)
        db_counts[cat] = count
        total_records += count
    
    # --- 上半部：儀表板 (Gauge Chart) 顯示總資料量 ---
    # 假設目前資料庫最大容量設定為 1000 筆 (你可以依需求調整)
# --- 上半部：儀表板 (Gauge Chart) 顯示總資料量 ---
    # 假設目前資料庫最大容量設定為 1000 筆
    MAX_CAPACITY = 500 
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_records,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "元大總資源量", 'font': {'size': 28, 'family': 'Noto Sans TC', 'color': '#002D62'}},
        gauge = {
            'axis': {
                'range': [None, MAX_CAPACITY], 
                'tickwidth': 2, 
                'tickcolor': "#002D62",
                'tickfont': {'size': 14} # 稍微縮小刻度數字，避免擁擠
            },
            'bar': {'color': "rgba(0,0,0,0)"}, # 隱藏預設的進度條，我們改用指針
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E5E7EB",
            'steps': [
                # 改成單一乾淨的淺藍色背景
                {'range': [0, MAX_CAPACITY], 'color': '#F0F4F8'} 
            ],
            'threshold': {
                # 這裡就是畫出那個「箭頭/指針」的關鍵設定
                'line': {'color': "#002D62", 'width': 8},
                'thickness': 0.75,
                'value': total_records
            }
        }
    ))
    
    fig.update_layout(
        height=380, # 稍微增加高度
        # 調整邊界，特別是左右(l, r)和底部(b)，避免文字被截斷
        margin=dict(t=80, b=40, l=40, r=40), 
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': "Noto Sans TC"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### 🚀 快速進入板塊 (點擊下方方塊)")
    
    # --- 下半部：四大方塊導航 ---
    col1, col2 = st.columns(2)
    categories = list(FILE_MAP.keys())
    
    for i, cat in enumerate(categories):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if st.button(cat, use_container_width=True, key=f"btn_{cat}"):
                st.session_state.current_page = cat
                st.rerun()

# ==========================================
# 6. 畫面邏輯 - 獨立資料庫頁面 (純檢視)
# ==========================================
else:
    selected_category = st.session_state.current_page
    st.title(f"📂 {selected_category}")

    market_filter = None
    if selected_category == "IR 會議公司名單":
        market_filter = st.radio("篩選市場板塊：", ["全部", "美股", "日股", "其他市場"], horizontal=True)

    df = load_data(selected_category)

    if selected_category == "IR 會議公司名單" and market_filter != "全部" and not df.empty:
        if "市場" in df.columns:
            df = df[df["市場"] == market_filter]

    st.markdown("---")
    
    # --- 表格顯示優化：自動換行與調整欄寬 ---
    # 將 Pandas DataFrame 轉換為帶有 CSS 樣式的格式
    styled_df = df.style.set_properties(**{
        'white-space': 'pre-wrap',       # 允許文字自動換行
        'text-align': 'left',            # 文字靠左對齊
        'min-width': '150px'             # 設定欄位最小寬度
    })
    
    # 顯示表格，並取消隱藏 index (因為 styled DataFrame hide_index 參數用法不同)
    st.dataframe(
        styled_df, 
        use_container_width=True, # 讓表格填滿畫面寬度
        height=600                # 給予足夠的高度讓換行的內容可以顯示
    )
