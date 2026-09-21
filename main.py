```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()

st.header("1. 시간에 따른 영화별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().unique().tolist()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일일 관객수"
    }
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "영화를 선택하면 시간에 따라 하루 관객수가 어떻게 변했는지 확인할 수 있습니다."
)

st.divider()

st.header("2. 다음 그래프")

st.info(
    "앞으로 시간에 따른 다른 영화 데이터 그래프를 이 구역에 추가할 수 있습니다."
)
```
