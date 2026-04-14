import streamlit as st
import pandas as pd
import os
from streamlit_echarts import st_echarts
import base64

def set_background_from_local(image_path):
    """讀取本地端圖片並設定為 Streamlit 背景"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # 注入 CSS
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        /* 因為你的附圖資訊量很大，建議加上一層半透明的白色遮罩，才不會讓原本網站的字看不清楚 */
        box-shadow: inset 0 0 0 2000px rgba(248, 250, 252, 0.5); 
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
# ==========================================
# 1. 頁面與視覺設定
# ==========================================
st.set_page_config(page_title="元大證券國金-資源彙整", page_icon="🏦", layout="wide")

# 請將檔名替換成你實際儲存的圖片檔名
set_background_from_local('yuantaschedule.png')

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
        color: #002D62;
    }
    div.stButton > button:hover {
        border-color: #002D62;
        background-color: #F0F4F8;
        box-shadow: 0 8px 20px rgba(0, 45, 98, 0.15);
        transform: translateY(-2px);
    }

    /* Gauge 標題樣式 */
    .gauge-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        color: #002D62;
        margin-bottom: 0px;
        padding-top: 8px;
    }

    /* 壓縮首頁標題與圖表之間的間距 */
    .block-container { padding-top: 3rem !important; padding-bottom: 0 !important; }
    h1 { margin-top: 0 !important; margin-bottom: 0 !important; padding-bottom: 0 !important; }
    iframe { margin-top: -1rem !important; }

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
    '論壇講師':       '論壇講師.csv',
    '專家領域':       '專家領域.csv',
    '研究資源':       '研究資源.csv'
}

DEFAULT_COLUMNS = {
    'IR 會議公司名單': ['市場', '公司', 'Ticker'],
    '論壇講師':       ['專家', '曾舉辦議題'],
    '專家領域':       ['專家', '內容摘要', '相關標的'],
    '研究資源':       ['上手', '資源類型']
}

CATEGORY_LABELS = {
    'IR 會議公司名單': 'IR 會議公司',
    '論壇講師':       '論壇講師',
    '專家領域':       '專家領域',
    '研究資源':       '研究資源'
}

CATEGORY_MAX = {
    'IR 會議公司名單': 200,
    '論壇講師':       100,
    '專家領域':       100,
    '研究資源':       100
}

# 四個板塊各自的專屬單位設定
CATEGORY_UNITS = {
    'IR 會議公司名單': '家',
    '論壇講師':       '位',
    '專家領域':       '位',
    '研究資源':       '筆'
}

# 四個板塊各自的配色 [淺色, 中色, 深色]
CATEGORY_COLORS = {
    'IR 會議公司名單': ["#E8F5E9", "#81C784", "#2E7D32"],   # 綠色系
    '論壇講師':       ["#FFF3E0", "#FFB74D", "#E65100"],   # 橘色系
    '專家領域':       ["#F3E5F5", "#BA68C8", "#6A1B9A"],   # 紫色系
    '研究資源':       ["#E0F7FA", "#4DD0E1", "#00695C"],   # 青色系
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
# 4. 側邊欄
# ==========================================
with st.sidebar:
    st.title("導覽列")
    if st.session_state.current_page != '總覽首頁':
        if st.button("🏠 返回總覽首頁", use_container_width=True, type="primary"):
            st.session_state.current_page = '總覽首頁'
            st.rerun()
    st.markdown("---")

# ==========================================
# 5. 小 Gauge 產生器（四個板塊用）- 加入 unit 參數
# ==========================================
def make_mini_gauge(label, value, max_val, colors, unit):
    light, mid, dark = colors
    return {
        "backgroundColor": "transparent",
        "series": [{
            "type": "gauge",
            "startAngle": 180,
            "endAngle": 0,
            "min": 0,
            "max": max_val,
            "splitNumber": 4,
            "radius": "88%",
            "center": ["50%", "68%"],
            "pointer": {
                "show": True,
                "length": "65%",
                "width": 4,
                "itemStyle": {"color": "#C0392B"}
            },
            "axisLine": {
                "lineStyle": {
                    "width": 16,
                    "color": [
                        [0.5, light],
                        [0.8, mid],
                        [1.0, dark]
                    ]
                }
            },
            "axisTick": {
                "distance": -16,
                "splitNumber": 4,
                "lineStyle": {"color": dark, "width": 1}
            },
            "splitLine": {
                "distance": -16,
                "length": 10,
                "lineStyle": {"color": dark, "width": 2}
            },
            "axisLabel": {
                "color": dark,
                "fontSize": 10,
                "distance": 4,
                "fontFamily": "Noto Sans TC"
            },
            "anchor": {
                "show": True,
                "showAbove": True,
                "size": 10,
                "itemStyle": {"color": "#C0392B"}
            },
            "detail": {
                "valueAnimation": True,
                "formatter": f"{{value}} {unit}",  # 動態替換為 家、位 或 筆
                "color": dark,
                "fontSize": 18,
                "fontWeight": "bold",
                "fontFamily": "Noto Sans TC",
                "offsetCenter": [0, "20%"]
            },
            "title": {
                "show": True,
                "offsetCenter": [0, "-25%"],
                "color": dark,
                "fontSize": 13,
                "fontWeight": "bold",
                "fontFamily": "Noto Sans TC"
            },
            "data": [{"value": value, "name": label}]
        }]
    }

# ==========================================
# 6. 畫面邏輯 - 總覽首頁
# ==========================================
if st.session_state.current_page == '總覽首頁':
    st.markdown("<h1 style='text-align: center; margin-bottom: 0; padding-bottom: 0;'>元大證券國金 - 資源總覽</h1>", unsafe_allow_html=True)

    # 讀取各板塊數量
    db_counts = {}
    total_records = 0
    for cat in FILE_MAP.keys():
        df_temp = load_data(cat)
        count = len(df_temp)
        db_counts[cat] = count
        total_records += count

    MAX_CAPACITY = 500

    # --- 主 Gauge ---
    # (主圖表為彙總資料，維持「筆」為單位)
    gauge_option = {
        "backgroundColor": "transparent",
        "series": [{
            "type": "gauge",
            "startAngle": 180,
            "endAngle": 0,
            "min": 0,
            "max": MAX_CAPACITY,
            "splitNumber": 5,
            "radius": "90%",
            "center": ["50%", "80%"],
            "pointer": {
                "show": True,
                "length": "70%",
                "width": 6,
                "itemStyle": {"color": "#C0392B"}
            },
            "axisLine": {
                "lineStyle": {
                    "width": 30,
                    "color": [
                        [0.5,  "#E6F1FB"],
                        [0.8,  "#B5D4F4"],
                        [1.0,  "#85B7EB"]
                    ]
                }
            },
            "axisTick": {
                "distance": -30,
                "splitNumber": 5,
                "lineStyle": {"color": "#185FA5", "width": 1}
            },
            "splitLine": {
                "distance": -30,
                "length": 14,
                "lineStyle": {"color": "#185FA5", "width": 2}
            },
            "axisLabel": {
                "color": "#185FA5",
                "fontSize": 13,
                "distance": 8,
                "fontFamily": "Noto Sans TC"
            },
            "anchor": {
                "show": True,
                "showAbove": True,
                "size": 14,
                "itemStyle": {"color": "#C0392B"}
            },
            "title": {
                "show": True,
                "offsetCenter": [0, "-20%"],
                "color": "#002D62",
                "fontSize": 20,
                "fontWeight": "bold",
                "fontFamily": "Noto Sans TC"
            },
            "detail": {
                "valueAnimation": True,
                "formatter": "{value} 筆",
                "color": "#002D62",
                "fontSize": 40,
                "fontWeight": "bold",
                "fontFamily": "Noto Sans TC",
                "offsetCenter": [0, "30%"]
            },
            "data": [{"value": total_records, "name": "總資源量"}]
        }]
    }

    st_echarts(options=gauge_option, height="360px")

    # --- 四個小 Gauge 板塊 ---
    st.markdown("#### 各板塊資料量")
    col1, col2, col3, col4 = st.columns(4)
    for col, (cat, label) in zip([col1, col2, col3, col4], CATEGORY_LABELS.items()):
        with col:
            mini_opt = make_mini_gauge(
                label=label,
                value=db_counts[cat],
                max_val=CATEGORY_MAX[cat],
                colors=CATEGORY_COLORS[cat],
                unit=CATEGORY_UNITS[cat]  # 傳入專屬的單位
            )
            st_echarts(options=mini_opt, height="200px")

    st.markdown("---")
    st.write("### 快速進入板塊 (點擊下方方塊)")

    # --- 四大方塊導航 ---
    col1, col2 = st.columns(2)
    categories = list(FILE_MAP.keys())
    for i, cat in enumerate(categories):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if st.button(cat, use_container_width=True, key=f"btn_{cat}"):
                st.session_state.current_page = cat
                st.rerun()

# ==========================================
# 7. 畫面邏輯 - 獨立資料庫頁面 (純檢視)
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

    styled_df = df.style.set_properties(**{
        'white-space': 'pre-wrap',
        'text-align': 'left',
        'min-width': '150px'
    })

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=600
    )
