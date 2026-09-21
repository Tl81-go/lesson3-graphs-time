# 그래프 4

st.divider()

st.header("4. 일관객 합계 TOP 10 영화")

movie_summary = (
df.groupby("영화명")
.agg(
일관객합계=("일관객", "sum"),
일수=("날짜", "count")
)
.reset_index()
)

top10_movies = (
movie_summary
.sort_values("일관객합계", ascending=False)
.head(10)
.sort_values("일관객합계", ascending=True)
)

fig4 = px.bar(
top10_movies,
x="일관객합계",
y="영화명",
orientation="h",
title="기간 내 일관객 합계 TOP 10",
labels={
"일관객합계": "일관객 합계",
"영화명": "영화"
},
custom_data=["일수"]
)

fig4.update_traces(
hovertemplate=(
"영화: %{y}<br>"
"일관객 합계: %{x:,}명<br>"
"10위권에 든 날수: %{customdata[0]}일"
"<extra></extra>"
)
)

fig4.update_layout(
xaxis_title="일관객 합계(명)",
yaxis_title="영화",
yaxis=dict(
categoryorder="total ascending"
)
)

st.plotly_chart(
fig4,
use_container_width=True
)

st.markdown(
"**이 그래프로 알 수 있는 것:** "
"이 기간 동안 일관객 합계가 가장 큰 영화 10편과 각 영화가 10위권에 등장한 날수를 확인할 수 있습니다."
)
