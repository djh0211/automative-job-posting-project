import streamlit as st
import requests
from PIL import Image
import re
from bs4 import BeautifulSoup as bs
import tools
import pandas as pd
import os

st.set_page_config(layout="wide")

job_num_dic = {"소프트웨어 엔지니어" : 10110,
               "파이썬 개발자" : 899,
               "데이터 엔지니어" : 655,
               "데이터 사이언티스트" : 1024,
               "빅데이터 엔지니어" : 1025,
               "DBA" : 10231}
base_img_url = "https://static.wanted.co.kr/images/wdes"
base_wanted_url = "https://www.wanted.co.kr/wd"

tab_wanted, tab_stepup = st.tabs(["Wanted 공고", "스텝업 공고"])
with tab_wanted:
    option_col, main_col = st.columns(spec = [2, 7])
    with option_col:
        multiselect_job_class = st.multiselect(
            '직무 선택 (다중선택가능)',
            list(job_num_dic.keys())
            )
    with main_col:
        if not multiselect_job_class:
            if "wanted_data" not in st.session_state:
                sql = """
                    select * from WANTED_POSTING ORDER BY DUE_DATE;
                    """
                data = tools.run_query(sql)
                wanted_df = pd.DataFrame.from_records(data)
                wanted_df["bookmark"] = [False] * len(wanted_df)
                wanted_df = tools.preprocess_wanted_dataframe(wanted_df)
                st.session_state["wanted_df"] = wanted_df
                
            a = st.data_editor(
                st.session_state["wanted_df"].iloc[:15],
                height = 565,
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
                        "⭐",
                        help="관심공고⭐",
                        default=False,
                        required=True
                    )
                },
                disabled=["img", "기업 이름",
                        "직무", "지원마감일", "url"],
                hide_index=True,)
            # TODO
            st.write(list(map(lambda x:int(x.split("/")[-1]),
                              a["url"].loc[a["bookmark"]].tolist())))
            
                            



    #     df["bookmark"] = [False] * len(df)
    #     df = df[["bookmark", "img",
    #             "기업 이름", "직무", "지원마감일", "url"]]
    #     st.session_state["df"] = df
    #     bookmark = df["bookmark"]
    #     st.session_state["bookmark"] = bookmark
    # # else:
    # #     df = st.session_state["df"]
    # #     bookmark = st.session_state["bookmark"]
    
    # st.data_editor(
    #     df,
    #     column_config={
    #         "url" : st.column_config.LinkColumn(
    #             "공고 URL",
    #             help = "클릭 시 창을 엽니다."
    #         ),
    #         "img" : st.column_config.ImageColumn(
    #             "Image",
    #             width = "small",
    #             help="Streamlit app preview screenshots"
    #         ),
    #         "bookmark": st.column_config.CheckboxColumn(
    #             "관심공고⭐",
    #             help="관심공고⭐",
    #             default=False,
    #         )
    #     },
    #     disabled=["img", "기업 이름",
    #               "직무", "지원마감일", "url"],
    #     hide_index=True,)
    
    # if not bookmark.equals(df["bookmark"]):
    #     st.session_state["df"] = df
    #     st.session_state["bookmark"] = df["bookmark"]
    #     bookmark = st.session_state["bookmark"]
        
    
    # if st.button("click me"):
    #     st.session_state["df"] = df
    
    
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

