import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="MZ 소비 트렌드 대시보드",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded" # 사이드바를 기본으로 펼치기
)

# --- 2. 제목 및 설명 ---
st.title("💸 MZ세대 소비 트렌드 대시보드")
st.markdown("""
이 대시보드는 **MZ세대의 소비 패턴**을 시각적으로 탐색하기 위한 예제입니다.
사이드바에서 필터를 조정하여 데이터를 탐색해보세요.
""")

st.divider()

# --- 3. 가상 데이터 생성 (원본과 동일) ---
@st.cache_data # 데이터 로딩 캐시
def load_data():
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
    return data

data = load_data()

# --- 4. 사이드바 필터 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1170/1170678.png", width=100)
    st.header("⚙️ 필터 설정")
    st.info("필터를 선택하면 대시보드가 실시간으로 업데이트됩니다.")

    year = st.multiselect("📅 연도 선택", sorted(data["연도"].unique()), default=[2023, 2024])
    ages = st.multiselect("🧑 연령대 선택", ["20대", "30대", "40대"], default=["20대", "30대"])
    genders = st.multiselect("🚻 성별 선택", ["남성", "여성"], default=["남성", "여성"])
    industries = st.multiselect("🛍️ 업종 선택", data["업종"].unique(), default=data["업종"].unique())

    st.divider()
    show_raw = st.checkbox("📄 원본 데이터 보기", value=False)


# --- 5. 데이터 필터링 ---
filtered = data[
    data["연도"].isin(year) &
    data["연령대"].isin(ages) &
    data["성별"].isin(genders) &
    data["업종"].isin(industries)
]

# 필터링된 데이터가 없을 경우 처리
if filtered.empty:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다. 필터를 조정해주세요.")
    st.stop()

# --- 6. KPI 카드 (컨테이너 사용) ---
with st.container(border=True):
    st.subheader("📊 핵심 요약 (KPIs)")
    total_spend = int(filtered["소비액"].sum())
    avg_spend = int(filtered["소비액"].mean())
    num_transactions = len(filtered)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 총 소비액", f"{total_spend:,.0f} 원",
                help="선택한 기간, 연령, 성별, 업종의 총 소비액 합계입니다.")
    col2.metric("💳 평균 결제액", f"{avg_spend:,.0f} 원",
                help="선택한 조건에서의 1회 평균 결제 금액입니다.")
    col3.metric("🧾 총 거래 건수", f"{num_transactions:,} 건",
                help="선택한 조건에서의 총 거래 횟수입니다.")

st.divider()

# --- 7. 시각화 영역 (레이아웃 변경) ---
st.subheader("📈 상세 소비 패턴 분석")

col1, col2 = st.columns([3, 2]) # 3:2 비율로 컬럼 나누기

with col1:
    # (1) 업종별 평균 소비액
    st.markdown("#### 🏪 업종별 평균 소비액")
    fig1_data = filtered.groupby("업종")["소비액"].mean().reset_index().sort_values(by="소비액", ascending=False)
    fig1 = px.bar(
        fig1_data,
        x="업종", y="소비액",
        text_auto=".2s",
        color="업종",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig1.update_layout(showlegend=False, height=400, yaxis_title="평균 소비액 (원)")
    st.plotly_chart(fig1, use_container
