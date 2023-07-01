import streamlit as st
import requests
from PIL import Image
import re
from bs4 import BeautifulSoup as bs




def get_wanted(offset : int = 0):
    url=f"https://www.wanted.co.kr/api/v4/jobs?1687507695204&country=kr&tag_type_ids=10231&tag_type_ids=1025&tag_type_ids=1024&tag_type_ids=655&locations=all&years=0&years=2&limit=10&offset={offset}&job_sort=company.response_rate_order"
    response=requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        if data:
            data = [{"company_name" :i["company"]["name"],
                     "due_time" :i["due_time"],
                     "thumb" : i["logo_img"]["thumb"],
                     "address" : i["address"],
                     "position" : i["position"],
                     "url" : f"https://www.wanted.co.kr/wd/{i['id']}"} for i in data]
            return data
    return -1
def get_stepup():
    url="https://cafe.naver.com/ArticleList.nhn?search.clubid=15754634&search.menuid=374&search.boardtype=L"
    response= requests.get(url)
    soup=bs(response.text,"html.parser")
    elements= soup.find_all("div","article-board m-tcol-c")[1]
    e=elements.table.tbody.find_all("tr")
    e=e[:5:2]
    url_list={}
    for row in e:
        temp={}
        title=re.sub(r'[^\w]','',row.td.find("div","inner_list").a.text)
        if "신입" in title:
            url_list["신입"]="https://cafe.naver.com/specup"+row.td.find("div","inner_list").a["href"]
        elif "인턴" in title:
            url_list["인턴"]="https://cafe.naver.com/specup"+row.td.find("div","inner_list").a["href"]
    
    response= requests.get(url_list["인턴"])
    soup=bs(response.text,"html.parser")
    divs= soup.find_all("div","tbody m-tcol-c")[0].div.find_all("div")
    img_link="https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fi.ibb.co%2FVH1ZBkT%2F5.png%22&type=cafe_wa740"
    for div in divs:
        if div.table:
            if div.table.tbody.tr.img["src"]==img_link:
                tbody = div.table.tbody

    intern_job_list=[]
        
    trs= list(map(lambda x:x.find_all("td"),tbody.find_all("tr")[2::2]))
    for tds in trs:
        url=tds[0].a["href"]
        temp={}
        temp["corporation_name"]=tds[0].a.text
        temp["job_name"]=tds[1].a.text
        if tds[2].span:
            temp["end_date"]=tds[2].span.text
        else:
            temp["end_date"]=tds[2].text
        temp["url"]=url
        intern_job_list.append(temp)
        
    response= requests.get(url_list["신입"])
    soup=bs(response.text,"html.parser")
    divs= soup.find_all("div","tbody m-tcol-c")[0].div.find_all("div")[2:]
    # divs
    tbody = divs[0].table.tbody
    big_job_list=[]
    temp= list(map(lambda x:x.find_all("td"),tbody.find_all("tr")[2::2]))
    trs=[]
    for tr in temp:
        if tr:
            trs.append(tr)
            
    for tds in trs:
        url=tds[0].a["href"]
        temp={}
        temp["corporation_name"]=tds[0].a.text
        temp["job_name"]=tds[1].a.text
        if tds[2].span:
            temp["end_date"]=tds[2].span.text
        else:
            temp["end_date"]=tds[2].text
        temp["url"]=url
        big_job_list.append(temp)

    tbody = divs[1].table.tbody
    middle_job_list=[]
    temp= list(map(lambda x:x.find_all("td"),tbody.find_all("tr")[2::2]))
    trs=[]
    for tr in temp:
        if tr:
            trs.append(tr)
    for tds in trs:
        url=tds[0].a["href"]
        temp={}
        temp["corporation_name"]=tds[0].a.text
        temp["job_name"]=tds[1].a.text
        if tds[2].span:
            temp["end_date"]=tds[2].span.text
        else:
            temp["end_date"]=tds[2].text
        temp["url"]=url
        middle_job_list.append(temp)

    tbody = divs[2].table.tbody
    popular_job_list=[]
    temp= list(map(lambda x:x.find_all("td"),tbody.find_all("tr")[2::2]))
    trs=[]
    for tr in temp:
        if tr:
            trs.append(tr)
    for tds in trs:
        url=tds[0].a["href"]
        temp={}
        temp["corporation_name"]=tds[0].a.text
        temp["job_name"]=tds[1].a.text
        if tds[2].span:
            temp["end_date"]=tds[2].span.text
        else:
            temp["end_date"]=tds[2].text
        temp["url"]=url
        popular_job_list.append(temp)
    
    return intern_job_list, big_job_list, middle_job_list, popular_job_list
            
intern_job_list, big_job_list, middle_job_list, popular_job_list = get_stepup()


tab_wanted, tab_stepup = st.tabs(["Wanted 공고", "스텝업 공고"])
with tab_wanted:
    st.header("Wanted 공고")
    number = st.number_input('페이지 넘버', 
                            min_value = 1, value = 1,
                            step = 1)
    data = get_wanted(offset = (number-1)*10)
    containers = [st.container() for i in range(len(data))]
    for i in range(len(containers)):
        with containers[i]:
            with st.expander(f'{data[i]["company_name"]}___{data[i]["position"]}'):
                st.image(data[i]["thumb"])
                st.markdown(data[i]["url"], unsafe_allow_html=True)
with tab_stepup:
    tab_intern, tab_big, tab_mid, tab_pop = st.tabs(["인턴 공고", "대기업 공고",
                                                     "중견기업 공고", "실시간 인기 공고"])
    with tab_intern:
        st.write(intern_job_list)
    with tab_big:
        st.write(big_job_list)
    with tab_mid:
        st.write(middle_job_list)
    with tab_pop:
        st.write(popular_job_list)
