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


# 그래프 1
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

fig1 = px.line(
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

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "영화를 선택하면 시간에 따라 하루 관객수가 어떻게 변했는지 확인할 수 있습니다."
)


# 그래프 2
st.divider()

st.header("2. 일관객 합계가 가장 큰 5편의 변화")

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_totals.head(5)["영화명"].tolist()

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["영화명", "날짜"]
)

graph2_title = "일관객 합계 상위 5편의 날짜별 일관객"

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title=graph2_title,
    labels={
        "날짜": "날짜",
        "일관객": "일일 관객수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "이 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 관객수 변화를 비교할 수 있습니다."
)


# 그래프 3
st.divider()

st.header("3. 날짜별 10위권 일관객 합계")

daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

top3_days = (
    daily_audience
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

fig3 = px.area(
    daily_audience,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일일 관객수 합계"
    }
)

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "10위권 관객수 합계: %{y:,}명"
        "<extra></extra>"
    )
)

for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br>{row['일관객']:,}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일일 관객수 합계(명)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "날짜별 10위권 영화의 관객수 합계와 관객이 가장 많았던 3일을 확인할 수 있습니다."
)


# 다음 그래프 공간
st.divider()

st.header("4. 다음 그래프")

st.info(
    "앞으로 새로운 영화 데이터 그래프를 이 구역에 추가할 수 있습니다."
)
