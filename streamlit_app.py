import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="MZ 소비 트렌드 대시보드",
    page_icon="💳",
    layout="wide"
)

# --- 2. 제목 및 설명 ---
st.title("💸 MZ세대 소비 트렌드 대시보드")
st.markdown("""
이 대시보드는 **MZ세대의 소비 패턴**을 시각적으로 탐색하기 위해 만들어졌습니다.  
업종별, 연령대별, 월별 소비 변화를 한눈에 파악할 수 있습니다.
""")

st.divider()

# --- 3. 가상 데이터 생성 ---
np.random.seed(42)
n = 5000
data = pd.DataFrame({
    "연도": np.random.choice([2021, 2022, 2023, 2024], n),
    "월": np.random.randint(1, 13, n),
    "연령대": np.random.choice(["20대", "30대", "40대"], n, p=[0.5, 0.35, 0.15]),
    "성별": np.random.choice(["남성", "여성"], n),
    "업종": np.random.choice(["패션", "식음료", "여행", "IT/전자", "엔터테인먼트"], n),
    "소비액": np.random.gamma(3, 100, n).round(0)
})

# --- 4. 사이드바 필터 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1170/1170678.png", width=100)
    st.title("⚙️ 필터 설정")

    year = st.multiselect("연도 선택", sorted(data["연도"].unique()), default=[2023])
    ages = st.multiselect("연령대 선택", ["20대", "30대", "40대"], default=["20대", "30대"])
    genders = st.multiselect("성별 선택", ["남성", "여성"], default=["남성", "여성"])
    industries = st.multiselect("업종 선택", data["업종"].unique(), default=data["업종"].unique())

    show_raw = st.checkbox("📄 원본 데이터 보기", value=False)

st.divider()

# --- 5. 데이터 필터링 ---
filtered = data[
    data["연도"].isin(year) &
    data["연령대"].isin(ages) &
    data["성별"].isin(genders) &
    data["업종"].isin(industries)
]

# --- 6. KPI 카드 ---
total_spend = int(filtered["소비액"].sum())
avg_spend = int(filtered["소비액"].mean())
num_transactions = len(filtered)

col1, col2, col3 = st.columns(3)
col1.metric("💰 총 소비액", f"{total_spend:,.0f} 원")
col2.metric("💳 평균 결제액", f"{avg_spend:,.0f} 원")
col3.metric("🧾 거래 건수", f"{num_transactions:,} 건")

st.divider()

# --- 7. 시각화 영역 ---

# (1) 업종별 평균 소비액
st.subheader("🏪 업종별 평균 소비액 비교")
fig1 = px.bar(
    filtered.groupby("업종")["소비액"].mean().reset_index(),
    x="업종", y="소비액",
    text_auto=".2s",
    color="업종",
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig1.update_layout(showlegend=False, height=400)
st.plotly_chart(fig1, use_container_width=True)

# (2) 월별 소비 트렌드
st.subheader("📅 월별 소비 트렌드")
fig2 = px.line(
    filtered.groupby(["연도", "월"])["소비액"].mean().reset_index(),
    x="월", y="소비액", color="연도",
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig2.update_traces(line=dict(width=3))
st.plotly_chart(fig2, use_container_width=True)

# (3) 연령대 & 성별별 소비액 비교
st.subheader("👥 연령대 및 성별별 소비 성향")
fig3 = px.box(
    filtered,
    x="연령대", y="소비액", color="성별",
    points="all",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig3, use_container_width=True)

# --- 8. 원본 데이터 보기 ---
if show_raw:
    st.divider()
    st.subheader("📄 필터링된 원본 데이터")
    st.dataframe(filtered, use_container_width=True)
