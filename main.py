import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")

# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 진짜 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)


# ============================================================
# 그래프 1
# ============================================================
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.write(
    "선택한 영화의 날짜별 관객 수가 어떻게 증가하거나 감소했는지 알 수 있습니다."
)


# ============================================================
# 그래프 2
# ============================================================
st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편")

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_totals.head(5)["영화명"].tolist()

top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.write(
    "이 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 관객 변화와 서로 다른 흥행 흐름을 비교할 수 있습니다."
)


# ============================================================
# 그래프 3
# ============================================================
st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

daily_audience = daily_audience.rename(
    columns={"일관객": "10위권_일관객_합계"}
)

top3_days = (
    daily_audience
    .nlargest(3, "10위권_일관객_합계")
    .sort_values("날짜")
)

fig3 = px.area(
    daily_audience,
    x="날짜",
    y="10위권_일관객_합계",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "10위권_일관객_합계": "10위권 일관객 합계"
    }
)

fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객 합계: %{y:,}명<extra></extra>"
)

for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["10위권_일관객_합계"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-45
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.write(
    "날짜별 10위권 전체의 관객 규모를 비교하여 어느 날 영화관 관객이 가장 많았는지 알 수 있습니다."
)


# ============================================================
# 그래프 4
# ============================================================
st.divider()

st.header("그래프 4. 기간 전체 일관객 TOP 10")

# 영화별 기간 전체 일관객 합계
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객_합계=("일관객", "sum"),
        10위권_등장_일수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계가 많은 순으로 정렬하여 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객_합계", ascending=False)
    .head(10)
)

# 가로 막대그래프에서 위쪽부터 관객이 많은 영화가 나오도록
top10_movies = top10_movies.sort_values("일관객_합계", ascending=True)

fig4 = px.bar(
    top10_movies,
    x="일관객_합계",
    y="영화명",
    orientation="h",
    title="기간 전체 일관객 TOP 10",
    labels={
        "일관객_합계": "기간 전체 일관객 합계",
        "영화명": "영화"
    },
    custom_data=["10위권_등장_일수"]
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 전체 일관객 합계(명)",
    yaxis_title="영화",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.write(
    "이 기간 동안 누적 일관객이 많았던 영화와 각 영화가 10위권에 등장한 날수를 함께 비교할 수 있습니다."
)


# ============================================================
# 앞으로 추가할 그래프
# ============================================================
st.divider()

st.header("그래프 5. 앞으로 추가할 그래프")

st.info("다음 그래프를 이 구역 아래에 추가하세요.")

# 여기에 다섯 번째 그래프를 추가합니다.
