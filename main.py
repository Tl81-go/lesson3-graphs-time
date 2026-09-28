
import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# ==========================================
# 데이터 불러오기
# ==========================================

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_daily.csv"

df = pd.read_csv(DATA_URL)


# ==========================================
# 데이터 전처리
# ==========================================

# 날짜를 진짜 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)

# 숫자형 데이터 변환
df["일관객"] = pd.to_numeric(df["일관객"], errors="coerce")


# ==========================================
# 그래프 1. 영화별 일관객 변화
# ==========================================

st.divider()
st.header("그래프 1. 영화별 일관객 변화")

# 영화 선택
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화만 필터링
movie_df = df[
    df["영화명"] == selected_movie
].sort_values("날짜")


# Plotly 선 그래프
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객"
    }
)

# 마우스를 올렸을 때 날짜와 관객수 표시
fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객",
    hovermode="x"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==========================================
# 그래프로 알 수 있는 것
# ==========================================

st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "여기에 선택한 영화의 날짜별 일관객 변화에서 알 수 있는 내용을 한 문장으로 작성하세요."
)


# ==========================================
# 앞으로 추가할 그래프
# ==========================================

st.divider()
st.header("그래프 2")
st.write("다음 그래프를 여기에 추가하세요.")

st.divider()
st.header("그래프 3")
st.write("다음 그래프를 여기에 추가하세요.")
