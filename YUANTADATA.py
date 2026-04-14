with top_col2:
        # 使用一段隱形空間直接把按鈕往下推 (你可以微調 120px 這個數字來決定高低)
        st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
        
        if st.button("📅 點擊查看\n元大下半年行程", use_container_width=True, key="btn_schedule"):
            st.session_state.current_page = "元大下半年行程"
            st.rerun()
