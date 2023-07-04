import streamlit as st
import requests
from PIL import Image
import re
from bs4 import BeautifulSoup as bs
import tools
import pandas as pd
import os

st.set_page_config(layout="wide")

tab_wanted, tab_stepup = st.tabs(["Wanted 공고", "스텝업 공고"])
with tab_wanted:
    st.header("Wanted 공고")
    if "df" not in st.session_state:
        sql = """
        select * from WANTED_POSTING LIMIT 16;
        """
        data = tools.run_query(sql)
        base_img_url = "https://static.wanted.co.kr/images/wdes"
        base_wanted_url = "https://www.wanted.co.kr/wd"
        
        df = pd.DataFrame.from_records(data)
        df.columns = ["url", "기업 이름", "직무", "지원마감일", "img"]
        df["url"] = [os.path.join(base_wanted_url, str(i)) 
                        for i in df["url"].to_list()]
        df["img"] = [os.path.join(base_img_url, str(i)) 
                        for i in df["img"].to_list()]
        df["bookmark"] = [False] * len(df)
        df = df[["bookmark", "img",
                "기업 이름", "직무", "지원마감일", "url"]]
        st.session_state["df"] = df
        bookmark = df["bookmark"]
        st.session_state["bookmark"] = bookmark
    # else:
    #     df = st.session_state["df"]
    #     bookmark = st.session_state["bookmark"]
    
    st.data_editor(
        df,
        column_config={
            "url" : st.column_config.LinkColumn(
                "공고 URL",
                help = "클릭 시 창을 엽니다."
            ),
            "img" : st.column_config.ImageColumn(
                "Image",
                width = "small",
                help="Streamlit app preview screenshots"
            ),
            "bookmark": st.column_config.CheckboxColumn(
                "관심공고⭐",
                help="관심공고⭐",
                default=False,
            )
        },
        disabled=["img", "기업 이름",
                  "직무", "지원마감일", "url"],
        hide_index=True,)
    
    if not bookmark.equals(df["bookmark"]):
        st.session_state["df"] = df
        st.session_state["bookmark"] = df["bookmark"]
        bookmark = st.session_state["bookmark"]
        
    
    if st.button("click me"):
        st.session_state["df"] = df
    
    
    # number = st.number_input('페이지 넘버', 
    #                         min_value = 1, value = 1,
    #                         step = 1)
    # data = get_wanted(offset = (number-1)*10)
    # containers = [st.container() for i in range(len(data))]
    # for i in range(len(containers)):
    #     with containers[i]:
    #         with st.expander(f'{data[i]["company_name"]}___{data[i]["position"]}'):
    #             st.image(data[i]["thumb"])
    #             st.markdown(data[i]["url"], unsafe_allow_html=True)
with tab_stepup:
    st.header("스텝업 공고")

