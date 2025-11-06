import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💳 MZ세대 소비 트렌드 대시보드")

# 가상 데이터 예시
data = pd.DataFrame({
    "연도": [2022, 2022, 2023, 2023]*3,
    "월": [1, 2, 1, 2]*3,
    "연령대": ["20대", "30대", "40대"]*4,
    "업종": ["패션", "식음료", "여행", "IT"]*3,
    "소비액": [200, 240, 300, 280, 180, 220, 260, 240, 150, 200, 230, 220]
})

# 선택
year = st.selectbox("연도 선택", sorted(data["연도"].unique()))
age_group = st.multiselect("연령대 선택", data["연령대"].unique(), default=["20대", "30대"])

filtered = data[(data["연도"] == year) & (data["연령대"].isin(age_group))]

# 시각화
fig = px.bar(filtered, x="업종", y="소비액", color="연령대", barmode="group", title="업종별 소비액 비교")
st.plotly_chart(fig)

st.write("📈 월별 소비 추이")
fig2 = px.line(filtered, x="월", y="소비액", color="연령대", markers=True)
st.plotly_chart(fig2)
