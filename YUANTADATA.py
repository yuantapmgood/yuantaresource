st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans TC', sans-serif; }
    
    /* ==========================================
       修改這裡：設定圖片背景並加上半透明遮罩
       ========================================== */
    .stApp { 
        /* 設定背景圖片 */
        background-image: url("background.jpg");
        /* 圖片覆蓋整個螢幕 */
        background-size: cover;
        /* 圖片置中 */
        background-position: center;
        /* 不重複圖片 */
        background-repeat: no-repeat;
        /* 加上一層半透明白色遮罩 (rgba 的最後一個數字 0.85 代表 85% 不透明度)
           你可以調整這個數字（0 到 1 之間）來決定遮罩的濃淡。
           這就是達到「模糊」或「淡淡浮水印」效果的關鍵。
        */
        box-shadow: inset 0 0 0 2000px rgba(248, 250, 252, 0.85); 
    }

    /* 大方塊按鈕樣式 */
    div.stButton > button {
        height: 140px;
        border-radius: 16px;
        border: 2px solid #E5E7EB;
        background-color: white; /* 保持按鈕背景為白色，確保字體清晰 */
        transition: 0.3s;
        margin-bottom: 20px;
    }
    /* ... 保持原本的按鈕樣式 ... */
    
    /* 針對行程按鈕特別調整高度與對齊 ... */
    .schedule-btn div.stButton > button {
        height: 180px !important; 
        margin-top: 100px !important; 
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
        border: 2px solid #B5D4F4;
    }

    /* ... 保持原本的其他樣式 ... */
    </style>
""", unsafe_allow_html=True)
