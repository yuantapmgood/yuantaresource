import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. 頁面與視覺設定
# ==========================================
st.set_page_config(page_title="元大證券國金-資源彙整", page_icon="📈", layout="wide")

# 初始化資料庫
if 'db' not in st.session_state:
    st.session_state['db'] = {
        'IR 會議公司名單': pd.DataFrame([
            {'市場': '美股', '公司代號': 'NVDA', '公司名稱': 'NVIDIA', '會議日期': '2026-05-20', '狀態': '已確認'},
            {'市場': '日股', '公司代號': '7203', '公司名稱': 'Toyota', '會議日期': '2026-05-22', '狀態': '邀請中'},
            {'市場': '其他市場', '公司代號': '2330', '公司名稱': '台積電', '會議日期': '2026-05-15', '狀態': '已確認'},
        ]),
        '論壇講師': pd.DataFrame([
            {'姓名': '王大明', '職位': '首席經濟學家', '機構': '元大投顧', '專長': '總體經濟'},
            {'姓名': '李AI', '職位': '技術總監', '機構': '科技研究院', '專長': '人工智慧'}
        ]),
        '專家領域': pd.DataFrame([
            {'領域名稱': 'AI 伺服器', '專家數量': 12, '熱門程度': 'High'},
            {'領域名稱': '綠能與ESG', '專家數量': 8, '熱門程度': 'Medium'}
        ]),
        '研究資源': pd.DataFrame([
            {'資源標題': '2026 Q3 全球市場展望', '檔案類型': 'PDF', '發布單位': '研究部'},
            {'資源標題': '半導體供應鏈深度解析', '檔案類型': 'Video', '發布單位': '產業組'}
        ])
    }

# 狀態管理
if 'current_page' not in st.session_state: st.session_state.current_page = "首頁"
if 'ir_sub_market' not in st.session_state: st.session_state.ir_sub_market = None
if 'admin_authenticated' not in st.session_state: st.session_state.admin_authenticated = False

# 自定義 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans TC', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* 大方塊按鈕樣式 */
    div.stButton > button {
        height: 120px;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        background-color: white;
        transition: 0.3s;
        margin-bottom: 20px; 
    }
    div.stButton > button p, div.stButton > button span {
        font-size: 28px !important; 
        font-weight: 700 !important;
        color: #1E293B;
    }
    div.stButton > button:hover {
        border-color: #002D62;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 側邊欄與權限
# ==========================================
st.sidebar.title("🔐 系統管理")
if st.session_state.current_page != "首頁":
    if st.sidebar.button("🏠 返回首頁", type="primary"):
        st.session_state.current_page = "首頁"
        st.session_state.ir_sub_market = None
        st.rerun()

user_role = st.sidebar.radio("身分選擇：", ["👤 一般使用者", "🛡️ 管理員"])

if user_role == "🛡️ 管理員" and not st.session_state.admin_authenticated:
    with st.sidebar.form("auth_form"):
        password = st.text_input("管理員密碼:", type="password")
        if st.form_submit_button("解鎖"):
            if password == "888":
                st.session_state.admin_authenticated = True
                st.rerun()
            else: st.sidebar.error("密碼錯誤")
elif user_role == "🛡️ 管理員" and st.session_state.admin_authenticated:
    if st.sidebar.button("👋 登出管理"):
        st.session_state.admin_authenticated = False
        st.rerun()

# ==========================================
# 3. 畫面邏輯
# ==========================================

# --- 首頁 ---
if st.session_state.current_page == "首頁":
    st.title("元大證券國金-資源彙整")
    st.markdown("---")
    
    # 統計資料與中空圓餅圖
    categories = list(st.session_state['db'].keys())
    counts = [len(st.session_state['db'][cat]) for cat in categories]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories, 
        values=counts, 
        hole=.5,
        marker=dict(colors=['#002D62', '#3B82F6', '#60A5FA', '#93C5FD']),
        textinfo='label+value',
        textfont=dict(size=20, family='Noto Sans TC'), # 🚀 新增：放大字體並指定字型
        hoverinfo='label+percent'
    )])
    
    # 🚀 新增：paper_bgcolor 設為透明 rgba(0,0,0,0)
    fig.update_layout(
        showlegend=False, 
        height=450, 
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.write("### 📂 資料庫導覽")
    # 方塊導覽
    for cat in categories:
        if st.button(f"{cat} (共 {len(st.session_state['db'][cat])} 筆)", use_container_width=True):
            st.session_state.current_page = cat
            st.rerun()

# --- IR 子選單頁面 ---
elif st.session_state.current_page == "IR 會議公司名單" and st.session_state.ir_sub_market is None:
    st.title("🏢 IR 會議公司名單 - 選擇市場")
    st.markdown("請選擇欲檢視的市場板塊：")
    
    col1, col2, col3 = st.columns(3)
    markets = ["美股", "日股", "其他市場"]
    for i, m in enumerate(markets):
        with [col1, col2, col3][i]:
            if st.button(m, use_container_width=True):
                st.session_state.ir_sub_market = m
                st.rerun()

# --- 資料列表頁面 ---
else:
    category_name = st.session_state.current_page
    market_filter = st.session_state.ir_sub_market
    
    display_title = f"{category_name} - {market_filter}" if market_filter else category_name
    st.title(f"📂 {display_title}")
    
    # 讀取資料
    df = st.session_state['db'][category_name]
    if market_filter:
        df = df[df['市場'] == market_filter]
    
    # 搜尋
    search = st.text_input("🔍 搜尋關鍵字...")
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    # 權限判定
    is_admin = (user_role == "🛡️ 管理員" and st.session_state.admin_authenticated)
    
    if is_admin:
        st.success("🛡️ 管理員模式：您可以直接編輯下表並儲存。")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
        if st.button("💾 儲存變更", type="primary"):
            if market_filter:
                original_df = st.session_state['db'][category_name]
                other_markets_df = original_df[original_df['市場'] != market_filter]
                st.session_state['db'][category_name] = pd.concat([other_markets_df, edited_df])
            else:
                st.session_state['db'][category_name] = edited_df
            st.toast("資料已儲存！")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)